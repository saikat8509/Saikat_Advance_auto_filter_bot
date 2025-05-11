# handlers/premium.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.user_data import get_user_data, upgrade_to_premium, get_referral_count, set_referral, is_premium
from config import ADMINS, PREMIUM_PRICE, REFERRAL_REWARD, TRIAL_PREMIUM_HOURS
from datetime import datetime, timedelta

@Client.on_message(filters.command("buy") & filters.private)
async def buy_plan(client, message: Message):
    text = (
        "**💳 Premium Plans**\n\n"
        f"➤ 1 Month Plan: {PREMIUM_PRICE} INR\n"
        f"➤ Payment via: UPI, Paytm, GPay\n\n"
        "📩 After payment, send the screenshot to the admin.\n"
        "✅ You'll be upgraded within minutes.\n\n"
        "🎁 Use your referral to earn FREE premium!"
    )
    buttons = [[
        InlineKeyboardButton("💬 Contact Admin", url="https://t.me/YourSupportAdmin"),
        InlineKeyboardButton("🎁 My Referral", callback_data="my_refer")
    ]]
    await message.reply(text, reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_message(filters.command("myplan") & filters.private)
async def my_plan(client, message: Message):
    user_id = message.from_user.id
    data = await get_user_data(user_id)
    if not data:
        await message.reply("❌ You're not registered. Try searching something first.")
        return

    if is_premium(data):
        expiry = data.get("premium_expiry")
        await message.reply(f"🌟 You are a premium user!\n\n⏳ Expires on: `{expiry}`")
    else:
        await message.reply("🆓 You are currently a free user.\nUpgrade to premium using /buy")


@Client.on_message(filters.command("refer") & filters.private)
async def referral_info(client, message: Message):
    user_id = message.from_user.id
    link = f"https://t.me/{(await client.get_me()).username}?start={user_id}"
    count = await get_referral_count(user_id)

    text = (
        "🎁 **Referral Program**\n\n"
        f"🔗 Your Referral Link:\n`{link}`\n\n"
        f"👥 Referrals Joined: {count}\n"
        f"💎 Earn {REFERRAL_REWARD} days premium per verified user!\n\n"
        "**Share with friends and earn rewards!**"
    )
    await message.reply(text)


@Client.on_message(filters.private & filters.regex(r"^/start (\d+)$"))
async def handle_referral(client, message: Message):
    referred_by = int(message.matches[0].group(1))
    user_id = message.from_user.id

    if referred_by == user_id:
        return await message.reply("❌ You can't refer yourself.")

    added = await set_referral(user_id, referred_by)
    if added:
        await message.reply("🎉 Welcome! You were referred successfully.\nCheck /refer for your own link.")
    else:
        await message.reply("✅ You're already referred or already a user!")


@Client.on_message(filters.command("trial") & filters.user(ADMINS))
async def give_trial(client, message: Message):
    if len(message.command) != 2:
        return await message.reply("Usage: `/trial user_id`", quote=True)

    user_id = int(message.command[1])
    expires = datetime.now() + timedelta(hours=TRIAL_PREMIUM_HOURS)
    await upgrade_to_premium(user_id, expires)
    await message.reply(f"✅ Trial given to `{user_id}` for {TRIAL_PREMIUM_HOURS} hours.")

    try:
        await client.send_message(user_id, f"🎁 You've received trial premium access for {TRIAL_PREMIUM_HOURS} hours!")
    except Exception:
        pass

