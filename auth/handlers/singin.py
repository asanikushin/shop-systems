import constants
from auth.storage import Storage

from utils import create_error_with_status

from flask import jsonify, request


def sing_in():
    email = request.json["email"]
    password = request.json["password"]

    access, refresh, status = Storage.create_session(email, password)
    http_status = constants.responses[status]

    if status == constants.statuses["tokens"]["created"]:
        body = dict(status=status, accessToken=access, refreshToken=refresh)
    elif status == constants.statuses["user"]["wrongPassword"]:
        body = create_error_with_status(status, "wrong password for email {{email}}", email=email)
    else:  # status == constants.statuses["user"]["noUser"]:
        body = create_error_with_status(status, "No user for email {{email}}", email=email)
    return jsonify(body), http_status
