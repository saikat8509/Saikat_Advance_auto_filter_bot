from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import (
    OWNER_USERNAME, UPDATE_CHANNEL, MOVIE_GROUP, SUPPORT_GROUP,
    TUTORIAL_CHANNEL, PAYMENT_PROOF_CHANNEL_URL, START_IMAGES,
    PREMIUM_HEADER, PREMIUM_FEATURES, PREMIUM_FOOTER
)
from bot.utils.database import db

@Client.on_callback_query(filters.regex("about"))
async def about_page(client, callback_query: CallbackQuery):
    await callback_query.message.edit_caption(
        caption=f"""👤 **Owner:** {OWNER_USERNAME}
📢 **Update Channel:** {UPDATE_CHANNEL}
🎬 **Movie Group:** {MOVIE_GROUP}
💬 **Support Group:** {SUPPORT_GROUP}""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("OWNER", url=f"https://t.me/{OWNER_USERNAME.strip('@')}")],
            [
                InlineKeyboardButton("SUPPORT GROUP", url=SUPPORT_GROUP),
                InlineKeyboardButton("MOVIE GROUP", url=MOVIE_GROUP)
            ],
            [InlineKeyboardButton("BACK", callback_data="start")]
        ])
    )

@Client.on_callback_query(filters.regex("premium_info"))
async def premium_info_page(client, callback_query: CallbackQuery):
    await callback_query.message.edit_caption(
        caption=f"{PREMIUM_HEADER}\n\n{PREMIUM_FEATURES}\n\n{PREMIUM_FOOTER}",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("PREMIUM PLANS", callback_data="premium_plans"),
                InlineKeyboardButton("REFERRAL", callback_data="referral")
            ],
            [
                InlineKeyboardButton("TAKE TRIAL", callback_data="take_trial"),
                InlineKeyboardButton("BACK", callback_data="start")
            ]
        ])
    )

@Client.on_callback_query(filters.regex("premium_plans"))
async def premium_plans_page(client, callback_query: CallbackQuery):
    from config import PREMIUM_PLANS, ADMIN_UPI_ID
    plan_list = "\n".join([
        f"💠 {plan['label']} — Rs. {plan['price']} / {plan['days']} days"
        for plan in PREMIUM_PLANS.values()
    ])

    caption = f"""💳 **Premium Plans**\n\n{plan_list}\n\n📥 **Send Payment to UPI:** `{ADMIN_UPI_ID}`\n🧾 After payment, click below to send screenshot.\n\n🔍 Check: `/myplan` to see your status.\n📢 Payment Proofs: {PAYMENT_PROOF_CHANNEL_URL}"""

    await callback_query.message.edit_caption(
        caption=caption,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("SEND PAYMENT SCREENSHOT", url=f"https://t.me/{OWNER_USERNAME.strip('@')}")],
            [
                InlineKeyboardButton("BACK", callback_data="premium_info"),
                InlineKeyboardButton("HOME", callback_data="start")
            ]
        ])
    )

@Client.on_callback_query(filters.regex("referral"))
async def referral_page(client, callback_query: CallbackQuery):
    user = callback_query.from_user
    ref_link = f"https://t.me/{client.me.username}?start={user.id}"
    count = await db.get_referral_count(user.id)

    await callback_query.message.edit_caption(
        caption=f"🎁 **Your Referral Link:**\n`{ref_link}`\n\n👥 **Referral Count:** {count}\n\n📢 Share this link to earn free Premium!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Invite Link", url=ref_link)],
            [InlineKeyboardButton("⌛️ Referrals", callback_data="referral")],
            [InlineKeyboardButton("BACK", callback_data="premium_info")]
        ])
    )

@Client.on_callback_query(filters.regex("take_trial"))
async def take_trial(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    granted = await db.grant_trial(user_id)

    if granted:
        await callback_query.answer("✅ Trial granted! You have limited access.", show_alert=True)
    else:
        await callback_query.answer("⚠️ Trial already used or unavailable.", show_alert=True)

@Client.on_callback_query(filters.regex("help_menu"))
async def help_menu(client, callback_query: CallbackQuery):
    help_text = """⚒️ **Admin Help Commands:**

• /addpremium user_id days - Grant premium manually
• /removepremium user_id - Remove premium access
• /myplan - User's current plan info
• /ban user_id - Ban a user
• /unban user_id - Unban a user
• /broadcast - Send message to all users
• /stats - Show total users
• /setfsub - Set force subscribe channels
• /adddb - Add channel to DB Index
• /wish - Trigger wish messages manually
• /popular - Get most viewed files
• /trending - Get most searched files"""

    await callback_query.message.edit_caption(
        caption=help_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("BACK", callback_data="start")]
        ])
    )

@Client.on_callback_query(filters.regex("start"))
async def back_to_start(client, callback_query: CallbackQuery):
    # Call /start logic from handlers
    from bot.handlers.start import start_private
    await start_private(client, callback_query.message)
