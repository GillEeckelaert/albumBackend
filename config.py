from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
print(path.join(basedir, 'variables.env'))
load_dotenv(path.join(basedir, 'variables.env'))

class Config(object):
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True
    STATIC_FOLDER = 'static'

    SQLALCHEMY_DATABASE_URI = environ.get('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    FLASK_APP = environ.get('FLASK_APP')

    SECRET_KEY = environ.get('SECRET_KEY')