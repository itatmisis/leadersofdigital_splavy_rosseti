from umongo import fields, EmbeddedDocument, MotorAsyncIOInstance

from database.entities.misc import Marker
from server import app

instance: MotorAsyncIOInstance = app.config["LAZY_UMONGO"]



@instance.register
class Event(EmbeddedDocument):
    title = fields.StringField(allow_none=True)
    description = fields.StringField(allow_none=True)
    markers = fields.ListField(fields.EmbeddedField(Marker))
