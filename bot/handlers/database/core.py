# database/core.py

import os
import logging
import motor.motor_asyncio
from datetime import datetime, timedelta
from pymongo.errors import ServerSelectionTimeoutError
from config import MONGO_URIS, SEARCH_LOG_EXPIRE_HOURS, TOKEN_VALIDITY_HOURS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ⚙️ Initialize clients for each MongoDB URI
db_clients = []
for uri in MONGO_URIS:
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Test connection
        db_clients.append(client)
        logger.info(f"Connected to MongoDB: {uri}")
    except ServerSelectionTimeoutError:
        logger.warning(f"Failed to connect to MongoDB: {uri}")

# 🚨 Exit if no DB is available
if not db_clients:
    raise Exception("❌ No MongoDB URI is available!")

# Function to dynamically pick the next available database for indexing
def get_index_db():
    return db_clients[0]['autofilter_db']  # Optionally use logic to pick based on load

# Core DB used for global settings, logs, users, groups, premium info
global_db = db_clients[0]['autofilter_db']
files_collection = get_index_db().files
search_logs = global_db.search_logs
token_collection = global_db.token_verified


# 📦 MongoDB stats and indexing
async def get_mongo_stats():
    stats = []
    for client in db_clients:
        try:
            server_status = await client.admin.command("serverStatus")
            db = client.get_default_database()
            file_count = await db.files.count_documents({})
            stats.append({
                "uri": str(client.address),
                "storage_used_mb": round(server_status["wiredTiger"]["cache"]["bytes currently in the cache"] / 1024 / 1024, 2),
                "objects_indexed": file_count
            })
        except Exception as e:
            stats.append({
                "uri": "Connection Failed",
                "storage_used_mb": 0,
                "objects_indexed": 0,
                "error": str(e)
            })
    return stats

async def get_indexed_file_count():
    total = 0
    for client in db_clients:
        try:
            db = client.get_default_database()
            total += await db.files.count_documents({})
        except:
            continue
    return total


# 🔍 Search logs for Trending & Most Searched
async def log_search_term(term: str, user_id: int):
    await search_logs.insert_one({
        "term": term.lower(),
        "user_id": user_id,
        "timestamp": datetime.utcnow()
    })

async def get_top_searched_terms(limit=10):
    time_threshold = datetime.utcnow() - timedelta(hours=SEARCH_LOG_EXPIRE_HOURS)
    pipeline = [
        {"$match": {"timestamp": {"$gte": time_threshold}}},
        {"$group": {"_id": "$term", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    results = await search_logs.aggregate(pipeline).to_list(length=limit)
    return [{"term": r["_id"], "count": r["count"]} for r in results]

async def clear_search_logs():
    time_threshold = datetime.utcnow() - timedelta(hours=SEARCH_LOG_EXPIRE_HOURS)
    await search_logs.delete_many({"timestamp": {"$lt": time_threshold}})


# ✅ Shortener Token Verification
async def add_token_user(user_id: int):
    await token_collection.update_one(
        {"user_id": user_id},
        {"$set": {"expires_at": datetime.utcnow() + timedelta(hours=TOKEN_VALIDITY_HOURS)}},
        upsert=True
    )

async def is_token_verified(user_id: int):
    doc = await token_collection.find_one({"user_id": user_id})
    if doc and doc.get("expires_at") > datetime.utcnow():
        return True
    return False

async def clear_token_verification():
    await token_collection.delete_many({"expires_at": {"$lt": datetime.utcnow()}})

