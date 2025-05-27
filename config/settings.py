import os
import json
from dotenv import load_dotenv

load_dotenv()

# Basic Bot Settings
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "Leazy_Boy")
ADMINS = list(map(int, os.getenv("ADMINS", "").split(","))) if os.getenv("ADMINS") else []

# MongoDB Settings
MONGO_URI = os.getenv("MONGO_URI", "")

# Channels & Groups URLs / IDs
TUTORIAL_CHANNEL_URL = os.getenv("TUTORIAL_CHANNEL_URL", "https://t.me/How_to_open_file_to_link")
PAYMENT_PROOF_CHANNEL_URL = os.getenv("PAYMENT_PROOF_CHANNEL_URL", "https://t.me/creazy_payments_proof")

FORCE_SUBSCRIBE_CHANNELS = list(
    filter(None, [ch.strip() for ch in os.getenv("FORCE_SUBSCRIBE_CHANNELS", "").split(",")])
)

# Image URLs (graph.org hosted)
WELCOME_IMAGE_URL = os.getenv("WELCOME_IMAGE_URL", "")
GOODBYE_IMAGE_URL = os.getenv("GOODBYE_IMAGE_URL", "")

WISH_IMAGES = {
    "morning": os.getenv("WISH_MORNING_IMAGE_URL", ""),
    "afternoon": os.getenv("WISH_AFTERNOON_IMAGE_URL", ""),
    "evening": os.getenv("WISH_EVENING_IMAGE_URL", ""),
    "night": os.getenv("WISH_NIGHT_IMAGE_URL", ""),
}

# Rotating /start command images (list)
START_IMAGES = list(filter(None, os.getenv("START_IMAGES", "").split()))

# Premium Membership Settings
REFERRAL_REWARD_DAYS = int(os.getenv("REFERRAL_REWARD_DAYS", "3"))

PREMIUM_DAYS_OPTIONS = list(map(int, os.getenv("PREMIUM_DAYS_OPTIONS", "7 15 30 90").split()))
PREMIUM_PRICE_OPTIONS = list(map(int, os.getenv("PREMIUM_PRICE_OPTIONS", "70 150 300 900").split()))

# Create a list of dicts for premium plans for easy reference
PREMIUM_PLANS = [
    {"days": days, "price": price, "label": f"{days} Days Plan"}
    for days, price in zip(PREMIUM_DAYS_OPTIONS, PREMIUM_PRICE_OPTIONS)
]

# AI Screenshot Payment Verification
ENABLE_SCREENSHOT_AI = os.getenv("ENABLE_SCREENSHOT_AI", "False").lower() == "true"
OCR_PROVIDER = os.getenv("OCR_PROVIDER", "tesseract").lower()  # 'tesseract' or 'google'

# URL Shortener API keys (dict loaded from JSON string)
try:
    SHORTENER_APIS = json.loads(os.getenv("SHORTENER_APIS_JSON", "{}"))
except json.JSONDecodeError:
    SHORTENER_APIS = {}

# Deployment Port
PORT = int(os.getenv("PORT", "8080"))


# Additional Constants
PAYMENT_PROOF_CHANNEL = PAYMENT_PROOF_CHANNEL_URL

# Premium footer text (used in messages)
PREMIUM_FOOTER = (
    f"🧾 Send payment screenshot to @{OWNER_USERNAME}\n"
    f"📂 Proof: {PAYMENT_PROOF_CHANNEL_URL}"
)

# Example function to get premium plan text dynamically
def get_premium_plans_text():
    header = (
        "○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪꜰʏ\n"
        "○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋꜱ\n"
        "○ ᴅɪʀᴇᴄᴛ ꜰɪʟᴇꜱ\n"
        "○ ᴀᴅ-ꜰʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ\n"
        "○ ʜɪɢʜ-ꜱᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ\n"
        "○ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇꜱ & ꜱᴇʀɪᴇꜱ\n"
        "○ ꜰᴜʟʟ ᴀᴅᴍɪɴ ꜱᴜᴘᴘᴏʀᴛ\n"
        "○ ʀᴇǫᴜᴇꜱᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ instantly [ verify instantly]\n\n"
    )
    plans_text = "\n".join(
        [f"• {plan['label']} — ₹{plan['price']}" for plan in PREMIUM_PLANS]
    )
    footer = f"\n{PREMIUM_FOOTER}"
    return header + plans_text + footer

