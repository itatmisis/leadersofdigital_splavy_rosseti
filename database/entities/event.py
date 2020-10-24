from umongo import fields, EmbeddedDocument, MotorAsyncIOInstance

from database.entities.misc import Marker
from server import app

instance: MotorAsyncIOInstance = app.config["LAZY_UMONGO"]


@instance.register
class Event(EmbeddedDocument):
    title = fields.StringField(required=True, allow_none=False)
    description = fields.StringField(allow_none=True, default="")
    event_type = fields.StringField(required=True, allow_none=False)
    event_start = fields.DateTimeField(required=True, allow_none=False)
    event_end = fields.DateTimeField(required=True, allow_none=False)
    probability = fields.FloatField(required=True, allow_none=False)
    markers = fields.ListField(fields.EmbeddedField(Marker), allow_none=True, default=[])
