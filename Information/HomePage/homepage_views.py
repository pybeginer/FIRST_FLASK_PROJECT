from . import blueprint_objt
from flask import render_template,current_app


@blueprint_objt.route("/")
def homepage():
    return render_template("news/index.html")


@blueprint_objt.route("/favicon.ico")
def add_favi():
    return current_app.send_static_file("news/favicon.ico")