import os

from flask import Flask

from ifs.views import fs_blueprint


def initialize_app(config_object_path=None, config_envvars=None):
    app = Flask(__name__)
    if config_object_path:
        app.config.from_object(config_object_path)
    if config_envvars:
        app.config.from_envvar(config_envvars)
    app.register_blueprint(fs_blueprint, url_prefix="/fs")
    if not app.debug:
        import logging
        from logging.handlers import TimedRotatingFileHandler

        # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
        file_handler = TimedRotatingFileHandler(
            os.path.join(app.config["LOG_DIR"], "ifs.log"), "midnight"
        )
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(
            logging.Formatter("<%(asctime)s> <%(levelname)s> %(message)s")
        )
        app.logger.addHandler(file_handler)
    return app
