from app import constants
from app.storage import memoryStorage

from flask import jsonify, request


def delete_product(prod_id=None):
    prod_id = prod_id or request.args.get("id")
    product, status = memoryStorage.delete_product(prod_id)
    http_status = constants.responses[status]

    if status == constants.statuses["product"]["deleted"]:
        body = jsonify(product=product, status=status)
    else:
        body = f"no such product id: {prod_id}"
    return body, http_status
