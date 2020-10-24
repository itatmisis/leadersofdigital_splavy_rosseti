import asyncio
from functools import wraps
import random

import sanic.response
from bson.json_util import dumps
import json
from sanic import Blueprint
from sanic_openapi import swagger_blueprint
from umongo.frameworks.motor_asyncio import WrappedCursor

from database.entities import User, Complex


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
            response = sanic.response.json({"ok": True})
            response.cookies["logged"] = user.salt
        else:
            response = sanic.response.json({"ok": False})
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
            complexes = dumps(complexes)
            response = sanic.response.json({"ok": True, "data": complexes})
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


