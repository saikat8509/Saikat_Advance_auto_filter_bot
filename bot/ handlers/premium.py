from pyrogram import filters, Client
from pyrogram.types import Message
from datetime import datetime, timedelta
from bot.utils.database import add_premium_user, get_user_plan, remove_expired_premium_users
from config import PREMIUM_PLANS, TRIAL_DURATION_HOURS
from bot.utils.buttons import premium_main_buttons


@Client.on_message(filters.command("myplan") & filters.private)
async def my_plan(client, message: Message):
    user_id = message.from_user.id
    plan = await get_user_plan(user_id)

    if plan:
        remaining = plan["expiry_date"] - datetime.utcnow()
        text = f"✅ **You are a Premium User!**\n\n**Plan:** {plan['label']}\n**Expires In:** {remaining.days} days"
    else:
        text = "❌ You are not a premium user.\n\nUse /premium to explore premium plans."

    await message.reply_text(
        text,
        reply_markup=premium_main_buttons(),
        quote=True
    )


@Client.on_message(filters.command("addpremium") & filters.user([int]))  # Replace [int] with actual admin user_ids
async def add_premium(client, message: Message):
    if len(message.command) < 3:
        return await message.reply("Usage: /addpremium <user_id> <days>")

    try:
        user_id = int(message.command[1])
        days = int(message.command[2])
        plan = PREMIUM_PLANS.get(str(days))
        if not plan:
            return await message.reply("Invalid days. Choose from plan keys: " + ", ".join(PREMIUM_PLANS.keys()))

        expiry_date = datetime.utcnow() + timedelta(days=days)
        await add_premium_user(user_id, expiry_date, plan["label"])
        await message.reply(f"✅ Added premium user {user_id} for {days} days.")
    except Exception as e:
        await message.reply(f"Error: {e}")


@Client.on_message(filters.command("trial") & filters.private)
async def trial_user(client, message: Message):
    user_id = message.from_user.id
    plan = await get_user_plan(user_id)

    if plan:
        await message.reply("❌ You already have a plan. Trials are for new users only.")
        return

    expiry_date = datetime.utcnow() + timedelta(hours=TRIAL_DURATION_HOURS)
    await add_premium_user(user_id, expiry_date, label="🆓 Trial Plan")
    await message.reply("✅ Trial activated successfully!\nEnjoy premium for a limited time.")


@Client.on_message(filters.command("clearexpired") & filters.user([int]))  # Replace [int] with actual admin user_ids
async def clear_expired(client, message: Message):
    count = await remove_expired_premium_users()
    await message.reply(f"✅ Cleared {count} expired premium users.")
