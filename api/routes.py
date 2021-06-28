import asyncio
import datetime
import json
import random
from functools import wraps

import sanic.response
from bson.json_util import dumps
from sanic import Blueprint
from sanic_openapi import swagger_blueprint
from umongo.frameworks.motor_asyncio import WrappedCursor

from api.ml import DetectPhase
from database.entities import User, Complex, Event, Marker, GeographicLocation


async def check_request_for_authorization_status(request):
    cookie = request.cookies.get("logged")
    user = await User.find_one({"salt": cookie})
    if user:
        return True
    else:
        return False


async def check_request_for_usertype(request):
    user = await User.find_one({"salt": request.cookies.get("logged")})
    if not user:
        return False

    return user.usertype


def authorized_type(f):
    @wraps(f)
    async def decorated_function(request, *args, **kwargs):
        # run some method that checks the request
        # for the client's type
        usertype = await check_request_for_usertype(request)

        if usertype:
            # the user exists.
            # run the handler method and return the response
            request.args["usertype"] = [usertype]
            response = await f(request, *args, **kwargs)
            return response
        else:
            # the user does not exist.
            return sanic.response.json({'ok': False, "description": "No such user exist"}, 403)

    return decorated_function


def authorized(f):
    @wraps(f)
    async def decorated_function(request, *args, **kwargs):
        # run some method that checks the request
        # for the client's authorization status
        is_authorized = await check_request_for_authorization_status(request)

        if is_authorized:
            # the user is authorized.
            # run the handler method and return the response
            response = await f(request, *args, **kwargs)
            return response
        else:
            # the user is not authorized.
            return sanic.response.json({'ok': False, "description": "Not autherized"}, 403)

    return decorated_function


async def initialize_routes(app):
    auth_blueprint = Blueprint("Authentication", url_prefix="/auth")

    app.blueprint(auth_blueprint)
    app.blueprint(swagger_blueprint)

    @app.route("/")
    async def handle(request):
        return sanic.response.json({"ok": True, "description": "Everything should work now!"})

    @app.get("/login")
    async def handle(request):
        user = await User.find_one({"username": request.args.get("username")})
        if not user:
            response = sanic.response.json({"ok": False, "description": "No such user exists"})
            return response
        user_pass = hash(str(user.password))
        request_pass = hash(str(request.args.get("password")))
        if str(user_pass) == str(request_pass):
            response = sanic.response.json({"ok": True, "usertype": str(user.usertype)})
            response.cookies["logged"] = user.salt
        else:
            response = sanic.response.json({"ok": False, "description": "Invalid password"})
        return response

    @app.post("/register")
    async def handle(request):
        does_user_exist = await User.find_one({"username": request.json["username"]})
        if not does_user_exist:
            user_salt = str(random.getrandbits(128))
            user = User(username=request.json["username"], password=request.json["password"], salt=user_salt)
            await user.commit()
            response = sanic.response.json({"ok": True})
            response.cookies["logged"] = user_salt
            return response
        else:
            return sanic.response.json({"ok": False, "description": "This username already exists"})

    @app.get("/complex/get")
    async def handle(request):
        try:
            cursor: WrappedCursor = Complex.find({})
            complexes = []
            obj = True
            while obj:
                try:
                    obj: Complex = await cursor.next()
                    if obj:
                        complexes.append(obj)
                except:
                    obj = False
            response = sanic.response.json({"ok": True, "data": complexes}, dumps=dumps)
            return response
        except:
            return sanic.response.json({"ok": False, "data": dumps([])})

    @app.websocket("/complex/fetch")
    async def feed(request, ws):
        await ws.recv()
        while True:
            try:
                cursor: WrappedCursor = Complex.find({})
                complexes = []
                obj = True
                while obj:
                    try:
                        obj: Complex = await cursor.next()
                        if obj:
                            complexes.append(dumps(obj))
                    except:
                        obj = False
                response = sanic.response.json({"ok": True, "data": complexes})
                await ws.send(response)
            except:
                await ws.send(sanic.response.json({"ok": False, "data": []}))
            await asyncio.sleep(20)

    @app.route("/supervisor")
    @authorized
    @authorized_type
    async def handle(request):
        if request.args.get("usertype") == "supervisor":
            return sanic.response.json({"ok": True, "description": "You are supervisor!"})
        else:
            return sanic.response.json({"ok": False, "description": "You are not a supervisor!"})

    @app.route("/worker")
    @authorized
    @authorized_type
    async def handle(request):
        if request.args.get("usertype") == "worker":
            return sanic.response.json({"ok": True, "description": "You are worker!"})
        else:
            return sanic.response.json({"ok": False, "description": "You are not a worker!"})

    @app.post("/worker/register-event")
    async def handle(request):
        try:
            req = request.json
            comp: Complex = await Complex.find_one({"title": req["complex_title"]})
            file = req["event_file"]
            results = DetectPhase.detect(file)
            event_type, event_start, event_end, probability = results[0]
            event_type = {"1_faza": "Однофазное КЗ", "2_faza": "Двухфазное КЗ", "3_faza": "Трёхфазное КЗ"}[event_type]
            event_start = int(event_start*1000000)
            event_end = int(event_end*1000000)
            event_start = datetime.datetime(2020, 10, 25, 9, 10, 15, event_start)
            event_end = datetime.datetime(2020, 10, 25, 9, 10, 15, event_end)
            event_length = event_end - event_start
            event = Event(title=req["event_title"],
                          description=req["event_description"],
                          event_type=event_type,
                          event_start=event_start.__str__(),
                          event_end=event_end.__str__(),
                          event_length=event_length.microseconds,
                          probability=probability)
            comp.events.append(event)
            await comp.commit()
            return sanic.response.json({"ok": True})
        except:
            return sanic.response.json({"ok": False})

    @app.post("/worker/add-marker")
    async def handle(request):
        try:
            req = request.json
            event: Event = await Event.find_one({"title": req["event_title"]})
            marker = Marker(title=req["marker_title"],
                            geographic_location=GeographicLocation(latitude=req["marker_latitude"],
                                                                   longitude=req["marker_longitude"]))
            event.markers.append(marker)
            await event.commit()
            return sanic.response.json({"ok": True})
        except:
            return sanic.response.json({"ok": False})
