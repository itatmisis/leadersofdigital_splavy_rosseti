from umongo import fields, Document, MotorAsyncIOInstance

from database.entities.misc import GeographicLocation
from database.entities.event import Event

from server import app

instance: MotorAsyncIOInstance = app.config["LAZY_UMONGO"]


@instance.register
class Complex(Document):
    title = fields.StringField(required=True, allow_none=False)
    location = fields.StringField(required=True, allow_none=False)
    geographic_location = fields.EmbeddedField(GeographicLocation)
    events = fields.ListField(fields.EmbeddedField(Event))
