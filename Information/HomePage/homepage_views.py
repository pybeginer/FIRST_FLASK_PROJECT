from . import blueprint_objt


@blueprint_objt.route("/")
def homepage():
    return "HomePage for test"