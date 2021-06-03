from os import environ, path

basedir = path.abspath(path.dirname(__file__))

databaseURL = environ['DATABASE_URL'].replace("postgres", "postgresql")

class Config(object):
    FLASK_ENV = 'production'
    STATIC_FOLDER = 'static'

    SQLALCHEMY_DATABASE_URI = databaseURL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    FLASK_APP = 'wsgi.py'

    SECRET_KEY = 'jhg876jhgkhdgsjkfg0878076879sdjhfshliuhHUILHG87XOS'