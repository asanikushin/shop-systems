import constants
from shop.storage import DBStorage

from utils import create_error_with_status

from flask import jsonify, request, current_app


def add_product():
    current_app.logger.info(f"Creating product by {request.environ['user_email']}")

    new_id, status = DBStorage.add_product(**request.json)
    http_status = constants.responses[status]

    if status == constants.statuses["product"]["created"]:
        body = dict(id=new_id, status=status)
    else:
        body = create_error_with_status(status, "missing product data")
    return jsonify(body), http_status
