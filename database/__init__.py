# database/__init__.py

import logging
from bot.config import MONGO_URIS
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# List of MongoDB URIs to support fallback
clients = []
databases = []
active_index = 0

# Load all MongoDB URIs and initialize clients
for index, uri in enumerate(MONGO_URIS):
    try:
        client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        db = client.AutoFilterDB
        databases.append(db)
        clients.append(client)
        LOGGER.info(f"✅ MongoDB [{index}] connected.")
    except Exception as e:
        LOGGER.warning(f"❌ MongoDB [{index}] failed: {e}")
        continue

if not databases:
    raise Exception("🚫 No valid MongoDB connections found.")

# Accessor: Get current active DB
def get_active_db():
    return databases[active_index]

# Optional: Manually switch DB if needed
def switch_db(index: int):
    global active_index
    if index < len(databases):
        active_index = index
        LOGGER.info(f"✅ Switched to MongoDB [{index}]")
    else:
        LOGGER.warning(f"❌ Invalid MongoDB index: {index}")

# DB connectivity test (used in main.py)
async def test_connection():
    try:
        info = await get_active_db().command("ping")
        return info.get("ok") == 1.0
    except Exception as e:
        LOGGER.error(f"⚠️ DB Test failed: {e}")
        return False

