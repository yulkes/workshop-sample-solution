import abc
from abc import abstractmethod

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
