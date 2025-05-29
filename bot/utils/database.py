from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
from datetime import datetime, timedelta

client = AsyncIOMotorClient(MONGO_DB_URI)
db = client.autofilter_bot

# === COLLECTIONS ===
users_col = db.users
searches_col = db.searches
premium_col = db.premium
referrals_col = db.referrals

# === USER FUNCTIONS ===
async def add_user(user_id: int):
    await users_col.update_one({"_id": user_id}, {"$setOnInsert": {"joined": datetime.utcnow()}}, upsert=True)

async def total_users() -> int:
    return await users_col.count_documents({})

# === PREMIUM FUNCTIONS ===
async def is_premium_user(user_id: int) -> bool:
    user = await premium_col.find_one({"_id": user_id})
    if user and "expiry" in user:
        return datetime.utcnow() < user["expiry"]
    return False

async def count_premium_users() -> int:
    return await premium_col.count_documents({"expiry": {"$gt": datetime.utcnow()}})

async def count_trial_users() -> int:
    return await premium_col.count_documents({"trial": True})

async def add_premium_user(user_id: int, duration_days: int, is_trial=False):
    expiry = datetime.utcnow() + timedelta(days=duration_days)
    await premium_col.update_one(
        {"_id": user_id},
        {"$set": {"expiry": expiry, "trial": is_trial}},
        upsert=True
    )

# === REFERRAL FUNCTIONS ===
async def add_referral(referrer_id: int, referred_id: int):
    await referrals_col.insert_one({
        "referrer": referrer_id,
        "referred": referred_id,
        "timestamp": datetime.utcnow()
    })

async def total_referred_users(referrer_id: int) -> int:
    return await referrals_col.count_documents({"referrer": referrer_id})

async def total_referral_count() -> int:
    return await referrals_col.count_documents({})

# === SPELLING / SIMILAR SEARCH ===
async def get_similar_queries(query: str) -> list:
    # Basic regex based search
    cursor = searches_col.find({"query": {"$regex": query, "$options": "i"}}).limit(10)
    results = []
    async for doc in cursor:
        results.append(doc["query"])
    return results

async def log_search(user_id: int, query: str):
    await searches_col.insert_one({
        "user_id": user_id,
        "query": query,
        "timestamp": datetime.utcnow()
    })
