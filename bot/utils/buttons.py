from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    OWNER_USERNAME,
    PAYMENT_PROOF_CHANNEL_URL,
    TUTORIAL_CHANNEL_URL,
    UPDATE_CHANNEL_URL,
    MOVIE_GROUP_URL,
    SUPPORT_GROUP_URL,
    POPULAR_CHANNEL_URL,
    TRENDING_CHANNEL_URL,
    REQUEST_CHANNEL_URL,
    PREMIUM_PLANS,
)

# --- START BUTTONS ---

def start_buttons():
    buttons = [
        [
            InlineKeyboardButton("⚒️ ADD ME TO YOUR GROUP ⚒️", url=f"t.me/Princess_Surch_Bot?startgroup=true")
        ],
        [
            InlineKeyboardButton("JOIN UPDATE CHANNEL", url=UPDATE_CHANNEL_URL),
            InlineKeyboardButton("MOVIE GROUP", url=MOVIE_GROUP_URL),
        ],
        [
            InlineKeyboardButton("SUPPORT GROUP", url=SUPPORT_GROUP_URL),
        ],
        [
            InlineKeyboardButton("ABOUT", callback_data="about"),
            InlineKeyboardButton("PREMIUM MEMBERSHIP & REFERRAL", callback_data="premium_referral"),
        ],
        [
            InlineKeyboardButton("⚒️ Help Menu", callback_data="help_menu")
        ],
    ]
    return InlineKeyboardMarkup(buttons)

# --- ABOUT BUTTONS ---

def about_buttons():
    buttons = [
        [
            InlineKeyboardButton("OWNER", url=f"https://t.me/{OWNER_USERNAME.strip('@')}"),
            InlineKeyboardButton("SUPPORT GROUP", url=SUPPORT_GROUP_URL),
        ],
        [
            InlineKeyboardButton("MOVIE GROUP", url=MOVIE_GROUP_URL),
        ],
        [
            InlineKeyboardButton("BACK", callback_data="start")
        ],
    ]
    return InlineKeyboardMarkup(buttons)

# --- PREMIUM MAIN BUTTONS ---

def premium_main_buttons():
    buttons = [
        [
            InlineKeyboardButton("PREMIUM PLANS", callback_data="premium_plans"),
            InlineKeyboardButton("REFERRAL", callback_data="referral"),
        ],
        [
            InlineKeyboardButton("TAKE TRIAL", callback_data="take_trial"),
            InlineKeyboardButton("BACK", callback_data="start"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

# --- PREMIUM PLANS BUTTONS ---

def premium_plans_buttons():
    buttons = [
        [
            InlineKeyboardButton("SEND PAYMENT SCREENSHOT", url=f"https://t.me/{OWNER_USERNAME.strip('@')}"),
        ],
        [
            InlineKeyboardButton("BACK", callback_data="premium_referral"),
            InlineKeyboardButton("HOME", callback_data="start"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

# --- REFERRAL BUTTONS ---

def referral_buttons():
    buttons = [
        [
            InlineKeyboardButton("Invite Link", callback_data="show_invite_link"),
            InlineKeyboardButton("⌛️ Referral Count", callback_data="show_referral_count"),
        ],
        [
            InlineKeyboardButton("BACK", callback_data="premium_referral"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

# --- NON-PREMIUM DOWNLOAD BUTTONS ---

def non_premium_download_buttons(short_url: str):
    buttons = [
        [
            InlineKeyboardButton("Download Now", url=short_url),
        ],
        [
            InlineKeyboardButton("How To Download", url=TUTORIAL_CHANNEL_URL),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

# --- POPULAR, TRENDING, REQUEST BUTTONS ---

def popular_button():
    return InlineKeyboardButton("🔥 Popular", url=POPULAR_CHANNEL_URL)

def trending_button():
    return InlineKeyboardButton("📈 Trending", url=TRENDING_CHANNEL_URL)

def request_button():
    return InlineKeyboardButton("📝 Request", url=REQUEST_CHANNEL_URL)

def popular_trending_request_buttons():
    buttons = [
        [popular_button(), trending_button()],
        [request_button()],
        [InlineKeyboardButton("BACK", callback_data="start")]
    ]
    return InlineKeyboardMarkup(buttons)

# --- PREMIUM PLAN TEXT GENERATOR ---

def premium_plan_text():
    plans_text = "**💎 PREMIUM PLANS**\n\n"
    for days, plan in PREMIUM_PLANS.items():
        plans_text += f"▫️ {plan['label']} - ₹{plan['price']} ({days} days)\n"
    plans_text += f"\n🧾 UPI ID: `{OWNER_USERNAME.strip('@')}@upi`"
    plans_text += "\n\n🔍 Check your plan: `/myplan`\n"
    plans_text += f"📍 Payment Proof: [Click Here]({PAYMENT_PROOF_CHANNEL_URL})"
    return plans_text

# --- PREMIUM FEATURES TEXT ---

PREMIUM_FEATURES_TEXT = (
    "💎 **Premium Membership Benefits** 💎\n\n"
    "• No ads or waiting\n"
    "• Fast and direct downloads\n"
    "• Access to exclusive content\n"
    "• Priority support\n"
    "• And much more!"
)

# --- REFERRAL TEXT ---

def referral_text(user_invite_link: str, referral_count: int):
    return (
        f"🎉 **Your Referral Link:**\n`{user_invite_link}`\n\n"
        f"👥 Total Referrals: {referral_count}\n\n"
        "Invite your friends and earn rewards!"
    )
