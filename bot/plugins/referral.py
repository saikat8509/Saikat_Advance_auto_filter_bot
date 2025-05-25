# bot/plugins/referral.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.users import get_referral_count, get_referral_link, add_referral, create_user
from config import BOT_USERNAME, REFERRAL_BONUS_POINTS
from utils.premium import update_user_points
from utils.texts import referral_text
from bot import user_db

# Handle new user joins with referral code
@Client.on_message(filters.private & filters.command("start"))
async def handle_referral_start(client: Client, message: Message):
    user_id = message.from_user.id
    args = message.text.split()
    
    # Register user if new
    await create_user(user_id)

    if len(args) > 1:
        ref_id = args[1]
        if ref_id != str(user_id):  # Prevent self-referral
            added = await add_referral(ref_id, user_id)
            if added:
                await update_user_points(ref_id, REFERRAL_BONUS_POINTS)
                await message.reply_text(
                    f"🎉 You've been referred by user `{ref_id}`.\n"
                    f"{REFERRAL_BONUS_POINTS} referral points awarded to them!"
                )

# Command: /referral - Show referral menu
@Client.on_message(filters.private & filters.command("referral"))
async def referral_menu(client: Client, message: Message):
    user_id = message.from_user.id
    referral_link = get_referral_link(user_id)
    count = await get_referral_count(user_id)

    await message.reply_photo(
        photo="https://graph.org/file/2e1872ed3549a81c88ef4.jpg",  # Stylish referral banner
        caption=referral_text(referral_link, count),
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📢 Your Invite Link", url=referral_link),
                InlineKeyboardButton("⌛️ Total Referrals", callback_data="ref_count")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="go_back_to_premium")
            ]
        ])
    )

# Callback to show total referrals
@Client.on_callback_query(filters.regex("ref_count"))
async def show_referral_count(client, callback_query):
    user_id = callback_query.from_user.id
    count = await get_referral_count(user_id)
    await callback_query.answer(f"👥 You’ve referred {count} users.", show_alert=True)
