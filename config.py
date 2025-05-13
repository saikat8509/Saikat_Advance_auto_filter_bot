import os

# ✅ Telegram Bot Token & API
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")

# ✅ MongoDB Configuration (🔁 Multiple)
MONGO_URIS = os.environ.get("MONGO_URIS", "").split()  # space-separated list of URIs

# ✅ Admin & Auth Users
ADMINS = list(map(int, os.environ.get("ADMINS", "").split()))
AUTH_USERS = list(map(int, os.environ.get("AUTH_USERS", "").split()))

# ✅ Force Subscribe Channels (🔁 Multiple)
FSUB_CHANNELS = list(map(int, os.environ.get("FSUB_CHANNELS", "").split()))

# ✅ Index Channels (🔁 Multiple) — used for file indexing with MongoDB
INDEX_CHANNEL_IDS = list(map(int, os.environ.get("INDEX_CHANNEL_IDS", "").split()))

# ✅ Trending Channel — where new indexed files with IMDb info + movie link button are posted
TRENDING_CHANNEL_ID = int(os.environ.get("TRENDING_CHANNEL_ID", 0))

# ✅ Most Searched Channel — where top searched movies are posted with IMDb info + movie link button
MOST_SEARCHED_CHANNEL_ID = int(os.environ.get("MOST_SEARCHED_CHANNEL_ID", 0))

# ✅ Link Shortener + Token Verification
ENABLE_SHORTENER = os.environ.get("ENABLE_SHORTENER", "True").lower() == "true"
TOKEN_VERIFICATION = os.environ.get("TOKEN_VERIFICATION", "True").lower() == "true"
SHORTENER_DOMAINS = os.environ.get("SHORTENER_DOMAINS", "").split()  # domain list
SHORTENER_API_KEYS = os.environ.get("SHORTENER_API_KEYS", "").split()  # API keys (same order)
TOKEN_VALIDITY_HOURS = int(os.environ.get("TOKEN_VALIDITY_HOURS", 24))

# ✅ Premium Membership System
ENABLE_PREMIUM = os.environ.get("ENABLE_PREMIUM", "True").lower() == "true"
PREMIUM_PLAN_TEXT = os.environ.get("PREMIUM_PLAN_TEXT", "✨ Premium Plan:\n\n1 Month - ₹49\n3 Months - ₹99\nLifetime - ₹199")
PAYMENT_UPI_ID = os.environ.get("PAYMENT_UPI_ID", "admin@upi")
PAYMENT_QR_CODE_URL = os.environ.get("PAYMENT_QR_CODE_URL", "")
REFERRAL_REWARD_DAYS = int(os.environ.get("REFERRAL_REWARD_DAYS", 3))  # days given per referral
PREMIUM_STICKER_URL = os.environ.get("PREMIUM_STICKER_URL", "")

# ✅ Channel/Group Links (used in /start & /stats buttons)
MOVIE_GROUP_LINK = os.environ.get("MOVIE_GROUP_LINK", "")
UPDATES_CHANNEL_LINK = os.environ.get("UPDATES_CHANNEL_LINK", "")
BACKUP_GROUP_LINK = os.environ.get("BACKUP_GROUP_LINK", "")

# ✅ /start Command Thumbnail Image
START_PIC_URL = os.environ.get("START_PIC_URL", "")

# ✅ Time-Based Wishes (text + stickers)
ENABLE_WISHES = os.environ.get("ENABLE_WISHES", "True").lower() == "true"

GOOD_MORNING_TEXT = os.environ.get("GOOD_MORNING_TEXT", "🌅 Good Morning!\nEnjoy your day with movies 🍿")
GOOD_AFTERNOON_TEXT = os.environ.get("GOOD_AFTERNOON_TEXT", "☀️ Good Afternoon!\nTake a movie break 🎬")
GOOD_EVENING_TEXT = os.environ.get("GOOD_EVENING_TEXT", "🌇 Good Evening!\nTime for a blockbuster 🎥")
GOOD_NIGHT_TEXT = os.environ.get("GOOD_NIGHT_TEXT", "🌙 Good Night!\nWatch & sleep well 😴")

GOOD_MORNING_STICKER = os.environ.get("GOOD_MORNING_STICKER", "")
GOOD_AFTERNOON_STICKER = os.environ.get("GOOD_AFTERNOON_STICKER", "")
GOOD_EVENING_STICKER = os.environ.get("GOOD_EVENING_STICKER", "")
GOOD_NIGHT_STICKER = os.environ.get("GOOD_NIGHT_STICKER", "")

# ✅ IMDb API Key
OMDB_API_KEY = os.environ.get("OMDB_API_KEY", "")

# ✅ IMDb Message Template
IMDB_MESSAGE_TEMPLATE = os.environ.get("IMDB_MESSAGE_TEMPLATE", """
🎬 **{title}** ({year})
🌟 IMDb: {rating}/10
🎭 Genre: {genre}
📅 Released: {release_date}
🕐 Runtime: {runtime}
🌐 Language: {language}
📽 Director: {director}
✍ Writer: {writer}
👨‍👩‍👧‍👦 Actors: {actors}
📝 Plot: {plot}
""")

# ✅ Feature Toggles
ENABLE_AUTO_DELETE = os.environ.get("ENABLE_AUTO_DELETE", "True").lower() == "true"
ENABLE_FS_JOIN_REQUEST = os.environ.get("ENABLE_FS_JOIN_REQUEST", "True").lower() == "true"
AUTO_APPROVE = os.environ.get("AUTO_APPROVE", "True").lower() == "true"
ENABLE_AISPELL = os.environ.get("ENABLE_AISPELL", "True").lower() == "true"
ENABLE_CAM_PRE_DVD_DELETE = os.environ.get("ENABLE_CAM_PRE_DVD_DELETE", "True").lower() == "true"
ENABLE_MOST_SEARCHED = os.environ.get("ENABLE_MOST_SEARCHED", "True").lower() == "true"
ENABLE_TRENDING_POST = os.environ.get("ENABLE_TRENDING_POST", "True").lower() == "true"

# ✅ Broadcast Toggles
ENABLE_USER_BROADCAST = os.environ.get("ENABLE_USER_BROADCAST", "True").lower() == "true"
ENABLE_GROUP_BROADCAST = os.environ.get("ENABLE_GROUP_BROADCAST", "True").lower() == "true"

# ✅ Logging & Debug
LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", 0))
DEBUG_MODE = os.environ.get("DEBUG_MODE", "False").lower() == "true"

