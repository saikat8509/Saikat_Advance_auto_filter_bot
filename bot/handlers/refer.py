# bot/handlers/refer.py

from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.users import get_user_data, add_referral, update_user_premium
from config import (
    REFERRAL_REWARD_DAYS,
    BOT_USERNAME,
    BUY_PLAN_TEXT,
    PAYMENT_TEXT,
    PAYMENT_UPI_ID,
    PAYMENT_QR,
    PLAN_STICKER,
)
from utils.functions import get_user_referral_link, is_premium, get_referral_stats


@Client.on_message(filters.command("refer"))
async def referral_panel(client: Client, message: Message):
    user_id = message.from_user.id
    user_data = await get_user_data(user_id)

    if not user_data:
        return await message.reply("You're not in the database. Please use /start first.")

    ref_link = await get_user_referral_link(user_id)
    referred = user_data.get("referred", 0)
    premium = await is_premium(user_id)
    referred_by = user_data.get("referred_by", None)
    total_rewards = referred * REFERRAL_REWARD_DAYS

    stats_text = f"""
**👥 Referral System**

🔗 **Your Referral Link:** 
`https://t.me/{BOT_USERNAME}?start={user_id}`

🎁 **Rewards Earned:** `{total_rewards}` Days
👤 **Referred Users:** `{referred}`

🏆 **Premium Status:** {"✅ Active" if premium else "❌ Not Active"}
    """

    buttons = [
        [InlineKeyboardButton("💸 Buy Premium", callback_data="buy_plan")],
        [InlineKeyboardButton("🏠 Back to Home", callback_data="start_page")]
    ]

    await message.reply_photo(
        photo=PLAN_STICKER,
        caption=stats_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_message(filters.command("start") & filters.private)
async def handle_start_ref(client: Client, message: Message):
    if " " in message.text:
        payload = message.text.split(" ", 1)[1]
        if payload.isdigit():
            referrer_id = int(payload)
            user_id = message.from_user.id

            if user_id != referrer_id:
                result = await add_referral(user_id, referrer_id)
                if result:
                    await message.reply_text(
                        f"🎉 You were referred by `{referrer_id}`!\nYou've earned `{REFERRAL_REWARD_DAYS}` days of premium!",
                        quote=True
                    )
                    await update_user_premium(user_id, REFERRAL_REWARD_DAYS)
            else:
                await message.reply_text("You cannot refer yourself!", quote=True)
