from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
print(path.join(basedir, 'variables.env'))
load_dotenv(path.join(basedir, 'variables.env'))

class Config(object):
    FLASK_ENV = 'production'
    STATIC_FOLDER = 'static'

    SQLALCHEMY_DATABASE_URI = 'postgresql://oktzbogwjcorkm:3529cfa5ca57bd1d863a1325a5ce3eb067f50b97f828b2ac295c0e9f9862072a@ec2-63-34-97-163.eu-west-1.compute.amazonaws.com:5432/d5lqcrvilccju2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    FLASK_APP = 'wsgi.py'

    SECRET_KEY = 'jhg876jhgkhdgsjkfg0878076879sdjhfshliuhHUILHG87XOS'