import constants
from auth.storage import Storage

from utils import create_error_with_status

from flask import jsonify, request


def validate():
    token = request.json["token"]
    body, status = Storage.check_token(token)
    http_status = constants.responses[status]

    if status == constants.statuses["tokens"]["accessExpired"]:
        body = create_error_with_status(status, "Access token expired", error=body)

    return jsonify(body), http_status
