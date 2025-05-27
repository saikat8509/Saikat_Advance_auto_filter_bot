from pyrogram import filters
from pyrogram.client import Client
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bot.utils.buttons import help_menu_buttons  # make sure this function exists in buttons.py

# Replace with your actual admin IDs
ADMINS = [123456789, 987654321]  # <-- Replace with your real admin user IDs


@Client.on_message(filters.command("help") & filters.private)
async def help_menu(client: Client, message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        return await message.reply("This help menu is only available for admins.")

    text = (
        "**👮 Admin Commands Help Menu**\n\n"
        "Here are all the available admin commands:\n\n"
        "🟢 /addpremium [user_id] [days] – Add user as premium for X days.\n"
        "🔴 /removepremium [user_id] – Remove user's premium access.\n"
        "📆 /setplan [user_id] [days] – Set/extend premium plan manually.\n"
        "✅ /checkplan [user_id] – Check if user is premium and expiry.\n"
        "👑 /premiumusers – List all current premium users.\n\n"
        "💸 /reward [user_id] [points] – Reward referral points.\n"
        "♻️ /resetref [user_id] – Reset referral count.\n"
        "🔗 /referral – Show your referral info.\n\n"
        "⚠️ /warn [user_id] [reason] – Warn a user.\n"
        "✅ /unwarn [user_id] – Remove one warning.\n"
        "🗑 /delwarn [user_id] – Clear all warnings.\n"
        "🚫 /ban [user_id] – Ban a user.\n"
        "♻️ /unban [user_id] – Unban a user.\n\n"
        "📊 /filecount – Total files in database.\n"
        "📈 /stats – Show bot usage statistics.\n"
        "🔎 /myplan – Check your current premium plan.\n\n"
        "📢 /broadcast – Send message to all users.\n"
        "🖼 /setimage start/about/welcome/goodbye/wish – Set rotating/start images.\n"
        "🔀 /toggle [feature] [on/off] – Toggle bot features like ForceSub, Shortener.\n"
    )

    buttons = help_menu_buttons()

    await message.reply_photo(
        photo="https://graph.org/file/b31d7bc58c555fa3c62a5.jpg",  # Replace with your stylish help image URL
        caption=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=buttons
    )


@Client.on_callback_query(filters.regex("^admin_commands$"))
async def admin_commands_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id not in ADMINS:
        await callback_query.answer("You are not authorized to view this.", show_alert=True)
        return

    text = (
        "**👮 Admin Commands Help Menu**\n\n"
        "Here are all the available admin commands:\n\n"
        "🟢 /addpremium [user_id] [days] – Add user as premium for X days.\n"
        "🔴 /removepremium [user_id] – Remove user's premium access.\n"
        "📆 /setplan [user_id] [days] – Set/extend premium plan manually.\n"
        "✅ /checkplan [user_id] – Check if user is premium and expiry.\n"
        "👑 /premiumusers – List all current premium users.\n\n"
        "💸 /reward [user_id] [points] – Reward referral points.\n"
        "♻️ /resetref [user_id] – Reset referral count.\n"
        "🔗 /referral – Show your referral info.\n\n"
        "⚠️ /warn [user_id] [reason] – Warn a user.\n"
        "✅ /unwarn [user_id] – Remove one warning.\n"
        "🗑 /delwarn [user_id] – Clear all warnings.\n"
        "🚫 /ban [user_id] – Ban a user.\n"
        "♻️ /unban [user_id] – Unban a user.\n\n"
        "📊 /filecount – Total files in database.\n"
        "📈 /stats – Show bot usage statistics.\n"
        "🔎 /myplan – Check your current premium plan.\n\n"
        "📢 /broadcast – Send message to all users.\n"
        "🖼 /setimage start/about/welcome/goodbye/wish – Set rotating/start images.\n"
        "🔀 /toggle [feature] [on/off] – Toggle bot features like ForceSub, Shortener.\n"
    )

    await callback_query.message.edit_text(text, reply_markup=help_menu_buttons(), parse_mode="markdown")
    await callback_query.answer()


@Client.on_callback_query(filters.regex("^user_commands$"))
async def user_commands_callback(client: Client, callback_query: CallbackQuery):
    text = (
        "**👤 User Commands Help Menu**\n\n"
        "/start - Start the bot\n"
        "/help - Show this help menu\n"
        "/myplan - Show your premium plan details\n"
        "/referral - Show your referral info\n"
        "/request - Request a movie\n"
        # Add your additional user commands here
    )
    await callback_query.message.edit_text(text, reply_markup=help_menu_buttons(), parse_mode="markdown")
    await callback_query.answer()


@Client.on_callback_query(filters.regex("^start_menu$"))
async def back_to_start(client: Client, callback_query: CallbackQuery):
    # Import your start handler here
    from bot.handlers.start import start_command  # adjust the import path if necessary
    await start_command(client, callback_query.message)
    await callback_query.answer()
