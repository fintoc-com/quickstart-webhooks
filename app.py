import os
import config
from logging.config import dictConfig
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Logs configuration
dictConfig({
    "version": 1,
    "formatters": {
        "console": {
            "format": "[%(asctime)s] [%(levelname)s] %(module)s: %(message)s"
        },
        "file": {
            "format": ("[%(asctime)s] [%(levelname)s] %(pathname)s - "
                       "line %(lineno)d: \n%(message)s\n")
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "console"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.getenv("LOG_FILE", default="webhooks.log"),
            "formatter": "file"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
})


app = Flask(__name__)

app.config.from_object(config.Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from events import Event
from middleware import verify_signature


@app.route("/webhook", methods=["POST"])
@verify_signature
def webhook():
    """Receives the Fintoc webhooks."""
    try:
        app.logger.info("POST request to webhook action")
        data = request.get_json(force=True)

        existing_event = Event.query.filter_by(id=data["id"]).first()

        if existing_event:
            app.logger.info(f"Event with id {data['id']} already exists")
            return jsonify({
                "success": False,
                "message": f"Event with id {data['id']} already exists",
            }), 200

        event = Event(event=data)

        # Save Event on the database
        db.session.add(event)
        db.session.commit()

        app.logger.info(
            f"Event type {event.type} generated with id {event.id}"
        )

        return jsonify({
            "success": True,
            "id": event.id,
            "type": event.type,
        }), 200

    except Exception as err:
        app.logger.error(err)
        return jsonify({"success": False}), 500

@app.route("/events", methods=["GET"])
def get_events():
    """Get every saved event."""
    try:
        app.logger.info("GET request to get_events action")

        events = Event.query.all()
        app.logger.info(f"Returning {len(events)} events on the HTTP response.")

        return jsonify([x.serialize() for x in events]), 200
    except Exception as err:
        app.logger.error(err)
        return jsonify({"success": False}), 500
