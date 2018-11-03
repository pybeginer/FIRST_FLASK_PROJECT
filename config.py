import redis


class Config(object):

    SECRET_KEY = "jdskgrrkjkk"
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/flask_project"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 86400 * 7


class ConfigDeve(Config):
    DEBUG = True


class ConfigRun(Config):
    DEBUG = False

config_dic = {
    "develop":ConfigDeve,
    "run":ConfigRun
}