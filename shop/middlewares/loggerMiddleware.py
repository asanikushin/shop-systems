from werkzeug.wrappers import Request, Response


class LoggerMiddleware:
    def __init__(self, app, logger):
        self.app = app
        self.logger = logger

    def __call__(self, environ, start_response):
        if environ["REQUEST_METHOD"] in ["POST", "DELETE", "PUT", "PATCH"]:
            request = Request(environ, shallow=True)
            self.logger.debug(request.headers)
        return self.app(environ, start_response)
