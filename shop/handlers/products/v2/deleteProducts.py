import constants
from shop.storage import DBStorage

from utils import create_error_with_status

from flask import jsonify, request


def delete_product(prod_id=None):
    prod_id = prod_id or request.args.get("id")
    product, status = DBStorage.delete_product(prod_id)
    http_status = constants.responses[status]

    if status == constants.statuses["product"]["deleted"]:
        body = dict(product=product, status=status)
    else:
        body = create_error_with_status(status, "no such product id: {{ID}}", ID=prod_id)
    return jsonify(body), http_status
