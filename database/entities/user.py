from umongo import Document, MotorAsyncIOInstance
from umongo.fields import StringField

from server import app

instance: MotorAsyncIOInstance = app.config["LAZY_UMONGO"]


@instance.register
class User(Document):
    username = StringField(required=True, allow_none=False, unique=True)
    password = StringField(required=True, allow_none=False)
    usertype = StringField(required=True, allow_none=False, default="worker")
    salt = StringField(required=True, unique=True, allow_none=False)
