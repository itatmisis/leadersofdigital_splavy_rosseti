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

    es = datetime.datetime(2020, 5, 17, 20, 15, 10, 128)
    ee = datetime.datetime(2020, 5, 17, 20, 15, 10, 584)
    el: datetime.timedelta = ee - es

    complex_1 = entities.Complex(title="Подстанция АРЗ-13", location="Деревня Постное",
                                 geographic_location=entities.GeographicLocation(latitude=43.725034,
                                                                                 longitude=45.634656),
                                 events=[entities.Event(title="Однофазное КЗ", event_type="Однофазное КЗ",
                                                        event_start=es.__str__(),
                                                        event_end=ee.__str__(),
                                                        event_length=el.microseconds,
                                                        probability=1,
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
