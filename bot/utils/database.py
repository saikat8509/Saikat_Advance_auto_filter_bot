import motor.motor_asyncio
from config import MONGO_DB_URI, DATABASE_CHANNEL_IDS

class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI)
        self.db = self.client["autofilter_bot_db"]

        # Collections
        self.users = self.db["users"]
        self.premium_users = self.db["premium_users"]
        self.trial_users = self.db["trial_users"]
        self.referrals = self.db["referrals"]
        self.files = self.db["files"]  # Example collection for indexed files

    # User management
    async def add_user(self, user_id: int):
        if not await self.users.find_one({"user_id": user_id}):
            await self.users.insert_one({"user_id": user_id})

    async def is_premium(self, user_id: int) -> bool:
        doc = await self.premium_users.find_one({"user_id": user_id})
        return bool(doc)

    async def add_premium_user(self, user_id: int, expires_at: int):
        await self.premium_users.update_one(
            {"user_id": user_id},
            {"$set": {"expires_at": expires_at}},
            upsert=True,
        )

    async def remove_premium_user(self, user_id: int):
        await self.premium_users.delete_one({"user_id": user_id})

    async def add_trial_user(self, user_id: int, expires_at: int):
        await self.trial_users.update_one(
            {"user_id": user_id},
            {"$set": {"expires_at": expires_at}},
            upsert=True,
        )

    async def remove_trial_user(self, user_id: int):
        await self.trial_users.delete_one({"user_id": user_id})

    # Referral management
    async def add_referral(self, referrer_id: int, referred_id: int):
        if not await self.referrals.find_one({"referred_id": referred_id}):
            await self.referrals.insert_one({
                "referrer_id": referrer_id,
                "referred_id": referred_id,
            })

    async def get_referral_count(self, referrer_id: int) -> int:
        return await self.referrals.count_documents({"referrer_id": referrer_id})

    # Statistics methods

    async def total_users(self) -> int:
        return await self.users.count_documents({})

    async def count_premium_users(self) -> int:
        return await self.premium_users.count_documents({})

    async def count_trial_users(self) -> int:
        return await self.trial_users.count_documents({})

    async def total_referred_users(self) -> int:
        return await self.referrals.count_documents({})

    async def total_referral_count(self) -> int:
        pipeline = [
            {"$group": {"_id": None, "total": {"$sum": 1}}}
        ]
        result = await self.referrals.aggregate(pipeline).to_list(length=1)
        if result:
            return result[0].get("total", 0)
        return 0

    # Example: files count in indexed channels
    async def count_files(self) -> int:
        return await self.files.count_documents({"channel_id": {"$in": DATABASE_CHANNEL_IDS}})

# Singleton instance of Database to be imported and used everywhere
db = Database()
