import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    # Secret Key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # API Keys
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    # Database Config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost/writegpt'
    SQLALCHEMY_TRACK_MODIFICATIONS = False