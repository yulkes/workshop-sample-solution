from dataclasses import dataclass, field
from logging import Logger
from pathlib import Path
from typing import List

logger = Logger(__name__)


@dataclass
class DirectoryListing:
    base_path: Path
    files: List[Path] = field(default_factory=list)
    dirs: List[Path] = field(default_factory=list)

    def add_file(self, path: Path):
        if path.is_dir():
            self.dirs.append(path)
        elif path.is_file():
            self.files.append(path)
        else:
            # We ignore other types of files
            pass

    def to_dict(self):
        """
        Make it easier to render this object as JSON later on.
        Can be extracted to a standalone JSON converter.
        :return:
        """
        return {
            {
                "filename": str(self.base_path),
                "dirs": [str(directory) for directory in self.dirs],
                "files": [str(f) for f in self.files],
            }
        }


@dataclass
class DirListingRequest:
    base_path: Path


@dataclass
class DeleteFileRequest:
    file_path: Path


@dataclass
class RenameFileRequest:
    old_path: Path
    new_path: Path
