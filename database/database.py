import datetime
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

    complex_1 = entities.Complex(title="Подстанция АРЗ-13", location="Деревня Постное",
                                 geographic_location=entities.GeographicLocation(latitude=43.725034,
                                                                                 longitude=45.634656),
                                 events=[entities.Event(title="Однофазное КЗ", event_type="однофазное КЗ",
                                                        event_start=datetime.datetime(2020, 5, 17),
                                                        event_end=datetime.datetime(2020, 5, 18),
                                                        probability=0.95,
                                                        markers=[entities.Marker(title="Срыв дерева от ветра",
                                                                                 geographic_location=entities.GeographicLocation(
                                                                                     latitude=43.780533,
                                                                                     longitude=45.333403))])])
    complex_2 = entities.Complex(title="Подстанция ПОС-49", location="Хутор Капустино",
                                 geographic_location=entities.GeographicLocation(latitude=43.779496,
                                                                                 longitude=45.335599))

    # await complex_1.commit()
    # await complex_2.commit()

    logging.debug("Collections were initialized!")
