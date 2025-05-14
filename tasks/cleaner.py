import asyncio
from datetime import datetime, timedelta
from database.users import user_collection
from pyrogram import Client
from config import BOT_TOKEN, API_ID, API_HASH

bot = Client("CleanerBot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

async def notify_user(user_id: int, message: str):
    try:
        await bot.send_message(user_id, message)
    except Exception:
        pass  # Ignore if user blocked bot or chat is unavailable

async def remove_expired_premium_users():
    if not user_collection:
        return

    now = datetime.utcnow()
    soon = now + timedelta(days=1)

    # Notify users whose premium expires in 1 day
    notify_soon = user_collection.find({
        "is_premium": True,
        "premium_expiry": {
            "$gte": now,
            "$lt": soon
        }
    })

    async for user in notify_soon:
        await notify_user(
            user["user_id"],
            "⚠️ Your premium access will expire in 24 hours. Renew it soon to keep enjoying ad-free direct downloads!"
        )

    # Remove expired premium and notify
    expired = user_collection.find({
        "is_premium": True,
        "premium_expiry": {"$lte": now}
    })

    count = 0
    async for user in expired:
        user_collection.update_one(
            {"user_id": user["user_id"]},
            {"$set": {"is_premium": False}}
        )
        await notify_user(
            user["user_id"],
            "❌ Your premium access has expired. Use /buy to renew and regain full access."
        )
        count += 1

    if count:
        print(f"[CRON] Removed and notified {count} expired users.")


async def start_cleaner(interval_minutes: int = 60):
    await bot.start()
    while True:
        await remove_expired_premium_users()
        await asyncio.sleep(interval_minutes * 60)
