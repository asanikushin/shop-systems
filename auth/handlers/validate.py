import constants
from auth.storage import Storage

from utils import create_error_with_status

from flask import jsonify, request, current_app


def validate():
    token = request.json["token"]

    current_app.logger.info(f"Validate token")
    current_app.logger.debug(f"Access token value {token}")

    body, status = Storage.check_token(token)
    http_status = constants.responses[status]

    if status == constants.statuses["tokens"]["accessOk"]:
        body = dict(status=status, value=body)
    else:  # status == constants.statuses["tokens"]["accessTokenExpired"]:
        body = create_error_with_status(status, "Access token expired", error=body)

    return jsonify(body), http_status
