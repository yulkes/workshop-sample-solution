from pathlib import Path

from flask import Blueprint, current_app, jsonify

from ifs.fs import RealFileSystemService
from ifs.models import DirListingRequest

fs = Blueprint("fs", "fs")


@fs.route("/", methods=["GET"])
@fs.route("/<path:listing_path>", methods=["GET"])
def get_listing(listing_path=Path(".")):
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
    current_app.logger.warning("This is the path received: [%s]", listing_path)
    try:
        request = DirListingRequest(Path(listing_path))
        fs_service = RealFileSystemService(Path("."))
        result = fs_service.get_dir_list(request)
    except ValueError as e:
        return jsonify({"success": False, "error": e.args[0]})
    return jsonify({"success": True, "fs": result.to_dict()})


@fs.route("/<path:path>", methods=["DELETE"])
def delete_file(path):
    pass


@fs.route("/<path:path>", methods=["PUT"])
def rename_file(path):
    # TODO: Get target path from body
    pass
