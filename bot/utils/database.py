# bot/utils/database.py

import motor.motor_asyncio
from datetime import datetime, timedelta
from config import MONGO_URL, DATABASE_NAME

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

# === USERS ===

async def add_user(user_id, name):
    await db.users.update_one(
        {"_id": user_id},
        {"$set": {"name": name, "joined_at": datetime.utcnow()}},
        upsert=True,
    )

async def is_user_exist(user_id):
    user = await db.users.find_one({"_id": user_id})
    return bool(user)

async def get_all_users():
    return db.users.find()

# === PREMIUM ===

async def add_premium_user(user_id, plan_name, duration_days):
    expiry = datetime.utcnow() + timedelta(days=duration_days)
    await db.premium.update_one(
        {"_id": user_id},
        {"$set": {"plan": plan_name, "expires_at": expiry}},
        upsert=True,
    )

async def remove_premium_user(user_id):
    await db.premium.delete_one({"_id": user_id})

async def is_premium(user_id):
    user = await db.premium.find_one({"_id": user_id})
    if not user:
        return False
    if user.get("expires_at") < datetime.utcnow():
        await remove_premium_user(user_id)
        return False
    return True

async def get_premium_users():
    return db.premium.find()

# === REFERRALS ===

async def create_referral(user_id):
    await db.referrals.update_one(
        {"_id": user_id}, {"$setOnInsert": {"count": 0}}, upsert=True
    )

async def increase_referral(user_id):
    await db.referrals.update_one({"_id": user_id}, {"$inc": {"count": 1}})

async def get_referral_count(user_id):
    user = await db.referrals.find_one({"_id": user_id})
    return user["count"] if user else 0

# === URL SHORTENER TOKENS ===

async def save_user_token(user_id, token):
    await db.tokens.update_one({"_id": user_id}, {"$set": {"token": token}}, upsert=True)

async def get_user_token(user_id):
    data = await db.tokens.find_one({"_id": user_id})
    return data.get("token") if data else None

# === FILE INDEXING ===

async def add_file(file_id, file_name, file_caption, file_type, size, unique_id):
    await db.files.update_one(
        {"_id": unique_id},
        {
            "$set": {
                "file_id": file_id,
                "file_name": file_name,
                "caption": file_caption,
                "type": file_type,
                "size": size,
                "added_at": datetime.utcnow(),
            }
        },
        upsert=True,
    )

async def search_files(query):
    return db.files.find({"file_name": {"$regex": query, "$options": "i"}})

async def get_file(unique_id):
    return await db.files.find_one({"_id": unique_id})

# === TRENDING / POPULAR ===

async def increment_trending(query):
    await db.trending.update_one(
        {"query": query},
        {"$inc": {"count": 1}, "$set": {"last_used": datetime.utcnow()}},
        upsert=True,
    )

async def get_trending(limit=10):
    return db.trending.find().sort("count", -1).limit(limit)

async def increment_popular(file_id):
    await db.popular.update_one(
        {"file_id": file_id},
        {"$inc": {"downloads": 1}, "$set": {"last_download": datetime.utcnow()}},
        upsert=True,
    )

async def get_popular(limit=10):
    return db.popular.find().sort("downloads", -1).limit(limit)

# === FORCE SUBSCRIBE ===

async def set_required_channels(channels):
    await db.settings.update_one({"_id": "fsub"}, {"$set": {"channels": channels}}, upsert=True)

async def get_required_channels():
    data = await db.settings.find_one({"_id": "fsub"})
    return data.get("channels", []) if data else []

# === PLAN EXPIRY AUTO CHECK ===

async def clean_expired_premium():
    expired = await db.premium.delete_many({"expires_at": {"$lt": datetime.utcnow()}})
    return expired.deleted_count

# === STATS ===

async def get_stats():
    users = await db.users.count_documents({})
    premium = await db.premium.count_documents({})
    files = await db.files.count_documents({})
    trending = await db.trending.count_documents({})
    popular = await db.popular.count_documents({})
    return {
        "users": users,
        "premium": premium,
        "files": files,
        "trending": trending,
        "popular": popular,
    }
