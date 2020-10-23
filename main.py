#!/usr/bin/env python3
from api import routes
from database import database
from server import app
from asyncio import get_event_loop


async def setup():
    await database.initialize_database(app)
    await routes.initialize_routes(app)


if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(setup())
    app.run(host='0.0.0.0', port=8000)
