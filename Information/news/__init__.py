
from flask import Blueprint

news_bluprt = Blueprint("news_bluprt", __name__, url_prefix="/news")

from . import views
