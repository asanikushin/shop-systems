import constants
from auth.storage import Storage

from utils import create_error_with_status

from flask import jsonify, request, current_app


def refresh_tokens():
    current_app.logger.info("Refresh tokens pair")
    try:
        token = request.json["token"]
    except KeyError:
        status = constants.statuses["tokens"]["missingData"]
        body = create_error_with_status(status, "No token get")
        current_app.logger.warn("No token for refreshment")
        return jsonify(body), constants.responses[status]

    current_app.logger.debug(f"Refresh token value {token}")

    access, refresh, status = Storage.update_session(token)
    http_status = constants.responses[status]

    if status == constants.statuses["tokens"]["created"]:
        body = dict(status=status, accessToken=access, refreshToken=refresh)
    elif status == constants.statuses["tokens"]["noSuchToken"]:
        body = create_error_with_status(status, "No information about token")
    else:  # status == constants.statuses["user"]["refreshExpired"]:
        body = create_error_with_status(status, "Refresh token expired")
    return jsonify(body), http_status
