import os

# === Owner and Admin Config ===
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "@Leazy_Boy")

# === Channels and Groups URLs ===
TUTORIAL_CHANNEL_URL = os.getenv("TUTORIAL_CHANNEL_URL", "https://t.me/How_to_open_file_to_link")
PAYMENT_PROOF_CHANNEL_URL = os.getenv("PAYMENT_PROOF_CHANNEL_URL", "https://t.me/creazy_payments_proof")
UPDATE_CHANNEL_URL = os.getenv("UPDATE_CHANNEL_URL", "https://t.me/creazy_announcement_hub")
MOVIE_GROUP_URL = os.getenv("MOVIE_GROUP_URL", "https://t.me/Creazy_Movie_Surch_Group")
SUPPORT_GROUP_URL = os.getenv("SUPPORT_GROUP_URL", "https://t.me/Leazy_support_group")

# === Premium Plans ===
# Structure: {duration_in_days: {label: str, price: int}}
PREMIUM_PLANS = {
    7: {"label": "Weekly Plan", "price": 40},
    15: {"label": "Bi-Weekly Plan", "price": 60},
    30: {"label": "Monthly Plan", "price": 120},
    90: {"label": "Quarterly Plan", "price": 300},
}

# === Start Command Rotating Images ===
START_IMAGES = [
    url.strip() for url in os.getenv("START_IMAGES", """
https://graph.org/file/801034beee0bc9024e364-43f7d2f29bba359564.jpg,
https://graph.org/file/1e999a80d917ff157d848-c90ea0fda9b6650053.jpg,
https://graph.org/file/1ed6d39fca02e42826bbd-4a9cb52ea057b3ff6d.jpg
""").split(",") if url.strip()
]

# === Other Configurations ===
# You can add more settings here like:
# - Referral rewards
# - Trial duration days
# - Token verification API keys
# - Force subscribe channels list
# - Wish messages / timezones etc.

# Example: Referral system settings
REFERRAL_REWARD_POINTS = int(os.getenv("REFERRAL_REWARD_POINTS", "10"))
TRIAL_DAYS = int(os.getenv("TRIAL_DAYS", "1"))

# === Function Helpers (Optional) ===

def get_premium_plan_text():
    text = "**💎 PREMIUM PLANS**\n\n"
    for days, plan in PREMIUM_PLANS.items():
        text += f"▫️ {plan['label']} - ₹{plan['price']} ({days} days)\n"
    text += f"\n🧾 UPI ID: `{OWNER_USERNAME.strip('@')}@upi`"
    text += "\n\n🔍 Check your plan: `/myplan`"
    text += f"\n📍 Payment Proof: [Click Here]({PAYMENT_PROOF_CHANNEL_URL})"
    return text

# === END OF SETTINGS ===
