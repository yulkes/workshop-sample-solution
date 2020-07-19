import abc
from abc import abstractmethod
from pathlib import Path

from ifs.models import (
    DirectoryListing,
    DirListingRequest,
    RenameFileRequest,
    DeleteFileRequest,
)


class AbstractFileSystemService(abc.ABC):
    @abstractmethod
    def get_dir_list(self, request: DirListingRequest) -> DirectoryListing:
        pass

    @abstractmethod
    def rename_file(self, request: RenameFileRequest) -> bool:
        pass

    @abstractmethod
    def delete_file(self, request: DeleteFileRequest) -> bool:
        pass


class RealFileSystemService(AbstractFileSystemService):
    def __init__(self, root_path: Path):
        self.root_path = root_path.absolute()

    def get_dir_list(self, request: DirListingRequest) -> DirectoryListing:
        dir_list_path = request.base_path
        self.validate_safe_path(dir_list_path)

        result = DirectoryListing(dir_list_path)
        for file in dir_list_path.iterdir():
            result.add_file(file)
        return result

    def validate_safe_path(self, path):
        if path.is_absolute():
            raise ValueError(
                f"Security Error, absolute paths are not allowed: {path}", path
            )
        full_path = self.root_path / path
        # Try to catch tricks to go outside the scope of the given root path (Like using ".." for dir traversal)
        if full_path > self.root_path:
            raise ValueError(
                f"Security Error, file path is outside allowed root: {path}", path
            )
        if not full_path.exists():
            raise ValueError(
                f"Given path does not exist: {full_path.name}", full_path.name
            )
        if not full_path.is_dir():
            raise ValueError(
                f"Given path is not a directory: {full_path.name}", full_path.name
            )

    def rename_file(self, request: RenameFileRequest) -> bool:
        pass

    def delete_file(self, request: DeleteFileRequest) -> bool:
        pass
