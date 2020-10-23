from umongo import fields, EmbeddedDocument, MotorAsyncIOInstance

from server import app

instance: MotorAsyncIOInstance = app.config["LAZY_UMONGO"]



@instance.register
class GeographicLocation(EmbeddedDocument):
    latitude = fields.FloatField(required=True, allow_none=False)
    longitude = fields.FloatField(required=True, allow_none=False)


@instance.register
class Marker(EmbeddedDocument):
    title = fields.StringField(required=True, allow_none=False)
    geographical_location = fields.EmbeddedField(GeographicLocation, allow_none=False)
