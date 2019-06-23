import os

from flask import Flask
from flask_migrate import Migrate

from config import Config
from users.models import db
from users.views import bp as users_bp
from celery import Celery

celery_ = Celery(__name__, broker=Config.CELERY_BROKER)


def create_app(overide_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)
    if overide_config is not None:
        app.config.from_mapping(overide_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)

    app.register_blueprint(users_bp)
    celery_.conf.update(app.config)

    return app
