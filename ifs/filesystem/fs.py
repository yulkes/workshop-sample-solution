import abc
import os
from abc import abstractmethod
from pathlib import Path

from .models import (
    DirectoryListing,
    DirListingRequest,
    RenameFileRequest,
    DeleteFileRequest,
)


class FileSystemException(Exception):
    pass


class AbstractFileSystemService(abc.ABC):
    @abstractmethod
    def get_dir_list(self, request: DirListingRequest) -> DirectoryListing:
        pass

    @abstractmethod
    def rename_file(self, request: RenameFileRequest):
        pass

    @abstractmethod
    def delete_file(self, request: DeleteFileRequest):
        pass


class RealFileSystemService(AbstractFileSystemService):
    def __init__(self, root_path: Path):
        self.root_path = root_path.resolve()

    def get_dir_list(self, request: DirListingRequest) -> DirectoryListing:
        dir_list_path = request.base_path
        full_path = self._validate_safe_path(
            dir_list_path, force_dir=True, should_exist=True
        )
        result = DirectoryListing(dir_list_path)
        for file in full_path.iterdir():
            result.add_file(file)
        return result

    def _validate_safe_path(self, path, force_dir=False, should_exist=True):
        if path.is_absolute():
            raise FileSystemException(
                f"Security Error, absolute paths are not allowed: {path}", path
            )
        full_path = (self.root_path / path).resolve()
        # Try to catch tricks to go outside the scope of the given root path (Like using ".." for dir traversal)
        if self.root_path not in full_path.parents and self.root_path != full_path:
            raise FileSystemException(
                f"Security Error, file path is outside allowed root: {path}", path
            )
        # Check existence:
        if should_exist and not full_path.exists():
            raise FileSystemException(f"Given path does not exist: {path}", path)
        elif not should_exist and full_path.exists():
            raise FileSystemException(f"Given path exists: {path}", path)

        if force_dir and not full_path.is_dir():
            raise FileSystemException(f"Given path is not a directory: {path}", path)
        return full_path

    def rename_file(self, request: RenameFileRequest):
        source_path = self._validate_safe_path(request.old_path, should_exist=True)
        target_path = self._validate_safe_path(request.new_path, should_exist=False)
        try:
            os.renames(source_path, target_path)
        except OSError as oe:
            raise FileSystemException("Failed moving file",)

    def delete_file(self, request: DeleteFileRequest):
        full_path = self._validate_safe_path(request.file_path)
        try:
            if full_path.is_dir():
                full_path.rmdir()
            elif full_path.is_file():
                os.remove(full_path)
            else:
                raise FileSystemException(
                    f"Cannot delete this type of file: {request.file_path}",
                    request.file_path,
                )
        except OSError as oe:
            raise FileSystemException(
                f"Failed deleting path: {request.file_path}"
            ) from oe
