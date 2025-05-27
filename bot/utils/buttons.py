from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import (
    OWNER_USERNAME,
    PAYMENT_PROOF_CHANNEL_URL,
)

def start_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⚒️ ADD ME TO YOUR GROUP ⚒️", url=f"https://t.me/Princess_Surch_Bot?startgroup=true"),
            ],
            [
                InlineKeyboardButton("JOIN UPDATE CHANNEL", url="https://t.me/creazy_announcement_hub"),
                InlineKeyboardButton("MOVIE GROUP", url="https://t.me/Creazy_Movie_Surch_Group"),
            ],
            [
                InlineKeyboardButton("SUPPORT GROUP", url="https://t.me/Leazy_support_group"),
            ],
            [
                InlineKeyboardButton("ABOUT", callback_data="about"),
                InlineKeyboardButton("PREMIUM MEMBERSHIP & REFERRAL", callback_data="premium_info"),
            ],
            [
                InlineKeyboardButton("⚒️ Help Menu", callback_data="help_menu"),
            ]
        ]
    )

def about_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("OWNER", url=f"https://t.me/{OWNER_USERNAME.lstrip('@')}"),
                InlineKeyboardButton("SUPPORT GROUP", url="https://t.me/Leazy_support_group"),
            ],
            [
                InlineKeyboardButton("MOVIE GROUP", url="https://t.me/Creazy_Movie_Surch_Group"),
                InlineKeyboardButton("BACK", callback_data="start"),
            ],
        ]
    )

def premium_menu_buttons():
    buttons = [
        [
            InlineKeyboardButton("PREMIUM PLANS", callback_data="premium_plans"),
            InlineKeyboardButton("REFERRAL", callback_data="referral"),
        ],
        [
            InlineKeyboardButton("TAKE TRIAL", callback_data="take_trial"),
        ],
        [
            InlineKeyboardButton("📜 CHECK MY PLAN", callback_data="myplan"),
        ],
        [
            InlineKeyboardButton("BACK", callback_data="start"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

def premium_plans_buttons():
    buttons = [
        [
            InlineKeyboardButton("SEND PAYMENT SCREENSHOT", url=f"https://t.me/{OWNER_USERNAME.lstrip('@')}"),
        ],
        [
            InlineKeyboardButton("📂 PAYMENT PROOFS", url=PAYMENT_PROOF_CHANNEL_URL),
        ],
        [
            InlineKeyboardButton("BACK", callback_data="premium_info"),
            InlineKeyboardButton("HOME", callback_data="start"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

def referral_buttons():
    buttons = [
        [
            InlineKeyboardButton("Invite Link", callback_data="invite_link"),
            InlineKeyboardButton("⌛️ Referral Count", callback_data="referral_count"),
        ],
        [
            InlineKeyboardButton("BACK", callback_data="premium_info"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

def help_menu_buttons():
    buttons = [
        [
            InlineKeyboardButton("Admin Commands", callback_data="admin_commands"),
            InlineKeyboardButton("User Commands", callback_data="user_commands"),
        ],
        [
            InlineKeyboardButton("BACK", callback_data="start"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)

def token_verification_toggle_buttons(enabled: bool):
    # Example toggle buttons for Token Verification feature on/off
    buttons = [
        [
            InlineKeyboardButton("Enable" if not enabled else "Disable", callback_data="toggle_token_verification"),
        ],
        [
            InlineKeyboardButton("BACK", callback_data="admin_menu"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)
    
def trending_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("TRENDING", callback_data="trending"),
                InlineKeyboardButton("POPULAR", callback_data="popular"),
            ],
            [
                InlineKeyboardButton("BACK", callback_data="start"),
            ],
        ]
    )


def popular_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("POPULAR", callback_data="popular"),
                InlineKeyboardButton("TRENDING", callback_data="trending"),
            ],
            [
                InlineKeyboardButton("BACK", callback_data="start"),
            ],
        ]
    )
