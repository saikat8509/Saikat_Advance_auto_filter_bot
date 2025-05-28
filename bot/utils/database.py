from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI, LOG_CHANNEL
import asyncio

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_DB_URI)
        self.db = self.client['autofilter_bot_db']
        self.users = self.db['users']
        self.files = self.db['files']
        self.referrals = self.db['referrals']
        self.premium = self.db['premium']
        self.logs = self.db['logs']

    # User management
    async def add_user(self, user_id: int, username: str = None):
        user = await self.users.find_one({"user_id": user_id})
        if not user:
            await self.users.insert_one({"user_id": user_id, "username": username, "joined_at": asyncio.get_event_loop().time()})
            return True
        return False

    async def is_premium(self, user_id: int) -> bool:
        premium_user = await self.premium.find_one({"user_id": user_id})
        if premium_user:
            from datetime import datetime
            expire_ts = premium_user.get("expires_at")
            if expire_ts and expire_ts > datetime.utcnow().timestamp():
                return True
            else:
                # Expired premium - remove
                await self.premium.delete_one({"user_id": user_id})
        return False

    async def add_premium(self, user_id: int, duration_days: int):
        from datetime import datetime, timedelta
        expire_time = datetime.utcnow() + timedelta(days=duration_days)
        await self.premium.update_one(
            {"user_id": user_id},
            {"$set": {"expires_at": expire_time.timestamp()}},
            upsert=True
        )

    # Referral system
    async def add_referral(self, referrer_id: int, referred_id: int):
        ref = await self.referrals.find_one({"referrer_id": referrer_id, "referred_id": referred_id})
        if not ref:
            await self.referrals.insert_one({"referrer_id": referrer_id, "referred_id": referred_id, "timestamp": asyncio.get_event_loop().time()})
            return True
        return False

    async def count_referrals(self, referrer_id: int) -> int:
        count = await self.referrals.count_documents({"referrer_id": referrer_id})
        return count

    # File tracking (e.g. downloads, searches)
    async def increment_file_download(self, file_id: str):
        await self.files.update_one({"file_id": file_id}, {"$inc": {"downloads": 1}}, upsert=True)

    async def increment_file_search(self, file_id: str):
        await self.files.update_one({"file_id": file_id}, {"$inc": {"searches": 1}}, upsert=True)

    # Log events to a channel or DB
    async def log_event(self, event_type: str, data: dict):
        log_entry = {"type": event_type, "data": data, "timestamp": asyncio.get_event_loop().time()}
        await self.logs.insert_one(log_entry)
        # You may add code here to forward log to LOG_CHANNEL if desired.

db = Database()
