# import os
# from dotenv import load_dotenv

# load_dotenv()  # load environment variables from .env if it exists.

# class Config(object):
#     """Base Config Object"""
#     DEBUG = False
#     SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
#     UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed



import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-later"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(os.path.dirname(basedir), "app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(basedir, "static", "uploads")