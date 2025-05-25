from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import datetime, timedelta
import asyncio

# Assuming you have a MongoDB or similar database instance imported as `db`
# Example: from bot.database import db
# db should have collections like 'users', 'search_logs', 'downloads', 'premium_users', 'referrals'

# Placeholder for your database object (Replace with your actual DB instance)
db = None  # TODO: replace with actual DB connection


# Helper: Format timedelta nicely
def format_timedelta(td: timedelta) -> str:
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0:
        parts.append(f"{seconds}s")
    return " ".join(parts) if parts else "0s"


@Client.on_message(filters.command("stats") & filters.user([123456789]))  # Replace with admin IDs list
async def stats_command(client: Client, message: Message):
    """
    Admin command to fetch bot usage statistics.
    Shows counts of users, searches, downloads, premium users, referrals, and uptime.
    """

    start_time = client.start_time if hasattr(client, "start_time") else datetime.utcnow()

    # Fetch total users count
    total_users = await db.users.count_documents({}) if db else "N/A"

    # Fetch total searches count
    total_searches = await db.search_logs.count_documents({}) if db else "N/A"

    # Fetch total downloads count
    total_downloads = await db.downloads.count_documents({}) if db else "N/A"

    # Fetch total premium users count
    total_premium = await db.premium_users.count_documents({}) if db else "N/A"

    # Fetch total referrals count (sum all referral entries)
    referrals_cursor = db.referrals.aggregate(
        [{"$group": {"_id": None, "total": {"$sum": "$count"}}}]
    ) if db else None
    total_referrals = 0
    if referrals_cursor:
        async for doc in referrals_cursor:
            total_referrals = doc.get("total", 0)

    # Calculate uptime
    uptime = datetime.utcnow() - start_time
    uptime_str = format_timedelta(uptime)

    # Compose statistics message
    stats_text = f"""
📊 **Bot Statistics**

👥 Total Users: `{total_users}`
🔍 Total Searches: `{total_searches}`
⬇️ Total Downloads: `{total_downloads}`
⭐️ Premium Users: `{total_premium}`
🔗 Total Referrals: `{total_referrals}`

⏳ Uptime: `{uptime_str}`

⚒️ Bot maintained by @Leazy_Boy
"""

    # Inline keyboard for stats navigation
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔄 Refresh", callback_data="stats_refresh"),
                InlineKeyboardButton("🏠 Home", callback_data="start_back_cb"),
            ]
        ]
    )

    await message.reply_text(stats_text, reply_markup=keyboard, parse_mode="md")


@Client.on_callback_query(filters.regex("^stats_refresh$"))
async def stats_refresh_callback(client: Client, callback_query: CallbackQuery):
    """
    Refresh the statistics message when user clicks refresh button.
    """

    start_time = client.start_time if hasattr(client, "start_time") else datetime.utcnow()

    total_users = await db.users.count_documents({}) if db else "N/A"
    total_searches = await db.search_logs.count_documents({}) if db else "N/A"
    total_downloads = await db.downloads.count_documents({}) if db else "N/A"
    total_premium = await db.premium_users.count_documents({}) if db else "N/A"

    referrals_cursor = db.referrals.aggregate(
        [{"$group": {"_id": None, "total": {"$sum": "$count"}}}]
    ) if db else None
    total_referrals = 0
    if referrals_cursor:
        async for doc in referrals_cursor:
            total_referrals = doc.get("total", 0)

    uptime = datetime.utcnow() - start_time
    uptime_str = format_timedelta(uptime)

    stats_text = f"""
📊 **Bot Statistics**

👥 Total Users: `{total_users}`
🔍 Total Searches: `{total_searches}`
⬇️ Total Downloads: `{total_downloads}`
⭐️ Premium Users: `{total_premium}`
🔗 Total Referrals: `{total_referrals}`

⏳ Uptime: `{uptime_str}`

⚒️ Bot maintained by @Leazy_Boy
"""

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔄 Refresh", callback_data="stats_refresh"),
                InlineKeyboardButton("🏠 Home", callback_data="start_back_cb"),
            ]
        ]
    )

    await callback_query.message.edit_text(stats_text, reply_markup=keyboard, parse_mode="md")
    await callback_query.answer("Stats refreshed!")


# Optionally you can add a /stats command for non-admin users with limited info or denial
@Client.on_message(filters.command("stats") & ~filters.user([123456789]))
async def stats_denied(client: Client, message: Message):
    await message.reply_text(
        "❌ You are not authorized to view the bot statistics.",
        quote=True
    )
