import os
import json
from dotenv import load_dotenv

load_dotenv()

# === Basic Telegram Bot Config ===
API_ID = int(os.getenv("API_ID", "123456"))  # Replace default with your actual API_ID
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

# === Bot Owner/Admin Details ===
ADMINS = [int(admin) for admin in os.getenv("ADMINS", "").split()]
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "@Leazy_Boy")
ADMIN_QR_IMAGE_URL = os.getenv("ADMIN_QR_IMAGE_URL", "")

# === MongoDB Config ===
MONGODB_URIS = os.getenv("MONGODB_URIS", "").split()  # Supports multiple MongoDB URIs

# === Channel and Group Config ===
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-100123456789"))
POPULAR_CHANNEL_ID = int(os.getenv("POPULAR_CHANNEL_ID", "-100123456789"))
TRENDING_CHANNEL_ID = int(os.getenv("TRENDING_CHANNEL_ID", "-100123456789"))
REQUEST_CHANNEL_ID = int(os.getenv("REQUEST_CHANNEL_ID", "-100123456789"))
PAYMENT_PROOF_CHANNEL_URL = os.getenv("PAYMENT_PROOF_CHANNEL_URL", "https://t.me/creazy_payments_proof")

FORCE_SUBSCRIBE_CHANNELS = os.getenv("FORCE_SUBSCRIBE_CHANNELS", "").split()  # Multiple FSub channel usernames or IDs
AUTO_APPROVE_FSUB = os.getenv("AUTO_APPROVE_FSUB", "True").lower() == "true"

# === Deployment Config ===
PORT = int(os.getenv("PORT", "8080"))  # For Koyeb or any platform

# === Welcome / Goodbye / Time-based Wishes ===
WELCOME_IMAGE_URL = os.getenv("WELCOME_IMAGE_URL", "")
GOODBYE_IMAGE_URL = os.getenv("GOODBYE_IMAGE_URL", "")
START_IMAGES = os.getenv("START_IMAGES", "").split()  # Multiple Graph.org image links

WISHES = {
    "morning": {
        "text": os.getenv("GOOD_MORNING_TEXT", "Good Morning! ☀️"),
        "image": os.getenv("GOOD_MORNING_IMAGE", "")
    },
    "afternoon": {
        "text": os.getenv("GOOD_AFTERNOON_TEXT", "Good Afternoon! 🌤️"),
        "image": os.getenv("GOOD_AFTERNOON_IMAGE", "")
    },
    "evening": {
        "text": os.getenv("GOOD_EVENING_TEXT", "Good Evening! 🌇"),
        "image": os.getenv("GOOD_EVENING_IMAGE", "")
    },
    "night": {
        "text": os.getenv("GOOD_NIGHT_TEXT", "Good Night! 🌙"),
        "image": os.getenv("GOOD_NIGHT_IMAGE", "")
    }
}

# === UI & Branding ===
ABOUT_IMAGE_URL = os.getenv("ABOUT_IMAGE_URL", "")
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "https://t.me/Leazy_support_group")
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "https://t.me/creazy_announcement_hub")
MOVIE_GROUP = os.getenv("MOVIE_GROUP", "https://t.me/Creazy_Movie_Surch_Group")

# === Premium System ===
TRIAL_DURATION_HOURS = int(os.getenv("TRIAL_DURATION_HOURS", "3"))
REFERRAL_REWARD_DAYS = int(os.getenv("REFERRAL_REWARD_DAYS", "3"))

PREMIUM_PLANS = {
    "7": {"days": 7, "price": 29, "label": "7-Days"},
    "15": {"days": 15, "price": 49, "label": "15-Days"},
    "30": {"days": 30, "price": 99, "label": "30-Days"},
    "90": {"days": 90, "price": 249, "label": "90-Days"}
}

PREMIUM_HEADER = os.getenv("PREMIUM_HEADER", "🔥 Unlock Premium Benefits Now!\n")
PREMIUM_FEATURES = os.getenv("PREMIUM_FEATURES", """○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪꜰʏ
○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋꜱ
○ ᴅɪʀᴇᴄᴛ ꜰɪʟᴇꜱ   
○ ᴀᴅ-ꜰʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ 
○ ʜɪɢʜ-ꜱᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ 
○ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇꜱ & ꜱᴇʀɪᴇꜱ  
○ ꜰᴜʟʟ ᴀᴅᴍɪɴ ꜱᴜᴘᴘᴏʀᴛ                              
○ ʀᴇǫᴜᴇꜱᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ ɪɴꜱᴛᴀɴᴛʟʏ [verify instantly]""")

PREMIUM_FOOTER = os.getenv(
    "PREMIUM_FOOTER",
    f"🖼️ Upload your payment screenshot below (auto verification enabled)\n💬 Or DM {OWNER_USERNAME} if any issues\n📂 Proofs: {PAYMENT_PROOF_CHANNEL_URL}"
)

# === Token Verification Shortener ===
ENABLE_TOKEN_VERIFICATION = os.getenv("ENABLE_TOKEN_VERIFICATION", "True").lower() == "true"

# Shortener domain-to-key mapping via JSON (recommended)
# Example in .env: SHORTENER_APIS_JSON='{"shortzon": "api_key", "try2link": "api_key"}'
SHORTENER_APIS = json.loads(os.getenv("SHORTENER_APIS_JSON", "{}"))

# === Screenshot AI Verification Settings ===
ENABLE_SCREENSHOT_AI = os.getenv("ENABLE_SCREENSHOT_AI", "False").lower() == "true"
OCR_PROVIDER = os.getenv("OCR_PROVIDER", "tesseract")  # or "google"
