from utils.errorResponse import create_error_with_status
import constants

from werkzeug.wrappers import Request, Response
import requests
import json


class AuthMiddleware:
    def __init__(self, app, base_app, logger):
        self.app = app
        self.base = base_app
        self.logger = logger

    def __call__(self, environ, start_response):
        request = Request(environ, shallow=True)
        if request.method in ["POST", "DELETE", "PUT", "PATCH"]:
            self.logger.info("Auth request")
            auth_url = self.base.config["AUTH_SERVICE_URI"] + "/validate"
            self.logger.debug(auth_url)
            auth = requests.post(auth_url, json={"token": request.headers["accessToken"]})

            self.logger.debug(str(auth.status_code) + str(auth.content))
            auth_status = auth.json()["status"]

            if auth_status != constants.statuses["tokens"]["accessOk"]:
                auth_error = auth.json()["error"]
                res = Response(json.dumps(create_error_with_status(0, auth_error)), mimetype="application/json",
                               status=constants.common_responses["No auth"])
                return res(environ, start_response)
            auth_email = auth.json()["value"]["email"]
            environ["user_email"] = auth_email

        return self.app(environ, start_response)
