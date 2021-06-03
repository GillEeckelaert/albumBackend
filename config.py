from os import environ, path

basedir = path.abspath(path.dirname(__file__))

class Config(object):
    FLASK_ENV = 'production'
    STATIC_FOLDER = 'static'

    SQLALCHEMY_DATABASE_URI = environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    FLASK_APP = 'wsgi.py'

    SECRET_KEY = 'jhg876jhgkhdgsjkfg0878076879sdjhfshliuhHUILHG87XOS'