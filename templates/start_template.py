# templates/start_template.py

from config import (
    BOT_USERNAME,
    OWNER_USERNAME,
    TUTORIAL_CHANNEL_URL,
    UPDATE_CHANNEL_URL,
    MOVIE_GROUP_URL,
    SUPPORT_GROUP_URL,
    ABOUT_IMAGE_URL,
    PREMIUM_HEADER,
    PREMIUM_FEATURES,
    PREMIUM_FOOTER,
)

def get_start_template(name: str) -> str:
    return (
        f"<b>👋 Hello {name}!</b>\n\n"
        "Welcome to the <b>Princess Search Bot</b> 👑\n"
        "I help you find and download movies and series effortlessly from our vast database.\n\n"
        "✨ Use me in groups or search directly here.\n"
        "💎 Unlock premium for best experience!\n\n"
        "<b>⚙️ Features:</b>\n"
        "• Auto movie filtering\n"
        "• IMDb info + trailer\n"
        "• Direct downloads (premium)\n"
        "• Trial and referral system\n"
        "• AI-powered screenshot verification\n"
        "• Stylish UI & blazing fast results\n\n"
        "<i>Click a button below to get started ↓</i>"
    )


def get_about_template() -> str:
    return (
        "<b>🤖 About Me:</b>\n\n"
        "I'm a powerful Telegram bot built to search, filter, and deliver movies fast.\n"
        "Integrated with IMDb and enhanced with a premium engine and referral system.\n\n"
        "<b>👑 Developed by:</b> <a href='https://t.me/{OWNER_USERNAME}'>@{OWNER_USERNAME}</a>\n"
        "<b>📢 Updates:</b> <a href='{UPDATE_CHANNEL_URL}'>{UPDATE_CHANNEL_URL}</a>\n"
        "<b>🎬 Movie Group:</b> <a href='{MOVIE_GROUP_URL}'>{MOVIE_GROUP_URL}</a>\n"
        "<b>🛠 Support:</b> <a href='{SUPPORT_GROUP_URL}'>{SUPPORT_GROUP_URL}</a>\n"
        "<b>📖 Tutorial:</b> <a href='{TUTORIAL_CHANNEL_URL}'>{TUTORIAL_CHANNEL_URL}</a>\n"
    )


def get_premium_template() -> str:
    return (
        f"<b>{PREMIUM_HEADER}</b>\n\n"
        f"{PREMIUM_FEATURES}\n\n"
        f"{PREMIUM_FOOTER}"
    )


def get_help_template() -> str:
    return (
        "<b>🛠 Help Menu</b>\n\n"
        "Here are all available admin commands:\n\n"
        "🔸 <code>/addpremium @user 30</code> – Add 30-day premium to user\n"
        "🔸 <code>/removepremium @user</code> – Remove premium access\n"
        "🔸 <code>/myplan</code> – Show your premium status\n"
        "🔸 <code>/referral</code> – Show your referral link\n"
        "🔸 <code>/trial</code> – Start a free trial (if available)\n"
        "🔸 <code>/stats</code> – View bot statistics\n"
        "🔸 <code>/broadcast</code> – Broadcast message to all users\n"
        "🔸 <code>/verifytoken TOKEN</code> – Verify file access token\n"
        "🔸 <code>/imdb MOVIE_NAME</code> – Get IMDb info manually\n"
        "🔸 <code>/trending</code> | <code>/popular</code> – View top files\n\n"
        "📌 Use the buttons for easy navigation!"
    )
