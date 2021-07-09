"""This module includes every number model used inside the API."""

from sqlalchemy_json import mutable_json_type

from app import app, db


class Event(db.Model):

    """Models a Fintoc event."""

    __tablename__ = "event"

    id = db.Column(db.String, primary_key=True)
    object = db.Column(db.String())
    data = db.Column(mutable_json_type(dbtype=db.JSON, nested=True))
    type = db.Column(db.String())

    def __init__(self, event):
        self.id = event["id"]
        self.object = event["object"]
        self.data = event["data"]
        self.type = event["type"]

    def __repr__(self):
        return f"<Event - id {self.id}>"

    def serialize(self):
        """Generates the serialized view of the object."""
        return {
            "id": self.id,
            "object": self.object,
            "data": self.data,
            "type": self.type,
        }
