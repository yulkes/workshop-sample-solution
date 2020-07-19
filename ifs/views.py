from pathlib import Path

from flask import Blueprint, current_app, jsonify

from ifs.fs import RealFileSystemService
from ifs.models import DirListingRequest

fs = Blueprint("fs", "fs")


@fs.route("/<path:listing_path>")
def get_listing(listing_path):
    """
    Read the path parameter, make sure it's valid
    Pass to the filesystem service, receive result
    Return result as JSON in expected format
    :return: JSON that looks like
    ```
    {"success": true,
     "fs": {"filename": "<path from request>",
            "dirs": ["dir1", ...],
            "files": ["a", ...]}
    }
    ```
    """
    request = DirListingRequest(listing_path)
    fs = RealFileSystemService(Path("."))
    result = fs.get_dir_list(request)
    current_app.logger.warning("This is the path received: [%s]", listing_path)
    return jsonify({"success": "ok", "fs": result.to_dict()})


@fs.route("/<path:path>")
def delete_file(path):
    pass


@fs.route("/<path:path>")
def rename_file(path):
    # TODO: Get target path from body
    pass
