import constants
from auth.storage import Storage

from utils import create_error_with_status

from flask import jsonify, request, current_app


def register_user():
    try:
        email = request.json["email"]
        password = request.json["password"]
    except KeyError:
        status = constants.statuses["user"]["missingData"]
        body = create_error_with_status(status, "missing user data")
        current_app.logger.warn("Not enough data for sing-up")
        return jsonify(body), constants.responses[status]

    current_app.logger.info(f"Sing up for {email}")

    status = Storage.add_user(email, password)
    http_status = constants.responses[status]

    if status == constants.statuses["user"]["created"]:
        body = dict(status=status, email=email)
    else:  # status == constants.statuses["user"]["emailUsed"]:
        body = create_error_with_status(status, "email {{email}} is already registered", email=email)
    return jsonify(body), http_status
