from flask import Blueprint
from Information import db


blueprint_objt = Blueprint("homepage", __name__)

from . import homepage_views

