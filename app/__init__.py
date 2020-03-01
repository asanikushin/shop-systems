from app.common import CustomJSONEncoder

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os
import config

# создание экземпляра приложения
app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopmentConfig')
app.json_encoder = CustomJSONEncoder

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models.database import product
from app.handlers import products_v1, products_v2

app.register_blueprint(products_v1, url_prefix="/products")
app.register_blueprint(products_v2, url_prefix="/products/v2")
