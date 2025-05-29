# bot/handlers/referral.py

from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import REFERRAL_REWARD_DAYS, OWNER_USERNAME, SUPPORT_GROUP_URL
from bot.utils.database import get_user_referrals, add_referral_bonus, get_user_premium_status

@Client.on_message(filters.command("referral") & filters.private)
async def referral_handler(client: Client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    referral_link = f"https://t.me/{client.me.username}?start={user_id}"

    referrals = await get_user_referrals(user_id)
    count = len(referrals)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔗 Invite Link", url=referral_link),
            InlineKeyboardButton(f"⌛️ Referrals: {count}", callback_data="ref_count")
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="start_back")
        ]
    ])

    await message.reply_photo(
        photo="https://graph.org/file/af9d0da2c3fdd791128d5-982b3f7eddd81ab274.jpg",
        caption=(
            f"👋 Hello {user_name}!

"
            f"🎉 Share your invite link below and earn **{REFERRAL_REWARD_DAYS} days** premium for each verified user.

"
            f"📝 Your Invite Link: `{referral_link}`\n"
            f"🔄 Referred Users: **{count}**\n\n"
            f"🤝 Invite your friends and enjoy more benefits!\n"
            f"👨‍💻 Contact {OWNER_USERNAME} for help."
        ),
        reply_markup=keyboard
    )


@Client.on_message(filters.command("add_referral") & filters.user([OWNER_USERNAME]))
async def add_referral_command(client: Client, message: Message):
    # Admin-only: /add_referral <referrer_id> <referred_id>
    parts = message.text.split()
    if len(parts) != 3:
        return await message.reply("Usage: /add_referral <referrer_id> <referred_id>")

    referrer_id, referred_id = int(parts[1]), int(parts[2])

    success = await add_referral_bonus(referrer_id, referred_id)
    if success:
        await message.reply("Referral bonus granted successfully.")
    else:
        await message.reply("Referral already used or invalid IDs.")

