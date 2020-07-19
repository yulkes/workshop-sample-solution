import pytest

from ifs import app_init


@pytest.fixture()
def flask_app():
    return app_init.initialize_app("tests.settings_for_test")


@pytest.fixture()
def app_test_client(flask_app):
    return flask_app.test_client()


def test_app_should_return_listing_for_empty_path(app_test_client):
    result = app_test_client.get("/fs/")
    result_json = result.json

    assert result_json.get("success")
    assert result_json.get("fs")
