# Telegram Bot Token
BOT_TOKEN=123456789:ABCDEFyourbottokenhere

# MongoDB connection string
MONGO_URI=mongodb+srv://user:password@cluster0.mongodb.net/mydatabase?retryWrites=true&w=majority

# Admin Telegram Usernames or IDs (comma separated)
ADMINS=123456789,987654321

# Owner username (without @)
OWNER_USERNAME=Leazy_Boy

# Tutorial channel URL for "How To Download" button
TUTORIAL_CHANNEL_URL=https://t.me/How_to_open_file_to_link

# Payment proof channel URL (shows payment screenshots for user trust)
PAYMENT_PROOF_CHANNEL_URL=https://t.me/creazy_payments_proof

# Force Subscribe channels (comma separated usernames without @)
FORCE_SUBSCRIBE_CHANNELS=creazy_announcement_hub,Leazy_support_group

# Welcome and Goodbye images (graph.org URLs)
WELCOME_IMAGE_URL=https://graph.org/file/yourwelcomeimage.jpg
GOODBYE_IMAGE_URL=https://graph.org/file/yourgoodbyeimage.jpg

# Wish images (morning, afternoon, evening, night) graph.org URLs
WISH_MORNING_IMAGE_URL=https://graph.org/file/morning.jpg
WISH_AFTERNOON_IMAGE_URL=https://graph.org/file/afternoon.jpg
WISH_EVENING_IMAGE_URL=https://graph.org/file/evening.jpg
WISH_NIGHT_IMAGE_URL=https://graph.org/file/night.jpg

# Start command rotating images (space separated graph.org URLs)
START_IMAGES=https://graph.org/file/image1.jpg https://graph.org/file/image2.jpg https://graph.org/file/image3.jpg

# Referral reward days for premium (integer)
REFERRAL_REWARD_DAYS=3

# Premium plans days and prices (space separated days and prices respectively)
PREMIUM_DAYS_OPTIONS=7 15 30 90
PREMIUM_PRICE_OPTIONS=70 150 300 900

# Enable AI screenshot payment verification (true/false)
ENABLE_SCREENSHOT_AI=False

# OCR provider to use ("tesseract" or "google")
OCR_PROVIDER=tesseract

# URL shortener API keys mapping in JSON format
# Example: '{"shortzon":"API_KEY_HERE","try2link":"API_KEY_HERE"}'
SHORTENER_APIS_JSON={"shortzon":"your_shortzon_api_key","try2link":"your_try2link_api_key"}

# Port for deployment (default 8080)
PORT=8080
