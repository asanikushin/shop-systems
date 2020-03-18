from .addProduct import add_product
from .deleteProducts import delete_product
from .getProducts import get_product, get_products
from .patchProducts import patch_product

from flask import Blueprint

products = Blueprint("products_v2", __name__)

products.add_url_rule("/", "add_products", add_product, methods=['POST'])

products.add_url_rule("/<int:prod_id>", "delete_product", delete_product, methods=['DELETE'])

products.add_url_rule("/", "get_products", get_products, methods=["GET"])
products.add_url_rule("/<int:prod_id>", "get_product", get_product, methods=["GET"])

products.add_url_rule("/<int:prod_id>", "patch_product", patch_product, methods=['PATCH', 'PUT'])

