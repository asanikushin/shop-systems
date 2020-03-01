from app.handlers.products.v1.addProduct import add_product
from app.handlers.products.v1.deleteProducts import delete_product
from app.handlers.products.v1.getProducts import get_product, get_products
from app.handlers.products.v1.patchProducts import patch_product

from flask import Blueprint

products = Blueprint("products_v1", __name__)

products.add_url_rule("/add", "add_products", add_product, methods=['POST'])

products.add_url_rule("/delete_id", "delete_product", delete_product, methods=['DELETE'])

products.add_url_rule("/get", "get_products", get_products)
products.add_url_rule("/get_id", "get_product", get_product)

products.add_url_rule("/update_id", "patch_product", patch_product, methods=['PATCH', 'PUT'])

