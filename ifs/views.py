from pathlib import Path

from flask import Blueprint, current_app, jsonify, request

from ifs.fs import RealFileSystemService
from ifs.models import DirListingRequest
from models import DeleteFileRequest, RenameFileRequest

fs = Blueprint("fs", "fs")


@fs.record
def set_app_fs_service():
    base_path_str = current_app.config.get("BASE_PATH", "")
    if not base_path_str:
        raise ValueError(
            "Initialized without BASE_PATH variable for the FileSystem module"
        )
    base_path = Path(base_path_str).resolve()
    if not base_path.exists() or not base_path.is_dir():
        raise ValueError(
            f"BASE_PATH [{base_path_str}] should reflect an existing directory"
        )
    current_app.fs_service = RealFileSystemService(base_path)


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
    current_app.logger.info("This is the path received: [%s]", listing_path)
    try:
        dir_list_request = DirListingRequest(Path(listing_path))
        result = current_app.fs_service.get_dir_list(dir_list_request)
    except ValueError as e:
        return jsonify({"success": False, "error": e.args[0]})
    return jsonify({"success": True, "fs": result.to_dict()})


@fs.route("/<path:path>", methods=["DELETE"])
def delete_file(path):
    current_app.logger.info("This is the path received: [%s]", path)
    try:
        delete_request = DeleteFileRequest(Path(path))
        current_app.fs_service.delete_file(delete_request)
        return jsonify(success=True)
    except ValueError as e:
        return jsonify(success=False, error=e.args[0])


@fs.route("/<path:path>", methods=["PUT"])
def rename_file(path):
    current_app.logger.info("This is the path received: [%s]", path)
    try:
        new_path = Path(request.json.get("name", ""))
        rename_request = RenameFileRequest(Path(path), Path(new_path))
        current_app.fs_service.rename_file(rename_request)
        return jsonify(success=True)
    except ValueError as e:
        return jsonify(success=False, error=e.args[0])
