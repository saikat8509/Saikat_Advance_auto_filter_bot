# templates/premium_template.py

from config import (
    PREMIUM_HEADER,
    PREMIUM_FEATURES,
    PREMIUM_FOOTER,
    PAYMENT_PROOF_CHANNEL_URL,
    OWNER_USERNAME
)


def get_premium_template():
    return f"""
{PREMIUM_HEADER}

<code>{PREMIUM_FEATURES}</code>

{PREMIUM_FOOTER}
"""


def get_premium_buttons():
    return [
        [
            {"text": "📜 PREMIUM PLANS", "callback_data": "premium_plans"},
            {"text": "🎁 REFERRAL", "callback_data": "referral"}
        ],
        [
            {"text": "🚀 TAKE TRIAL", "callback_data": "take_trial"},
            {"text": "📥 CHECK MY PLAN", "callback_data": "myplan"}
        ],
        [
            {"text": "⬅️ BACK", "callback_data": "start"}
        ]
    ]


def get_premium_plans_template():
    return f"""
<b>💎 Available Premium Plans:</b>

<b>🔹 1 Week:</b> ₹29  
<b>🔸 15 Days:</b> ₹49  
<b>🌟 1 Month:</b> ₹79  
<b>💫 3 Months:</b> ₹199

<b>🛍️ UPI ID:</b> <code>leazy@ybl</code>  
<b>🧾 Proofs:</b> <a href="{PAYMENT_PROOF_CHANNEL_URL}">Payment Proofs Channel</a>  
<b>⏳ Check Plan:</b> /myplan  
"""


def get_premium_plans_buttons():
    return [
        [
            {"text": "📤 SEND PAYMENT SCREENSHOT", "url": f"https://t.me/{OWNER_USERNAME.lstrip('@')}"}
        ],
        [
            {"text": "⬅️ BACK", "callback_data": "premium_menu"},
            {"text": "🏠 HOME", "callback_data": "start"}
        ]
    ]
