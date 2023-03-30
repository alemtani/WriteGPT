import logging
import openai
import os

from config import Config
from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler, SMTPHandler

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    openai.api_key = app.config['OPENAI_API_KEY']

    from app.errors import errors
    app.register_blueprint(errors)
    from app.prompters import prompters
    app.register_blueprint(prompters, url_prefix='/api')
    from app.tokens import tokens
    app.register_blueprint(tokens, url_prefix='/api')
    from app.stories import stories
    app.register_blueprint(stories, url_prefix='/api')
    from app.fake import fake
    app.register_blueprint(fake)
    
    return app