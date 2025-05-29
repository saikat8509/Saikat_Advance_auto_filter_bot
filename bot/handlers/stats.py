from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_USERNAME
from bot.utils.database import db


@Client.on_message(filters.command("stats") & filters.private)
async def bot_stats(client: Client, message: Message):
    user = message.from_user

    # Verify user is the owner
    if user.username != OWNER_USERNAME.replace("@", ""):
        return await message.reply("🚫 You are not authorized to use this command.")

    total_users = await db.total_users()
    premium_users = await db.count_premium_users()
    trial_users = await db.count_trial_users()
    referred_users = await db.total_referred_users()
    total_referrals = await db.total_referral_count()

    stats_msg = f"""📊 **Bot Usage Statistics**

👥 Total Users: `{total_users}`
💎 Premium Users: `{premium_users}`
🧪 Trial Users: `{trial_users}`
🔗 Users Referred: `{referred_users}`
📈 Total Referrals Used: `{total_referrals}`
"""

    await message.reply(stats_msg)

