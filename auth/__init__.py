from utils import CustomJSONEncoder

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import auth.config

import logging
import os

db = SQLAlchemy()
migrate = Migrate()

logging.basicConfig(
    format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def create_app(config_class="auth.config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(os.environ.get('FLASK_ENV') or config_class)
    app.json_encoder = CustomJSONEncoder

    db.init_app(app)
    migrate.init_app(app, db)

    from auth.handlers.singup import register_user
    from auth.handlers.singin import sing_in
    from auth.handlers.refresh import refresh_tokens
    from auth.handlers.validate import validate

    app.add_url_rule("/register", "register", register_user, methods=['POST'])
    app.add_url_rule("/singin", "sing_in", sing_in, methods=['POST'])
    app.add_url_rule("/refresh", "refresh", refresh_tokens, methods=['POST'])
    app.add_url_rule("/validate", "validate", validate, methods=['POST'])

    from swagger_ui import api_doc
    working_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(working_dir, '../swagger.yaml')
    api_doc(app, config_path=config_path, url_prefix='/swagger', title='API doc', editor=True)

    log = logging.getLogger(app.name)
    log.setLevel(app.config["LOG_LEVEL"])

    return app
