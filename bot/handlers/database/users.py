import time
from datetime import datetime, timedelta
from pymongo import UpdateOne
from config import MONGO_DB, REF_BONUS_DAYS
from .db import get_collection

users_col = get_collection(MONGO_DB, "users")


# ------------------ USER MANAGEMENT ------------------

async def add_user(user_id: int, first_name: str, referrer_id: int = None):
    user = await users_col.find_one({"user_id": user_id})
    if user:
        await users_col.update_one({"user_id": user_id}, {
            "$set": {"first_name": first_name}
        })
    else:
        data = {
            "user_id": user_id,
            "first_name": first_name,
            "join_date": datetime.utcnow(),
            "is_banned": False,
            "is_premium": False,
            "premium_expiry": None,
            "referrer_id": referrer_id,
            "token_expiry": None
        }
        await users_col.insert_one(data)
        if referrer_id:
            await add_referral_bonus(referrer_id)


async def get_user(user_id: int):
    return await users_col.find_one({"user_id": user_id})


async def get_all_users():
    return users_col.find({"is_banned": False})


async def total_users_count():
    return await users_col.count_documents({})


# ------------------ PREMIUM MANAGEMENT ------------------

async def set_premium(user_id: int, days: int):
    expiry = datetime.utcnow() + timedelta(days=days)
    await users_col.update_one(
        {"user_id": user_id},
        {"$set": {"is_premium": True, "premium_expiry": expiry}}
    )


async def check_premium(user_id: int):
    user = await get_user(user_id)
    if not user:
        return False
    expiry = user.get("premium_expiry")
    if expiry and expiry > datetime.utcnow():
        return True
    await users_col.update_one(
        {"user_id": user_id},
        {"$set": {"is_premium": False, "premium_expiry": None}}
    )
    return False


async def expire_premium_users():
    now = datetime.utcnow()
    await users_col.update_many(
        {"is_premium": True, "premium_expiry": {"$lte": now}},
        {"$set": {"is_premium": False, "premium_expiry": None}}
    )


# ------------------ REFERRAL BONUS ------------------

async def add_referral_bonus(referrer_id: int):
    user = await get_user(referrer_id)
    if not user:
        return
    current_expiry = user.get("premium_expiry")
    bonus = timedelta(days=REF_BONUS_DAYS)
    if current_expiry and current_expiry > datetime.utcnow():
        new_expiry = current_expiry + bonus
    else:
        new_expiry = datetime.utcnow() + bonus
    await users_col.update_one(
        {"user_id": referrer_id},
        {"$set": {"is_premium": True, "premium_expiry": new_expiry}}
    )


# ------------------ TOKEN SYSTEM ------------------

async def activate_token(user_id: int):
    expiry = datetime.utcnow() + timedelta(hours=24)
    await users_col.update_one(
        {"user_id": user_id},
        {"$set": {"token_expiry": expiry}}
    )


async def check_token(user_id: int):
    user = await get_user(user_id)
    if not user:
        return False
    token_expiry = user.get("token_expiry")
    if token_expiry and token_expiry > datetime.utcnow():
        return True
    return False


# ------------------ BAN MANAGEMENT ------------------

async def ban_user(user_id: int):
    await users_col.update_one({"user_id": user_id}, {"$set": {"is_banned": True}})


async def unban_user(user_id: int):
    await users_col.update_one({"user_id": user_id}, {"$set": {"is_banned": False}})


async def is_banned(user_id: int):
    user = await get_user(user_id)
    return user.get("is_banned", False) if user else False


# ------------------ BROADCAST SUPPORT ------------------

async def get_user_ids_for_broadcast():
    return users_col.find({"is_banned": False}, {"user_id": 1})
