# bot/utils/expiry_checker.py

import asyncio
from datetime import datetime
from database.users import get_all_users, remove_expired_premium
from config import LOG_CHANNEL_ID

async def premium_expiry_checker(bot):
    while True:
        now = datetime.utcnow()
        expired_users = remove_expired_premium()

        if expired_users and LOG_CHANNEL_ID:
            for user in expired_users:
                await bot.send_message(
                    LOG_CHANNEL_ID,
                    f"⚠️ Premium Expired\n\n"
                    f"👤 User ID: `{user['user_id']}`\n"
                    f"⏰ Expired at: `{user['premium_expiry']}`"
                )

        await asyncio.sleep(43200)  # 12 hours
