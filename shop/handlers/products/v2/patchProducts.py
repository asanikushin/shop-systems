import constants
from shop.storage import DBStorage

from utils import create_error_with_status

from flask import jsonify, request


def patch_product(prod_id=None):
    prod_id = prod_id or request.args.get("id")
    product, status = DBStorage.update_product(prod_id, request.method, **request.json)
    http_status = constants.responses[status]

    if status == constants.statuses["product"]["modified"]:
        body = dict(product=product, status=status)
    elif status == constants.statuses["product"]["notExists"]:
        body = create_error_with_status(status, "no such product id: {{ID}}", ID=prod_id)
    elif status == constants.statuses["product"]["missingData"]:
        body = create_error_with_status(status, "missing product data")
    else:  # status == constants.statuses["product"]["replacingID"]:
        body = create_error_with_status(status, "replacing product ID")
    return jsonify(body), http_status
