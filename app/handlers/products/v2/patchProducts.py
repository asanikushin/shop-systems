from app import constants
from app.storage import DBStorage

from flask import jsonify, request


def patch_product(prod_id=None):
    prod_id = prod_id or request.args.get("id")
    print(prod_id)
    product, status = DBStorage.update_product(prod_id, request.method, **request.json)
    http_status = constants.responses[status]

    if status == constants.statuses["product"]["modified"]:
        body = jsonify(product=product, status=status)
    elif status == constants.statuses["product"]["notExists"]:
        body = f"no such product id: {prod_id}"
    elif status == constants.statuses["product"]["missingData"]:
        body = "missing product data"
    else:  # status == constants.statuses["product"]["replacingID"]:
        body = f"replacing product ID"
    return body, http_status
