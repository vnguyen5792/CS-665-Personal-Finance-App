from flask import Flask

from config import Config
from .extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

# Import models so SQLAlchemy knows about them before creating the database
    from app import models
    from .routes import main

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app