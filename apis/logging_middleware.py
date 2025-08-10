# logging_middleware.py
import time
from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


def register_logging_hooks(app, logger):
    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def log_request(response):
        now = time.time()
        duration = round(now - getattr(request, 'start_time', now), 4)
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        method = request.method
        path = request.path
        status = response.status_code
        user = None
        try:
            verify_jwt_in_request(optional=True)
            user = get_jwt_identity()
        except Exception:
            user = None

        log_params = {
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(now)),
            "remote_addr": ip,
            "method": method,
            "path": path,
            "status": status,
            "duration": duration,
            "user": user,
            "request_id": request.headers.get('X-Request-ID'),
        }
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                log_params["request_json"] = request.get_json()
            except Exception:
                log_params["request_json"] = None
        logger.info("request", extra=log_params)
        return response
