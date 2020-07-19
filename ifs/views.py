from flask import render_template, Blueprint, current_app

fs = Blueprint("fs", "fs")


@fs.route("/")
def get_listing():
    current_app.logger.warning("sample message")
    return render_template("index.html")


@fs.route("/")
def delete_file():
    pass


@fs.route("/")
def rename_file():
    pass
