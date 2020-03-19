import constants
from auth.storage import Storage

from utils import create_error_with_status

from flask import jsonify, request, current_app


def validate():
    current_app.logger.info(f"Validate token")
    try:
        token = request.json["token"]
    except KeyError:
        status = constants.statuses["tokens"]["missingData"]
        body = create_error_with_status(status, "No token get")
        current_app.logger.warn("No token for validation")
        return jsonify(body), constants.responses[status]

    current_app.logger.debug(f"Access token value {token}")

    body, status = Storage.check_token(token)
    http_status = constants.responses[status]

    if status == constants.statuses["tokens"]["accessOk"]:
        body = dict(status=status, value=body)
    elif status == constants.statuses["tokens"]["invalidToken"]:
        body = create_error_with_status(status, "Access token has invalid format", error=body)
    else:  # status == constants.statuses["tokens"]["accessTokenExpired"]:
        body = create_error_with_status(status, "Access token expired", error=body)

    return jsonify(body), http_status
