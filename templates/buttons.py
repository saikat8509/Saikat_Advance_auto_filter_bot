from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚒️ ADD ME TO YOUR GROUP ⚒️", url="https://t.me/Princess_Surch_Bot?startgroup=true")
        ],
        [
            InlineKeyboardButton("JOIN UPDATE CHANNEL", url="https://t.me/creazy_announcement_hub"),
            InlineKeyboardButton("MOVIE GROUP", url="https://t.me/Creazy_Movie_Surch_Group")
        ],
        [
            InlineKeyboardButton("SUPPORT GROUP", url="https://t.me/Leazy_support_group")
        ],
        [
            InlineKeyboardButton("ABOUT", callback_data="about_menu"),
            InlineKeyboardButton("PREMIUM MEMBERSHIP & REFERRAL", callback_data="premium_menu")
        ],
        [
            InlineKeyboardButton("⚒️Help Menu", callback_data="admin_help")
        ]
    ])


def about_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👑 OWNER", url="https://t.me/Leazy_Boy"),
            InlineKeyboardButton("💬 SUPPORT GROUP", url="https://t.me/Leazy_support_group")
        ],
        [
            InlineKeyboardButton("🎬 MOVIE GROUP", url="https://t.me/Creazy_Movie_Surch_Group")
        ],
        [
            InlineKeyboardButton("BACK", callback_data="start")
        ]
    ])


def premium_menu_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💰 PREMIUM PLANS", callback_data="premium_plans"),
            InlineKeyboardButton("🎁 REFERRAL", callback_data="referral_menu")
        ],
        [
            InlineKeyboardButton("🧪 TAKE TRIAL", callback_data="trial_request")
        ],
        [
            InlineKeyboardButton("BACK", callback_data="start")
        ]
    ])


def premium_plan_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📜 CHECK MY PLAN", callback_data="myplan")
        ],
        [
            InlineKeyboardButton("🖼 SEND PAYMENT SCREENSHOT", url="https://t.me/Leazy_Boy")
        ],
        [
            InlineKeyboardButton("BACK", callback_data="premium_menu"),
            InlineKeyboardButton("🏠 HOME", callback_data="start")
        ]
    ])


def referral_buttons(ref_link):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🤝 Invite Link", url=ref_link)
        ],
        [
            InlineKeyboardButton("⌛️ Referral Count", callback_data="referral_count")
        ],
        [
            InlineKeyboardButton("BACK", callback_data="premium_menu")
        ]
    ])


def non_premium_download_buttons(short_url):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔗 Download Now", url=short_url)
        ],
        [
            InlineKeyboardButton("📖 How To Download", url="https://t.me/How_to_open_file_to_link")
        ]
    ])


def trending_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔥 TRENDING", callback_data="trending"),
            InlineKeyboardButton("🌟 POPULAR", callback_data="popular")
        ],
        [
            InlineKeyboardButton("BACK", callback_data="start")
        ]
    ])


def popular_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🌟 POPULAR", callback_data="popular"),
            InlineKeyboardButton("🔥 TRENDING", callback_data="trending")
        ],
        [
            InlineKeyboardButton("BACK", callback_data="start")
        ]
    ])
