import os

basedir = os.path.abspath(os.path.dirname(__file__))


def process_uri(uri):

    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    return uri


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = process_uri(os.environ['DATABASE_URL'])


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True



