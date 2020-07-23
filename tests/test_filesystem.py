import os
import tempfile
from pathlib import Path
import time

import pytest

from filesystem.fs import RealFileSystemService, FileSystemException
from filesystem.models import DeleteFileRequest, RenameFileRequest, DirListingRequest


@pytest.fixture()
def temporary_dir():
    with tempfile.TemporaryDirectory() as td:
        yield td


@pytest.fixture()
def nonexisting_file() -> Path:
    f = Path(f"nonexistingfile{time.time_ns()}")
    yield f
    if f.exists():
        os.remove(f)


@pytest.fixture()
def filesystem(temporary_dir):
    yield RealFileSystemService(root_path=Path(temporary_dir))


def test_real_fs_should_return_empty_directory(filesystem):
    result = filesystem.get_dir_list(DirListingRequest(Path(".")))
    assert not result


def test_real_fs_system_should_block_absolute_urls(filesystem):
    with pytest.raises(FileSystemException):
        filesystem.get_dir_list(DirListingRequest(Path("/test")))


def test_real_fs_should_block_urls_outside_root(filesystem):
    with pytest.raises(FileSystemException):
        filesystem.get_dir_list(DirListingRequest(Path("../../test")))


def test_real_fs_should_return_files(temporary_dir, filesystem):
    with tempfile.TemporaryDirectory(
        dir=temporary_dir
    ) as testdir, tempfile.NamedTemporaryFile(dir=temporary_dir) as testfile:
        dirlist = filesystem.get_dir_list(DirListingRequest(Path(".")))
        assert Path(testdir).resolve() in dirlist.dirs
        assert Path(testfile.name).resolve() in dirlist.files


def test_real_fs_delete_existing_file_should_succeed(temporary_dir, filesystem):
    with tempfile.NamedTemporaryFile(dir=temporary_dir, delete=False) as testfile:
        assert Path(testfile.name).exists()
        print(f"\n{testfile.name=}\n{temporary_dir=}")
        filesystem.delete_file(DeleteFileRequest(Path(Path(testfile.name).name)))
        assert not Path(testfile.name).exists()


def test_real_fs_delete_nonexisting_file_should_fail(filesystem, nonexisting_file):
    with pytest.raises(FileSystemException):
        assert not nonexisting_file.exists()
        filesystem.delete_file(DeleteFileRequest(nonexisting_file))


def test_real_fs_rename_nonexisting_file_should_fail(filesystem, nonexisting_file):
    with pytest.raises(FileSystemException):
        target = Path("anything")
        assert not target.exists()
        filesystem.rename_file(RenameFileRequest(nonexisting_file, target))


def test_real_fs_rename_existing_target_file_should_fail(
    filesystem, temporary_dir, nonexisting_file
):
    with tempfile.NamedTemporaryFile(dir=temporary_dir, delete=False) as target_file:
        simplified_path = Path(target_file.name).relative_to(temporary_dir)
        with pytest.raises(FileSystemException):
            filesystem.rename_file(RenameFileRequest(nonexisting_file, simplified_path))


def test_real_fs_rename_valid_should_succeed(filesystem, temporary_dir):
    with tempfile.NamedTemporaryFile(dir=temporary_dir, delete=False) as source_file:
        simplified_source = Path(source_file.name).relative_to(temporary_dir)
        target_file = Path("thisfiledoesnotexist")
        filesystem.rename_file(RenameFileRequest(simplified_source, target_file))
        assert (temporary_dir / target_file).exists()
