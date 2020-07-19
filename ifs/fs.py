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
        self.root_path = root_path

    def get_dir_list(self, request: DirListingRequest) -> DirectoryListing:
        full_path = self.root_path / request.base_path
        if self.root_path not in full_path.parents:
            raise ValueError(
                "Security Error, file path is outside allowed root: %s",
                request.base_path,
            )
        return DirectoryListing(request.base_path)

    def rename_file(self, request: RenameFileRequest) -> bool:
        pass

    def delete_file(self, request: DeleteFileRequest) -> bool:
        pass
