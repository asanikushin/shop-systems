import constants
from shop.storage import memoryStorage

from flask import jsonify, request


def add_product():
    new_id, status = memoryStorage.add_product(**request.json)
    http_status = constants.responses[status]

    if status == constants.statuses["product"]["created"]:
        body = jsonify(id=new_id, status=status)
    else:
        body = "missing product data"
    return body, http_status
