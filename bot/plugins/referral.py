# bot/plugins/referral.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import BOT_USERNAME
from bot.utils.database import (
    get_user_referral_count,
    add_referral,
    has_referred_before,
    get_referral_link,
)
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def referral_start_handler(client: Client, message: Message):
    """
    Handle /start with optional referral code.
    If user is new and referral code is valid, grant referral points.
    """
    args = message.text.split()
    user_id = message.from_user.id
    referrer_id = None

    if len(args) > 1:
        ref_code = args[1]
        try:
            referrer_id = int(ref_code)
        except ValueError:
            # Invalid referral code, ignore
            referrer_id = None

    # Check if user has referred before to prevent multiple referral credits
    already_referred = await has_referred_before(user_id)

    if referrer_id and referrer_id != user_id and not already_referred:
        # Add referral to DB
        success = await add_referral(referrer_id, user_id)
        if success:
            await message.reply_text(
                f"🎉 Thanks for joining! You were referred by user ID: {referrer_id}.\n"
                f"Referral points have been credited."
            )
        else:
            await message.reply_text("⚠️ Unable to process referral at the moment.")
    else:
        # Normal /start message without referral or invalid referral
        await message.reply_text("Welcome to the bot! Use /help to see commands.")

@Client.on_message(filters.command("myreferrals") & filters.private)
async def my_referrals(client: Client, message: Message):
    """
    Show the user their referral count and referral link.
    """
    user_id = message.from_user.id
    count = await get_user_referral_count(user_id)
    ref_link = get_referral_link(user_id, BOT_USERNAME)

    text = (
        f"🔗 Your referral link:\n{ref_link}\n\n"
        f"👥 Total users referred: {count}\n\n"
        "Share this link with your friends and earn rewards!"
    )
    await message.reply_text(text)

