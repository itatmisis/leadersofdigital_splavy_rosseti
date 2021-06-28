from sanic import Sanic
from sanic_cors import CORS

from umongo import MotorAsyncIOInstance

app = Sanic(__name__)
CORS(app)

app.config.update({
    "MONGODB_DATABASE": "rosseti",
    "MONGODB_URI": "mongodb+srv://user:pass@cluster0.2cssf.mongodb.net/rosseti?retryWrites=true&w=majority",
    "LAZY_UMONGO": MotorAsyncIOInstance(),
})
