import os
from flask import Flask
from .views import fs

app = Flask(__name__)
app.config.from_object("ifs.default_settings")
app.config.from_envvar("IFS_SETTINGS")

app.register_blueprint(fs, url_prefix="/fs")

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
