from datetime import datetime, timedelta
from pymongo import MongoClient
from config import MONGO_DB_URIS

# Connect to all MongoDB URIs and choose the first one that's available
clients = []
user_collection = None

for uri in MONGO_DB_URIS:
    try:
        client = MongoClient(uri)
        client.admin.command('ping')  # Test connection
        db = client['autofilterbot']
        user_collection = db['users']
        break
    except Exception:
        continue


def add_user(user_id: int):
    if not user_collection:
        return
    if not user_collection.find_one({"user_id": user_id}):
        user_collection.insert_one({
            "user_id": user_id,
            "is_premium": False,
            "premium_expiry": None,
            "referred_by": None,
            "referrals": 0,
            "joined": datetime.utcnow(),
            "token_expiry": None
        })


def set_premium(user_id: int, days: int):
    if not user_collection:
        return
    expiry_date = datetime.utcnow() + timedelta(days=days)
    user_collection.update_one({"user_id": user_id}, {"$set": {
        "is_premium": True,
        "premium_expiry": expiry_date
    }})


def check_premium(user_id: int):
    if not user_collection:
        return False
    user = user_collection.find_one({"user_id": user_id})
    if user and user.get("is_premium"):
        if user.get("premium_expiry") and datetime.utcnow() < user["premium_expiry"]:
            return True
        else:
            user_collection.update_one({"user_id": user_id}, {"$set": {"is_premium": False}})
    return False


def set_token_validity(user_id: int, hours: int = 24):
    if not user_collection:
        return
    expiry = datetime.utcnow() + timedelta(hours=hours)
    user_collection.update_one({"user_id": user_id}, {"$set": {"token_expiry": expiry}})


def has_valid_token(user_id: int):
    if not user_collection:
        return False
    user = user_collection.find_one({"user_id": user_id})
    expiry = user.get("token_expiry") if user else None
    return expiry and datetime.utcnow() < expiry


def set_referral(user_id: int, referred_by: int):
    if not user_collection:
        return
    user = user_collection.find_one({"user_id": user_id})
    if user and not user.get("referred_by"):
        user_collection.update_one({"user_id": user_id}, {"$set": {"referred_by": referred_by}})
        user_collection.update_one({"user_id": referred_by}, {"$inc": {"referrals": 1}})


def get_referral_count(user_id: int):
    if not user_collection:
        return 0
    user = user_collection.find_one({"user_id": user_id})
    return user.get("referrals", 0) if user else 0


def get_user_info(user_id: int):
    if not user_collection:
        return None
    return user_collection.find_one({"user_id": user_id})

