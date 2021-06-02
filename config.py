from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
print(path.join(basedir, 'variables.env'))
load_dotenv(path.join(basedir, 'variables.env'))

class Config(object):
    FLASK_ENV = 'production'
    STATIC_FOLDER = 'static'

    SQLALCHEMY_DATABASE_URI = 'postgres://mwwxexnafnvzoz:68f224a5e7b0476b7a9d4635fed7f3227359c0215dffa17a6baa7fb90b8a47f9@ec2-63-33-239-176.eu-west-1.compute.amazonaws.com:5432/dec7po8bqjh0qt'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    FLASK_APP = 'wsgi.py'

    SECRET_KEY = 'jhg876jhgkhdgsjkfg0878076879sdjhfshliuhHUILHG87XOS'