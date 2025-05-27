import os
import json


# === Telegram Bot Credentials ===
API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "ac9926d2cb8acc38413f5e93881fd514")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# === MongoDB ===
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "")

# === Bot Basic Config ===
BOT_USERNAME = os.getenv("BOT_USERNAME", "Princess_Surch_Bot")
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "@Leazy_Boy")
BOT_NAME = os.getenv("BOT_NAME", "Creazy Movies")

# === Channels and Groups ===
TUTORIAL_CHANNEL_URL = os.getenv("TUTORIAL_CHANNEL_URL", "https://t.me/How_to_open_file_to_link")
PAYMENT_PROOF_CHANNEL_URL = os.getenv("PAYMENT_PROOF_CHANNEL_URL", "https://t.me/creazy_payments_proof")
UPDATE_CHANNEL_URL = os.getenv("UPDATE_CHANNEL_URL", "https://t.me/creazy_announcement_hub")
MOVIE_GROUP_URL = os.getenv("MOVIE_GROUP_URL", "https://t.me/Creazy_Movie_Surch_Group")
SUPPORT_GROUP_URL = os.getenv("SUPPORT_GROUP_URL", "https://t.me/Leazy_support_group")

# === Force Subscribe ===
FORCE_SUB_CHANNELS = os.getenv("FORCE_SUB_CHANNELS", "@channel1 @channel2").split()
AUTO_APPROVE_FSUB = os.getenv("AUTO_APPROVE_FSUB", "True").lower() == "true"

# === Database Channel IDs for Indexing ===
DATABASE_CHANNEL_IDS = list(map(int, os.getenv("DATABASE_CHANNEL_IDS", "-1001234567890 -1009876543210").split()))

# === Welcome & Goodbye Images ===
WELCOME_IMAGE_URL = os.getenv("WELCOME_IMAGE_URL", "https://graph.org/file/xxx.jpg")
GOODBYE_IMAGE_URL = os.getenv("GOODBYE_IMAGE_URL", "https://graph.org/file/yyy.jpg")

# === About Section Image ===
ABOUT_IMAGE_URL = os.getenv("ABOUT_IMAGE_URL", "https://graph.org/file/zzz.jpg")

# === Popular & Trending Channels ===
POPULAR_CHANNEL_ID = int(os.getenv("POPULAR_CHANNEL_ID", "-1001122334455"))
TRENDING_CHANNEL_ID = int(os.getenv("TRENDING_CHANNEL_ID", "-1005544332211"))
REQUEST_CHANNEL_ID = int(os.getenv("REQUEST_CHANNEL_ID", "-1009988776655"))

# === Deployment ===
PORT = int(os.getenv("PORT", "8080"))

# === Premium Plans ===
PREMIUM_PLANS = {
    "7": {"days": 7, "price": 29, "label": "🥉 7 Days Plan"},
    "15": {"days": 15, "price": 49, "label": "🥈 15 Days Plan"},
    "30": {"days": 30, "price": 79, "label": "🥇 30 Days Plan"},
    "90": {"days": 90, "price": 199, "label": "🏆 90 Days Plan"},
}

# === WISHES ===
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

# === Premium System ===
TRIAL_DURATION_HOURS = int(os.getenv("TRIAL_DURATION_HOURS", "3"))
REFERRAL_REWARD_DAYS = int(os.getenv("REFERRAL_REWARD_DAYS", "3"))

# === Premium Display Content ===
PREMIUM_HEADER = os.getenv("PREMIUM_HEADER", "🔥 Unlock Premium Benefits Now!\n")
PREMIUM_FEATURES = os.getenv("PREMIUM_FEATURES", """○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪꜰʏ
○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋꜱ
○ ᴅɪʀᴇᴄᴛ ꜰɪʟᴇꜱ   
○ ᴀᴅ-ꜰʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ 
○ ʜɪɢʜ-ꜱᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ 
○ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇꜱ & ꜱᴇʀɪᴇꜱ  
○ ꜰᴜʟʟ ᴀᴅᴍɪɴ ꜱᴜᴘᴘᴏʀᴛ                              
○ ʀᴇǫᴜᴇꜱᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ ɪɴꜱᴛᴀɴᴛʟʏ [verify instantly]""")
PREMIUM_FOOTER = os.getenv("PREMIUM_FOOTER", f"🖼️ Upload your payment screenshot below (auto verification enabled)\n💬 Or DM {OWNER_USERNAME} if any issues\n📂 Proofs: {PAYMENT_PROOF_CHANNEL_URL}")

# === Token Verification Shortener ===
ENABLE_TOKEN_VERIFICATION = os.getenv("ENABLE_TOKEN_VERIFICATION", "True").lower() == "true"
SHORTENER_APIS = json.loads(os.getenv("SHORTENER_APIS_JSON", "{}"))

# === Screenshot AI Verification ===
ENABLE_SCREENSHOT_AI = os.getenv("ENABLE_SCREENSHOT_AI", "False").lower() == "true"
OCR_PROVIDER = os.getenv("OCR_PROVIDER", "tesseract")

# === Admin QR Code Image ===
ADMIN_QR_IMAGE_URL = os.getenv("ADMIN_QR_IMAGE_URL", "")
