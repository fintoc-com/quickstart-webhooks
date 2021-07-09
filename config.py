import os
basedir = os.path.abspath(os.path.dirname(__file__))


DATABASE_URL = os.environ.get("DATABASE_URL")
DB_USERNAME = os.environ.get("DB_USERNAME", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "postgres")

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SQLALCHEMY_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        DATABASE_URL or f"postgresql://"
        f"{DB_USERNAME}{':' if DB_PASSWORD else ''}"
        f"{DB_PASSWORD}@{DB_HOST}/"
        f"{DB_NAME}"
    )
