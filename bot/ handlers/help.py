from pyrogram import filters, types
from pyrogram.enums import ParseMode
from pyrogram.client import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Replace this list with your actual admin IDs
ADMINS = [123456789, 987654321]  # Replace with real admin IDs

@Client.on_message(filters.command("help") & filters.private)
async def help_menu(client: Client, message: types.Message):
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

    buttons = [
        [
            InlineKeyboardButton("🏠 Home", callback_data="start_menu"),
            InlineKeyboardButton("📦 Premium Panel", callback_data="premium_info"),
        ],
        [
            InlineKeyboardButton("💬 Support Group", url="https://t.me/Leazy_support_group"),
            InlineKeyboardButton("👑 Owner", url="https://t.me/Leazy_Boy"),
        ]
    ]

    await message.reply_photo(
        photo="https://graph.org/file/b31d7bc58c555fa3c62a5.jpg",  # Replace with your stylish help image
        caption=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
