from utils import CustomJSONEncoder

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(os.environ.get('FLASK_ENV') or config_class)
    app.json_encoder = CustomJSONEncoder

    db.init_app(app)
    migrate.init_app(app, db)

    from shop.models.database import product
    from shop.handlers import products_v1, products_v2

    app.register_blueprint(products_v1, url_prefix="/products/v1")
    app.register_blueprint(products_v2, url_prefix="/products")
    from swagger_ui import api_doc
    working_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(working_dir, '../swagger.yaml')
    api_doc(app, config_path=config_path, url_prefix='/swagger', title='API doc', editor=True)

    return app
