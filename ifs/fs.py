import abc
import os
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
        self.root_path = root_path.resolve()

    def get_dir_list(self, request: DirListingRequest) -> DirectoryListing:
        dir_list_path = request.base_path
        full_path = self._validate_safe_path(dir_list_path)
        result = DirectoryListing(dir_list_path)
        for file in full_path.iterdir():
            result.add_file(file)
        return result

    def _validate_safe_path(self, path, force_directory=True):
        if path.is_absolute():
            raise ValueError(
                f"Security Error, absolute paths are not allowed: {path}", path
            )
        full_path = (self.root_path / path).resolve()
        # Try to catch tricks to go outside the scope of the given root path (Like using ".." for dir traversal)
        if self.root_path not in full_path.parents and self.root_path != full_path:
            raise ValueError(
                f"Security Error, file path is outside allowed root: {path}", path
            )
        if not full_path.exists():
            raise ValueError(f"Given path does not exist: {path}", path)
        if force_directory and not full_path.is_dir():
            raise ValueError(f"Given path is not a directory: {path}", path)
        return full_path

    def rename_file(self, request: RenameFileRequest):
        return False

    def delete_file(self, request: DeleteFileRequest):
        full_path = self._validate_safe_path(request.file_path, force_directory=False)
        if full_path.is_dir():
            try:
                full_path.rmdir()
            except OSError as oe:
                raise ValueError(
                    f"Failed deleting directory: {request.file_path}"
                ) from oe
        elif full_path.is_file():
            os.remove(full_path)
        else:
            raise ValueError(
                f"Cannot delete this type of file: {request.file_path}",
                request.file_path,
            )
