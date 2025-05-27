from pyrogram import filters, Client
from pyrogram.types import Message, CallbackQuery
from bot.utils.buttons import premium_menu_buttons, premium_plans_buttons, referral_buttons
from config import PREMIUM_HEADER, PREMIUM_FOOTER, PREMIUM_FEATURES, PREMIUM_PLANS, TRIAL_DURATION_HOURS
from bot.utils.database import get_user_plan, start_trial_for_user
from datetime import datetime

@Client.on_message(filters.command("myplan"))
async def my_plan(client: Client, message: Message):
    user_id = message.from_user.id
    plan = await get_user_plan(user_id)
    if plan:
        expiry = datetime.utcfromtimestamp(plan['expires_at']).strftime('%Y-%m-%d %H:%M:%S UTC')
        text = f"\u2705 **You have an active premium plan**\n**Plan:** {plan['label']}\n**Valid until:** `{expiry}`"
    else:
        text = "\u274C You don't have any active premium plans."
    await message.reply(text)

@Client.on_callback_query(filters.regex("^premium$"))
async def premium_menu(_, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text=f"{PREMIUM_HEADER}\n\n{PREMIUM_FEATURES}\n\n{PREMIUM_FOOTER}",
        reply_markup=premium_menu_buttons(),
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex("^plans$"))
async def premium_plans(_, callback_query: CallbackQuery):
    text = "\u2728 **Available Premium Plans**\n\n"
    for days, info in PREMIUM_PLANS.items():
        text += f"\u2022 **{info['label']}**  -  ₹{info['price']}  ({days} days)\n"
    text += f"\n{PREMIUM_FOOTER}"
    await callback_query.message.edit_text(
        text=text,
        reply_markup=premium_plans_buttons(),
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex("^referral$"))
async def referral_info(_, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    invite_link = f"https://t.me/YourBotUsername?start={user_id}"  # Replace with dynamic username if needed
    count = await get_user_referral_count(user_id)
    text = f"\ud83d\udce3 **Invite Friends & Earn Premium**\n\nInvite your friends using your link below and earn premium days!\n\n**Your Link:** `{invite_link}`\n**Referrals:** {count}"
    await callback_query.message.edit_text(
        text=text,
        reply_markup=referral_buttons(user_id, count),
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex("^trial$"))
async def take_trial(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    status = await start_trial_for_user(user_id, TRIAL_DURATION_HOURS)
    if status == "already_taken":
        text = "\u274C You've already taken a trial."
    else:
        text = f"\u2705 Trial started! You now have premium access for {TRIAL_DURATION_HOURS} hours."
    await callback_query.answer(text, show_alert=True)
