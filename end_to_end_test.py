"""
This end-to-end test should run when the service is up and running in Docker.
Its expectations are based on the directory structure created in the Dockerfile.
"""
import logging

import requests

SERVICE_BASE_PATH = "http://localhost:5000/fs/"


def end_to_end_test():

    logging.debug("Testin: Initial dir list")
    dir_list_response = requests.get(SERVICE_BASE_PATH)
    assert dir_list_response.ok
    dir_list = dir_list_response.json()
    assert dir_list.get("success")
    start_filesystem = dir_list.get("fs", {})
    assert set(start_filesystem.get("dirs")) == {"a1", "a2", "a3"}
    assert set(start_filesystem.get("files")) == {"f1", "f2", "f3"}

    logging.debug("Testing File deletion")
    delete_response = requests.delete(SERVICE_BASE_PATH + "f1")
    assert delete_response.ok
    assert set(requests.get(SERVICE_BASE_PATH).json()["fs"]["files"]) == {"f2", "f3"}

    logging.debug("Testing: Moving a file")
    rename_response = requests.put(
        SERVICE_BASE_PATH + "f2", json={"name": "a1/new_name"}
    )
    assert rename_response.ok
    assert set(requests.get(SERVICE_BASE_PATH).json()["fs"]["files"]) == {"f3"}
    assert "new_name" in requests.get(SERVICE_BASE_PATH + "a1").json()["fs"]["files"]

    # Success!
    logging.info("Everything finished successfully")


if __name__ == "__main__":
    end_to_end_test()
