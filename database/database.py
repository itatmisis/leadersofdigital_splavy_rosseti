import logging

from motor.motor_asyncio import AsyncIOMotorClient
from sanic_mongodb_ext import MongoDbExtension

import database.entities as entities


async def initialize_database(app):
    MongoDbExtension(app)

    client = AsyncIOMotorClient(app.config['MONGODB_URI'])
    database = client[app.config['MONGODB_DATABASE']]
    lazy_umongo = app.config["LAZY_UMONGO"]
    lazy_umongo.init(database)

    logging.debug("Clearing collections...")
    await entities.User.ensure_indexes()
    logging.debug("User document was initialized...")

    await entities.Complex.ensure_indexes()
    logging.debug("Complex document was initialized...")

    logging.debug("Collections were initialized!")
