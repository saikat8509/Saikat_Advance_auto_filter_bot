from pyrogram import Client, filters
from pyrogram.types import Message
from config import ADMINS, PREMIUM_PLANS
from bot.utils.database import (
    add_premium_user,
    remove_premium_user,
    get_user_plan,
    set_user_plan,
    get_all_users,
)
from datetime import datetime, timedelta
from bot.utils.broadcast import broadcast_message


@Client.on_message(filters.command("addpremium") & filters.user(ADMINS))
async def add_premium_cmd(_, message: Message):
    if len(message.command) < 3:
        return await message.reply("Usage: /addpremium <user_id> <plan_days>")
    try:
        user_id = int(message.command[1])
        plan_days = int(message.command[2])
        expiry_date = datetime.utcnow() + timedelta(days=plan_days)
        await set_user_plan(user_id, True, expiry_date)
        await message.reply(f"✅ Premium granted to `{user_id}` for {plan_days} days.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")


@Client.on_message(filters.command("removepremium") & filters.user(ADMINS))
async def remove_premium_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /removepremium <user_id>")
    try:
        user_id = int(message.command[1])
        await set_user_plan(user_id, False, None)
        await message.reply(f"🗑️ Premium removed for `{user_id}`.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")


@Client.on_message(filters.command("myplan"))
async def myplan_cmd(_, message: Message):
    user_id = message.from_user.id
    plan = await get_user_plan(user_id)
    if plan and plan["is_premium"]:
        expires = plan["expires_at"]
        expires_str = expires.strftime("%Y-%m-%d %H:%M:%S") if expires else "Unknown"
        await message.reply(f"💎 You are a premium user!\n🕒 Expires on: `{expires_str}`")
    else:
        await message.reply("⚠️ You are not a premium user.\nBuy one using the PREMIUM MEMBERSHIP button.")


@Client.on_message(filters.command("users") & filters.user(ADMINS))
async def total_users(_, message: Message):
    users = await get_all_users()
    await message.reply(f"👥 Total Users: `{len(users)}`")


@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast_cmd(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")
    
    await message.reply("📣 Broadcasting...")
    total, success, failed = await broadcast_message(message.reply_to_message)
    await message.reply(
        f"✅ Broadcast complete\n\nTotal: {total}\n✅ Success: {success}\n❌ Failed: {failed}"
    )
