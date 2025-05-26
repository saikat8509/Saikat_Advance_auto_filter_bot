# bot/utils/buttons.py

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    ADMIN_USERNAME,
    UPDATE_CHANNEL,
    MOVIE_GROUP,
    SUPPORT_GROUP,
    TUTORIAL_CHANNEL,
    PAYMENT_PROOF_CHANNEL
)

def start_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚒️ ADD ME TO YOUR GROUP ⚒️", url="https://t.me/Princess_Surch_Bot?startgroup=true")],
        [InlineKeyboardButton("JOIN UPDATE CHANNEL", url=UPDATE_CHANNEL)],
        [InlineKeyboardButton("MOVIE GROUP", url=MOVIE_GROUP)],
        [InlineKeyboardButton("SUPPORT GROUP", url=SUPPORT_GROUP)],
        [
            InlineKeyboardButton("ABOUT", callback_data="about"),
            InlineKeyboardButton("PREMIUM MEMBERSHIP & REFERRAL", callback_data="premium_menu")
        ],
        [InlineKeyboardButton("⚒️ Help Menu", callback_data="help_menu")]
    ])

def about_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 OWNER", url=f"https://t.me/{ADMIN_USERNAME}")],
        [InlineKeyboardButton("🎬 MOVIE GROUP", url=MOVIE_GROUP)],
        [InlineKeyboardButton("🛠 SUPPORT GROUP", url=SUPPORT_GROUP)],
        [InlineKeyboardButton("⬅️ BACK", callback_data="start")]
    ])

def premium_main_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 PREMIUM PLANS", callback_data="premium_plans")],
        [InlineKeyboardButton("🎯 REFERRAL", callback_data="referral")],
        [InlineKeyboardButton("🎁 TAKE TRIAL", callback_data="trial")],
        [InlineKeyboardButton("⬅️ BACK", callback_data="start")]
    ])

def premium_plans_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💸 SEND PAYMENT SCREENSHOT", url=f"https://t.me/{ADMIN_USERNAME}")],
        [InlineKeyboardButton("📜 CHECK MY PLAN", callback_data="myplan")],
        [InlineKeyboardButton("📂 PAYMENT PROOFS", url=PAYMENT_PROOF_CHANNEL)],
        [InlineKeyboardButton("⬅️ BACK", callback_data="premium_menu")],
        [InlineKeyboardButton("🏠 HOME", callback_data="start")]
    ])

def referral_buttons(referral_link):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Invite Link", url=referral_link)],
        [InlineKeyboardButton("⌛️ Referral Count", callback_data="referral_count")],
        [InlineKeyboardButton("⬅️ BACK", callback_data="premium_menu")]
    ])

def download_buttons(shortened_url):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬇️ Download Now", url=shortened_url)],
        [InlineKeyboardButton("📺 How To Download?", url=TUTORIAL_CHANNEL)]
    ])

def spell_buttons(suggestions):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🎯 {title}", callback_data=f"spellfix:{title}")]
        for title in suggestions
    ])

def back_to_premium():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ BACK", callback_data="premium_menu")]
    ])

def help_menu_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔧 Admin Commands", callback_data="admin_cmds")],
        [InlineKeyboardButton("🔎 User Commands", callback_data="user_cmds")],
        [InlineKeyboardButton("⬅️ BACK", callback_data="start")]
    ])

def admin_help_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ BACK", callback_data="help_menu")]
    ])

def user_help_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ BACK", callback_data="help_menu")]
    ])

def trending_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Top 10 Trending", callback_data="show_trending")],
        [InlineKeyboardButton("⬅️ BACK", callback_data="start")]
    ])

def popular_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Most Downloaded", callback_data="show_popular")],
        [InlineKeyboardButton("⬅️ BACK", callback_data="start")]
    ])
