import tempfile
from pathlib import Path

from ifs.models import DirectoryListing


def test_directory_listing_should_detect_files():
    listing = DirectoryListing(Path())
    with tempfile.NamedTemporaryFile() as tf:
        listing.add_file(Path(tf.name))
        assert listing.files
        assert not listing.dirs


def test_directory_listing_should_detect_directories():
    listing = DirectoryListing(Path())
    with tempfile.TemporaryDirectory() as tf:
        listing.add_file(Path(tf))
        assert listing.dirs
        assert not listing.files
