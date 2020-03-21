import constants
from auth.storage import Storage

from utils import create_error_with_status

from flask import jsonify, request, current_app


def sing_in():
    try:
        email = request.json["email"]
        password = request.json["password"]
    except KeyError:
        status = constants.statuses["user"]["missingData"]
        body = create_error_with_status(status, "missing user data")
        current_app.logger.warn("Not enough data for sing-in")
        return jsonify(body), constants.responses[status]

    current_app.logger.info(f"Sing in for {email}")

    access, refresh, status = Storage.create_session(email, password)
    http_status = constants.responses[status]

    if status == constants.statuses["tokens"]["created"]:
        body = dict(status=status, accessToken=access, refreshToken=refresh)
    elif status == constants.statuses["user"]["wrongPassword"]:
        body = create_error_with_status(status, "wrong password for email {{email}}", email=email)
    else:  # status == constants.statuses["user"]["noUser"]:
        body = create_error_with_status(status, "No user for email {{email}}", email=email)
    return jsonify(body), http_status
