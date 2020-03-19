import constants
from auth.storage import Storage

from utils import create_error_with_status

from flask import jsonify, request, current_app


def register_user():
    email = request.json["email"]
    password = request.json["password"]

    current_app.logger.info(f"Sing up for {email}")

    status = Storage.add_user(email, password)
    http_status = constants.responses[status]

    if status == constants.statuses["user"]["created"]:
        body = dict(status=status, email=email)
    else:
        body = create_error_with_status(status, "email {{email}} is already registered", email=email)
    return jsonify(body), http_status
