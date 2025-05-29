from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import (
    PREMIUM_HEADER,
    PREMIUM_FEATURES,
    PREMIUM_FOOTER,
    PAYMENT_PROOF_CHANNEL_URL,
    OWNER_USERNAME,
    PREMIUM_PLANS,
)
from bot.utils.database import (
    is_premium_user,
    get_user_plan,
)

# Helper: create main premium buttons
def premium_main_buttons():
    buttons = [
        [InlineKeyboardButton("💎 PREMIUM PLANS", callback_data="premium_plans")],
        [InlineKeyboardButton("🤝 REFERRAL", callback_data="premium_referral")],
        [InlineKeyboardButton("🎁 TAKE TRIAL", callback_data="premium_trial")],
        [InlineKeyboardButton("⬅️ BACK", callback_data="premium_back")],
    ]
    return InlineKeyboardMarkup(buttons)

# Helper: premium plans buttons
def premium_plans_buttons():
    buttons = [
        [InlineKeyboardButton(f"{plan['label']} - ₹{plan['price']}", callback_data=f"buy_plan_{key}")]
        for key, plan in PREMIUM_PLANS.items()
    ]
    buttons.append(
        [InlineKeyboardButton("📂 PAYMENT PROOFS", url=PAYMENT_PROOF_CHANNEL_URL)]
    )
    buttons.append([InlineKeyboardButton("⬅️ BACK", callback_data="premium_back")])
    return InlineKeyboardMarkup(buttons)

# /premium command
@Client.on_message(filters.command("premium") & filters.private)
async def premium_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    is_premium = await is_premium_user(user_id)
    plan = await get_user_plan(user_id)
    
    text = f"📢 **Premium Membership** 📢\n\n"
    if is_premium and plan:
        expire_str = plan.get("expire_date").strftime("%Y-%m-%d %H:%M") if plan.get("expire_date") else "Unknown"
        text += f"✅ You are a premium user.\nPlan: {plan['label']}\nExpires on: {expire_str}\n\n"
    else:
        text += "❌ You are not a premium user.\n\n"
    
    # Compose full premium message with header, features, footer
    full_text = (
        f"{PREMIUM_HEADER}\n\n"
        f"{text}"
        f"Features:\n{PREMIUM_FEATURES}\n\n"
        f"{PREMIUM_FOOTER}"
    )
    
    await message.reply_photo(
        photo=PREMIUM_HEADER.split("\n")[0],  # Assuming header includes image URL in config or replace below line accordingly
        caption=full_text,
        reply_markup=premium_main_buttons(),
        parse_mode="markdown",
    )

# Callback handler for premium menu buttons
@Client.on_callback_query(filters.regex("^premium_"))
async def premium_callback(client, callback_query):
    data = callback_query.data

    if data == "premium_plans":
        await callback_query.message.edit_text(
            "💳 **Choose a Premium Plan:**",
            reply_markup=premium_plans_buttons(),
            parse_mode="markdown",
        )
    elif data == "premium_referral":
        # Placeholder for referral info display
        await callback_query.message.edit_text(
            "📢 Referral system info coming soon!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ BACK", callback_data="premium_back")]]
            ),
            parse_mode="markdown",
        )
    elif data == "premium_trial":
        await callback_query.message.edit_text(
            "🎁 Trial feature coming soon!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ BACK", callback_data="premium_back")]]
            ),
            parse_mode="markdown",
        )
    elif data == "premium_back":
        await callback_query.message.edit_text(
            f"{PREMIUM_HEADER}\n\n"
            "Choose from the options below:",
            reply_markup=premium_main_buttons(),
            parse_mode="markdown",
        )
    elif data.startswith("buy_plan_"):
        plan_key = data.split("_")[-1]
        plan = PREMIUM_PLANS.get(plan_key)
        if not plan:
            await callback_query.answer("Invalid plan!", show_alert=True)
            return
        await callback_query.message.edit_text(
            f"You selected **{plan['label']}** plan.\n\n"
            f"Please send your payment screenshot to @{OWNER_USERNAME}.\n"
            f"After verification, your premium membership will be activated.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ BACK", callback_data="premium_plans")]]
            ),
            parse_mode="markdown",
        )
