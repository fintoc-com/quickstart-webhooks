import hmac
import json
import os
from functools import wraps
from hashlib import sha256

from flask import request
from werkzeug.wrappers import Response

from app import app


WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")


def verify_signature(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if WEBHOOK_SECRET is None:  # No verification, proceed
            app.logger.info("Webhook secret not configured")
            return function(*args, **kwargs)

        # Get timestamp and event signature from request header
        signature = request.headers.get("Fintoc-Signature")
        timestamp, event_signature = [
            x.split("=")[1] for x in signature.split(",")
        ]
        app.logger.info(
            f"Validating with timestamp {timestamp} and signature {event_signature}"
        )

        # Create validation message
        message = (
            "{}.{}".format(
                timestamp,
                request.get_data().decode("utf-8"),
            )
        )
        encoded_secret = WEBHOOK_SECRET.encode('utf-8')
        encoded_message = message.encode('utf-8')
        hmac_object = hmac.new(encoded_secret, msg=encoded_message, digestmod=sha256)
        computed_signature = hmac_object.hexdigest()

        # Validate signature
        valid_signature = hmac.compare_digest(computed_signature, event_signature)

        if valid_signature:
            app.logger.info("Valid signature, proceding with the request")
            return function(*args, **kwargs)

        app.logger.error("Signature invalid")
        return Response(u'Signature Invalid', mimetype= 'text/plain', status=401)
    return wrapper
