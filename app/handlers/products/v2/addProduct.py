from app import constants
from app.storage import DBStorage

from app.common.errorResponse import create_error_with_status

from flask import jsonify, request


def add_product():
    new_id, status = DBStorage.add_product(**request.json)
    http_status = constants.responses[status]

    if status == constants.statuses["product"]["created"]:
        body = dict(id=new_id, status=status)
    else:
        body = create_error_with_status(status, "missing product data")
    return jsonify(body), http_status
