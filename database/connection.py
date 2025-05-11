# database/connection.py

import motor.motor_asyncio
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
import logging
import asyncio
import os

from config import MONGO_URIS, DB_NAME

logger = logging.getLogger(__name__)

mongo_clients = []
active_db = None


async def init_database():
    global mongo_clients, active_db

    for uri in MONGO_URIS:
        try:
            client = motor.motor_asyncio.AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
            await client.server_info()  # Test connection
            mongo_clients.append(client)
            db = client[DB_NAME]
            # Optional: perform test read to ensure it's writable
            await db.test.find_one()
            active_db = db
            logger.info(f"[DB] Connected to MongoDB: {uri}")
            break
        except (ServerSelectionTimeoutError, OperationFailure) as e:
            logger.warning(f"[DB] Connection failed for {uri}: {e}")
            continue

    if not active_db:
        logger.error("[DB] All MongoDB connections failed. Shutting down.")
        raise SystemExit("❌ Could not connect to any MongoDB instances.")


def get_active_db():
    if not active_db:
        raise Exception("Database not initialized yet. Call init_database() first.")
    return active_db
