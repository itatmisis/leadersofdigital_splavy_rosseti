import asyncio
from functools import wraps

import sanic.response
from bson.json_util import dumps
from sanic import Blueprint
from sanic_openapi import swagger_blueprint
from umongo.frameworks.motor_asyncio import WrappedCursor

from database.entities import User, Complex


async def check_request_for_authorization_status(request):
    cookie = str(request.cookies.get("logged"))
    user = await User.find_one({"username": request.args.get("username")})
    if not user:
        return False

    hashed_pass = str(hash(user.password))
    flag = (cookie == hashed_pass)

    return flag


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
            response.cookies["logged"] = str(hash(str(request.args["password"])))
        else:
            response = sanic.response.json({"ok": False})
        return response

    @app.post("/register")
    async def handle(request):
        does_user_exist = await User.find_one({"username": request.json["username"]})
        if not does_user_exist:
            user = User(username=request.json["username"], password=request.json["password"])
            await user.commit()
            response = sanic.response.json({"ok": True})
            response.cookies["logged"] = str(hash(request.json["password"]))
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
                        complexes.append(dumps(obj))
                except:
                    obj = False
            response = sanic.response.json({"ok": True, "data": complexes})
            return response
        except:
            return sanic.response.json({"ok": False, "data": []})

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
