# database/user_data.py

from datetime import datetime, timedelta
from database.connection import get_active_db

db = get_active_db()
users_collection = db.users


async def add_user(user_id, full_name, username=None):
    user = await users_collection.find_one({"user_id": user_id})
    if not user:
        data = {
            "user_id": user_id,
            "name": full_name,
            "username": username,
            "joined_at": datetime.utcnow(),
            "premium": False,
            "premium_expires": None,
            "referrals": 0,
            "search_history": [],
            "banned": False
        }
        await users_collection.insert_one(data)


async def is_premium(user_id):
    user = await users_collection.find_one({"user_id": user_id})
    if user and user.get("premium"):
        if user.get("premium_expires") and user["premium_expires"] > datetime.utcnow():
            return True
        else:
            await remove_premium(user_id)
    return False


async def make_premium(user_id, days):
    expiry = datetime.utcnow() + timedelta(days=days)
    await users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"premium": True, "premium_expires": expiry}},
        upsert=True
    )


async def remove_premium(user_id):
    await users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"premium": False, "premium_expires": None}}
    )


async def add_referral(referrer_id):
    await users_collection.update_one(
        {"user_id": referrer_id},
        {"$inc": {"referrals": 1}},
        upsert=True
    )


async def get_referral_count(user_id):
    user = await users_collection.find_one({"user_id": user_id})
    return user.get("referrals", 0) if user else 0


async def ban_user(user_id):
    await users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"banned": True}},
        upsert=True
    )


async def unban_user(user_id):
    await users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"banned": False}},
        upsert=True
    )


async def is_banned(user_id):
    user = await users_collection.find_one({"user_id": user_id})
    return user.get("banned", False) if user else False


async def log_search(user_id, query):
    await users_collection.update_one(
        {"user_id": user_id},
        {"$push": {"search_history": {"query": query, "time": datetime.utcnow()}}},
        upsert=True
    )


async def get_top_users(limit=10):
    cursor = users_collection.find({"referrals": {"$gt": 0}}).sort("referrals", -1).limit(limit)
    return await cursor.to_list(length=limit)


async def get_total_users():
    return await users_collection.count_documents({})
