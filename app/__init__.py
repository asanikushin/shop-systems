from app.common import CustomJSONEncoder

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

import os
import config

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Simple shtop REST API"
    }
)

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
app.register_blueprint(swagger, url_prefix=SWAGGER_URL)
