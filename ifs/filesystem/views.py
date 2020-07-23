from pathlib import Path

import flask
from flask import Blueprint, current_app, jsonify, request

from ifs.fs import RealFileSystemService, FileSystemException
from ifs.models import DirListingRequest, DeleteFileRequest, RenameFileRequest

fs_blueprint = Blueprint("fs", "fs")


@fs_blueprint.record
def set_app_fs_service(setup_state: flask.blueprints.BlueprintSetupState):
    base_path_str = setup_state.app.config.get("BASE_PATH", "")
    if not base_path_str:
        raise ValueError(
            "Initialized without BASE_PATH variable for the FileSystem module"
        )
    base_path = Path(base_path_str).resolve()
    if not base_path.exists() or not base_path.is_dir():
        raise ValueError(
            f"BASE_PATH [{base_path_str}] should reflect an existing directory"
        )
    setup_state.app.fs_service = RealFileSystemService(base_path)


@fs_blueprint.route("/", methods=["GET"])
@fs_blueprint.route("/<path:listing_path>", methods=["GET"])
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
    except FileSystemException as e:
        return jsonify({"success": False, "error": e.args[0]})
    return jsonify({"success": True, "fs": result.to_dict()})


@fs_blueprint.route("/<path:path>", methods=["DELETE"])
def delete_file(path):
    current_app.logger.info("This is the path received: [%s]", path)
    try:
        delete_request = DeleteFileRequest(Path(path))
        current_app.fs_service.delete_file(delete_request)
        return jsonify(success=True)
    except FileSystemException as e:
        return jsonify(success=False, error=e.args[0])


@fs_blueprint.route("/<path:path>", methods=["PUT"])
def rename_file(path):
    current_app.logger.info("This is the path received: [%s]", path)
    try:
        new_path = Path(request.json.get("name", ""))
        rename_request = RenameFileRequest(Path(path), Path(new_path))
        current_app.fs_service.rename_file(rename_request)
        return jsonify(success=True)
    except FileSystemException as e:
        return jsonify(success=False, error=e.args[0])
