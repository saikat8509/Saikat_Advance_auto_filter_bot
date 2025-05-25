from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.premium import (
    is_premium_user,
    get_user_plan,
    get_referral_info,
    get_user_invite_link,
    count_referrals,
    activate_trial,
)
from config import ADMIN_ID, PAYMENT_PROOF_CHANNEL, TUTORIAL_CHANNEL, UPI_ID

# 💎 /myplan - Check user's current premium status
@Client.on_message(filters.command("myplan") & filters.private)
async def my_plan(client, message):
    user_id = message.from_user.id
    plan = await get_user_plan(user_id)

    if plan:
        await message.reply_text(
            f"👤 **Premium User**\n\n"
            f"🗓️ Plan: `{plan['plan_name']}`\n"
            f"⏳ Expires: `{plan['expires_on']}`\n"
            f"💎 Status: Active\n",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🏠 Back to Menu", callback_data="back_to_menu")]]
            )
        )
    else:
        await message.reply_text(
            "🚫 You are not a premium user.\n\n"
            "Tap the button below to view membership plans.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("💎 Premium Plans", callback_data="premium_plans")]]
            )
        )

# 💰 Premium Plans Callback
@Client.on_callback_query(filters.regex("premium_plans"))
async def premium_plans_callback(client, query):
    await query.message.edit_text(
        "**💎 Premium Membership Plans:**\n\n"
        "1️⃣ 1 Week – ₹29\n"
        "2️⃣ 1 Month – ₹79\n"
        "3️⃣ 3 Months – ₹199\n\n"
        f"📤 Send payment to: `{UPI_ID}`\n"
        f"📎 Upload screenshot to: @{ADMIN_ID}\n"
        f"📁 Payment proof: [Click Here]({PAYMENT_PROOF_CHANNEL})\n\n"
        "To activate your plan, send the screenshot to admin.",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 Send Screenshot", url=f"https://t.me/{ADMIN_ID}")],
            [InlineKeyboardButton("🔙 Back", callback_data="premium_menu")],
            [InlineKeyboardButton("🏠 Home", callback_data="back_to_menu")]
        ])
    )

# 📢 Premium Info Menu
@Client.on_callback_query(filters.regex("premium_menu"))
async def premium_menu_callback(client, query):
    await query.message.edit_text(
        "**💎 Premium Membership Features:**\n\n"
        "- ⚡ Direct downloads\n"
        "- 🚫 No ads or link shorteners\n"
        "- 📊 Referral earnings\n"
        "- 🔓 Trial access option\n\n"
        "Choose an option below:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💰 Premium Plans", callback_data="premium_plans")],
            [InlineKeyboardButton("🎯 Referral", callback_data="referral_info")],
            [InlineKeyboardButton("🎁 Take Trial", callback_data="take_trial")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
        ])
    )

# 🎯 Referral Info
@Client.on_callback_query(filters.regex("referral_info"))
async def referral_info_callback(client, query):
    user = query.from_user
    invite_link = await get_user_invite_link(user.id)
    count = await count_referrals(user.id)

    await query.message.edit_text(
        "**🎯 Referral Program:**\n\n"
        f"👤 User: `{user.first_name}`\n"
        f"🔗 Invite Link: {invite_link}\n"
        f"🏆 Referrals: {count} user(s)\n\n"
        "Invite friends and earn points to redeem for premium!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Invite Link", url=invite_link)],
            [InlineKeyboardButton(f"⌛ {count} Referrals", callback_data="ref_count")],
            [InlineKeyboardButton("🔙 Back", callback_data="premium_menu")]
        ])
    )

# 🎁 Take Trial
@Client.on_callback_query(filters.regex("take_trial"))
async def trial_callback(client, query):
    user_id = query.from_user.id
    success = await activate_trial(user_id)

    if success:
        await query.answer("✅ Trial activated for 24 hours!", show_alert=True)
        await query.message.edit_text(
            "🎁 You have been granted **24 hours of premium trial access**.\n\n"
            "Enjoy direct downloads and premium features!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Home", callback_data="back_to_menu")]
            ])
        )
    else:
        await query.answer("❌ You already used your trial or are a premium user.", show_alert=True)

# 💡 How to Download Guide (linked from shortened messages)
@Client.on_callback_query(filters.regex("how_to_download"))
async def how_to_download_callback(client, query):
    await query.message.edit_text(
        f"📥 **How to Download Files:**\n\n"
        "1. Click the shortened link.\n"
        "2. Verify the token (if prompted).\n"
        "3. Wait for redirection to the actual download.\n\n"
        f"For a step-by-step video guide, [click here]({TUTORIAL_CHANNEL}).",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
        ])
    )
