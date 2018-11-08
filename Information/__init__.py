import logging
from logging.handlers import RotatingFileHandler

import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect,generate_csrf
from config import config_dic

logging.basicConfig(level=logging.DEBUG)
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
file_log_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_log_handler)

db = SQLAlchemy()
redis_store = None


def create_app(config_style):
    app = Flask(__name__)
    Config = config_dic.get(config_style)
    app.config.from_object(Config)
    db.init_app(app)
    global redis_store
    redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)
    Session(app)

    CSRFProtect(app)
    @app.after_request
    def create_csrf(resp):
        csrf_token = generate_csrf()
        resp.set_cookie("csrf_token1", csrf_token)
        return resp
    from Information.news import news_bluprt
    app.register_blueprint(news_bluprt)

    from Information.utils.common import class_filter
    app.add_template_filter(class_filter, "classtrans")

    from Information.passport import passport_blueprint
    app.register_blueprint(passport_blueprint)

    from Information.HomePage import blueprint_objt
    app.register_blueprint(blueprint_objt)

    return app



