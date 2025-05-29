from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URI

client = AsyncIOMotorClient(MONGODB_URI)
db = client["autofilter_bot"]
users_collection = db["users"]


class Database:
    def __init__(self):
        self.collection = users_collection

    async def add_user(self, user_id: int, referred_by: int = None):
        existing = await self.collection.find_one({"user_id": user_id})
        if existing:
            return

        user_data = {
            "user_id": user_id,
            "is_premium": False,
            "is_trial": False,
            "referred_by": referred_by,
            "referral_count": 0,
        }

        await self.collection.insert_one(user_data)

        # Increment referral count for the referrer if valid
        if referred_by:
            await self.collection.update_one(
                {"user_id": referred_by},
                {"$inc": {"referral_count": 1}}
            )

    async def total_users(self) -> int:
        return await self.collection.count_documents({})

    async def count_premium_users(self) -> int:
        return await self.collection.count_documents({"is_premium": True})

    async def count_trial_users(self) -> int:
        return await self.collection.count_documents({"is_trial": True})

    async def total_referred_users(self) -> int:
        return await self.collection.count_documents({"referred_by": {"$ne": None}})

    async def total_referral_count(self) -> int:
        # Sum up all referral_count fields across all users
        pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$referral_count"}}}
        ]
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0

    async def set_premium(self, user_id: int, is_premium: bool = True):
        await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"is_premium": is_premium}},
            upsert=True
        )

    async def set_trial(self, user_id: int, is_trial: bool = True):
        await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"is_trial": is_trial}},
            upsert=True
        )

    async def get_user(self, user_id: int):
        return await self.collection.find_one({"user_id": user_id})

    async def get_referral_count(self, user_id: int) -> int:
        data = await self.get_user(user_id)
        return data.get("referral_count", 0) if data else 0


# Export database instance
db = Database()
