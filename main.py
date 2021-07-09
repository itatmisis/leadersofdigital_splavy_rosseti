#!/usr/bin/env python3
from asyncio import get_event_loop

from api import routes
from database import database
from server import app


async def setup():
    await database.initialize_database(app)
    await routes.initialize_routes(app)


if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(setup())
    app.run(host='wirer.xyz', port=8000, ssl=dict(cert="/etc/letsencrypt/live/wirer.xyz/fullchain.pem", key="/etc/letsencrypt/live/wirer.xyz/privkey.pem"))
