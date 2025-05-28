from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    BOT_USERNAME,
    OWNER_USERNAME,
    PAYMENT_PROOF_CHANNEL_URL,
    TUTORIAL_CHANNEL_URL,
    UPDATE_CHANNEL_URL,
    MOVIE_GROUP_URL,
    SUPPORT_GROUP_URL,
    PREMIUM_HEADER,
    PREMIUM_FEATURES,
    PREMIUM_FOOTER,
)

# Start buttons
def get_start_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚒️ ADD ME TO YOUR GROUP ⚒️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton("JOIN UPDATE CHANNEL", url=UPDATE_CHANNEL_URL)],
        [InlineKeyboardButton("MOVIE GROUP", url=MOVIE_GROUP_URL)],
        [InlineKeyboardButton("SUPPORT GROUP", url=SUPPORT_GROUP_URL)],
        [
            InlineKeyboardButton("ABOUT", callback_data="about"),
            InlineKeyboardButton("PREMIUM MEMBERSHIP & REFERRAL", callback_data="premium_referral"),
            InlineKeyboardButton("⚒️Help Menu", callback_data="help_menu")
        ],
    ])

# About buttons
def get_about_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("OWNER", url=f"https://t.me/{OWNER_USERNAME.lstrip('@')}")],
        [InlineKeyboardButton("SUPPORT GROUP", url=SUPPORT_GROUP_URL)],
        [InlineKeyboardButton("MOVIE GROUP", url=MOVIE_GROUP_URL)],
        [InlineKeyboardButton("BACK", callback_data="start")]
    ])

# Premium & Referral main buttons
def get_premium_referral_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("PREMIUM PLANS", callback_data="premium_plans")],
        [InlineKeyboardButton("REFERRAL", callback_data="referral")],
        [InlineKeyboardButton("TAKE TRIAL", callback_data="take_trial")],
        [InlineKeyboardButton("BACK", callback_data="start")]
    ])

# Premium plans buttons including Payment Proof channel button
def get_premium_plans_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("SEND PAYMENT SCREENSHOT", url=f"https://t.me/{OWNER_USERNAME.lstrip('@')}")],
        [InlineKeyboardButton("PROOF CHANNEL", url=PAYMENT_PROOF_CHANNEL_URL)],  # <-- Added here
        [InlineKeyboardButton("BACK", callback_data="premium_referral")],
        [InlineKeyboardButton("HOME", callback_data="start")]
    ])

# Referral buttons
def get_referral_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Invite Link", callback_data="invite_link")],
        [InlineKeyboardButton("⌛️ Referral Count", callback_data="referral_count")],
        [InlineKeyboardButton("BACK", callback_data="premium_referral")]
    ])

# Non-premium download buttons with tutorial link
def get_non_premium_download_buttons(shortened_link):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Download Now", url=shortened_link)],
        [InlineKeyboardButton("How To Download", url=TUTORIAL_CHANNEL_URL)],
    ])

# Help menu buttons (example list of admin commands)
def get_help_menu_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Admin Commands", callback_data="admin_commands")],
        [InlineKeyboardButton("BACK", callback_data="start")]
    ])
