import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:////{basedir}/app.db'
    CELERY_BROKER = 'redis://localhost:32768/0'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
