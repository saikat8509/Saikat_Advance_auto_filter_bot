import os
import json

# === Telegram Bot Credentials ===
API_ID = int(os.getenv("API_ID", "23584757"))
API_HASH = os.getenv("API_HASH", "ac9926d2cb8acc38413f5e93881fd514")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# === MongoDB ===
MONGO_DB_URI = os.getenv("MONGO_DB_URI", (
    "mongodb+srv://mailmetosaikat676:saikat9735@cluster0.2esif.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0 "
    "mongodb+srv://creazybanda84:sampa9735@cluster0.v4nwi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0 "
    "mongodb+srv://workwithsaikat:saikat9735@cluster0.0e5vp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
))

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

# === Log Channel ===
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002187892688"))

# === Force Subscribe ===
FORCE_SUB_CHANNELS = os.getenv("FORCE_SUB_CHANNELS", "@creazy_trending_movie_channel @creazy_popular_movie_channel @ceazy_backup_X").split()
AUTO_APPROVE_FSUB = os.getenv("AUTO_APPROVE_FSUB", "True").lower() == "true"

# === Database Channels ===
DATABASE_CHANNEL_IDS = list(map(int, os.getenv("DATABASE_CHANNEL_IDS", "-1002308876940 -1002509542265 -1002649284010 -1002287841044").split()))

# === Welcome & Goodbye ===
WELCOME_IMAGE_URL = os.getenv("WELCOME_IMAGE_URL", "https://graph.org/file/dff6201d94d8c1921a7d2-1a026674213213b846.jpg")
GOODBYE_IMAGE_URL = os.getenv("GOODBYE_IMAGE_URL", "https://graph.org/file/6b0c4cb1c0d90aadf7a4b-89e2cfdafea4b6acff.jpg")

# === About Image ===
ABOUT_IMAGE_URL = os.getenv("ABOUT_IMAGE_URL", "https://graph.org/file/dff6201d94d8c1921a7d2-1a026674213213b846.jpg")

# === Channels for Popular, Trending, Requests ===
POPULAR_CHANNEL_ID = int(os.getenv("POPULAR_CHANNEL_ID", "-1002619662804"))
TRENDING_CHANNEL_ID = int(os.getenv("TRENDING_CHANNEL_ID", "-1002619662804"))
REQUEST_CHANNEL_ID = int(os.getenv("REQUEST_CHANNEL_ID", "-1002303567438"))

# === Deployment Port ===
PORT = int(os.getenv("PORT", "8080"))

# === Premium Plans ===
PREMIUM_PLANS = {
    "7": {"days": 7, "price": 29, "label": "🥉 7 Days Plan"},
    "30": {"days": 30, "price": 99, "label": "🥈 15 Days Plan"},
    "90": {"days": 90, "price": 249, "label": "🥇 30 Days Plan"},
    "180": {"days": 180, "price": 549, "label": "🏆 90 Days Plan"},
}

# === Wishes System ===
WISHES = {
    "morning": {
        "text": os.getenv("GOOD_MORNING_TEXT", "Good Morning! ☀️"),
        "image": os.getenv("GOOD_MORNING_IMAGE", "https://graph.org/file/239f0d8c61da76d3e33a4-35fa7c588489ec675b.jpg")
    },
    "afternoon": {
        "text": os.getenv("GOOD_AFTERNOON_TEXT", "Good Afternoon! 🌤️"),
        "image": os.getenv("GOOD_AFTERNOON_IMAGE", "https://graph.org/file/7e0ef6ba06f38f463ad13-d77f9ce4b838171c95.jpg")
    },
    "evening": {
        "text": os.getenv("GOOD_EVENING_TEXT", "Good Evening! 🌇"),
        "image": os.getenv("GOOD_EVENING_IMAGE", "https://graph.org/file/c97b6bdff438cc626761c-6a7aec1bf2a41fe3c9.jpg")
    },
    "night": {
        "text": os.getenv("GOOD_NIGHT_TEXT", "Good Night! 🌙"),
        "image": os.getenv("GOOD_NIGHT_IMAGE", "https://graph.org/file/10030b1c0e17097e53758-35355c1185104c8217.jpg")
    }
}

# === Premium System Settings ===
TRIAL_DURATION_HOURS = int(os.getenv("TRIAL_DURATION_HOURS", "3"))
REFERRAL_REWARD_DAYS = int(os.getenv("REFERRAL_REWARD_DAYS", "15"))

# === Premium Display ===
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

# === Token Verification ===
ENABLE_TOKEN_VERIFICATION = os.getenv("ENABLE_TOKEN_VERIFICATION", "True").lower() == "true"
SHORTENER_APIS = json.loads(os.getenv("SHORTENER_APIS_JSON", "{}"))

# === Screenshot AI Verification ===
ENABLE_SCREENSHOT_AI = os.getenv("ENABLE_SCREENSHOT_AI", "True").lower() == "true"
OCR_PROVIDER = os.getenv("OCR_PROVIDER", "tesseract")

# === Admin QR Code Image ===
ADMIN_QR_IMAGE_URL = os.getenv("ADMIN_QR_IMAGE_URL", "https://graph.org/file/42ebe0594c3356a5a0428-6e4437cdf281c5d517.jpg")

# === Start Command Rotating Images ===
START_IMAGES = [img.strip() for img in os.getenv("START_IMAGES", """
https://graph.org/file/801034beee0bc9024e364-43f7d2f29bba359564.jpg,
https://graph.org/file/1e999a80d917ff157d848-c90ea0fda9b6650053.jpg,
https://graph.org/file/1ed6d39fca02e42826bbd-4a9cb52ea057b3ff6d.jpg
""").split(",") if img.strip()]
