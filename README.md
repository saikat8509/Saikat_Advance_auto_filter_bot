# Telegram Movie Autofilter Bot

A powerful Telegram bot for movie groups that indexes multiple movie database channels, filters movie files by search queries, integrates IMDb data, and offers premium membership with token verification, referral system, and AI-based payment screenshot verification.

---

## Features

### Core Features
- **Multi-Database Indexing**: Index movie files from multiple Telegram database channels.
- **Powerful Search**: Search by movie name, format (.mkv, .mp4, .avi), and more.
- **IMDb Integration**: Fetch detailed movie info, ratings, and posters from IMDb.
- **Auto Filter & Inline Mode**: Quickly filter movies inline or via commands.

### Premium Membership System
- **Direct Downloads for Premium Users**: Premium users get direct access without token verification.
- **Token Verification for Non-Premium Users**: Links are shortened and verified via token-based shortener APIs.
- **Multiple Shortener API Support**: Easily add or switch URL shortener APIs.
- **Auto Expiry**: Premium plans expire automatically after the set duration.
- **Referral Program**: Earn rewards for inviting friends.
- **Premium Plan Management**: Admin commands to add/remove premium users, check plans, and list all premium members.
- **Trial Plans**: Optional trial period for new users.

### Payment & Verification
- **AI-based Payment Screenshot Verification**:
  - Upload payment screenshots.
  - OCR extracts transaction details.
  - Automatic premium membership granting upon valid payment detection.
- **Admin Manual Verification & Notifications**.

### User Interaction
- **Rotating Start Images**: Stylish welcome images rotating on each /start.
- **Stylish Templates**: Premium info, referral, about, help, and error templates.
- **Force Subscribe**: Users must join configured channels before using the bot.
- **Welcome & Goodbye Messages** with dynamic images.
- **Auto Wish Messages**: Morning, afternoon, evening, and night wishes based on user timezone.
- **Trending & Popular Sections**: Based on file search and download stats.
- **Admin Panel & Help Menu**: Full suite of admin commands with buttons.

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/telegram-movie-autofilter-bot.git
cd telegram-movie-autofilter-bot

**Create and activate a virtual environment**
python3 -m venv venv
source venv/bin/activate   # Linux/MacOS
venv\Scripts\activate      # Windows

**Install dependencies**
pip install -r requirements.txt

**Configure environment variables**
API_ID=123456
API_HASH=your_api_hash
BOT_TOKEN=123456:ABCDEF
MONGO_DB_URI=mongodb+srv://user:password@cluster.mongodb.net/dbname
ADMIN_IDS=123456789,987654321
FORCE_SUBSCRIBE_CHANNELS=@channel1,@channel2
SHORTENER_APIS_JSON={"shortzon": "api_key", "try2link": "api_key"}
ENABLE_SCREENSHOT_AI=True
OCR_PROVIDER=tesseract
OWNER_USERNAME=@Leazy_Boy
PAYMENT_PROOF_CHANNEL_URL=https://t.me/creazy_payments_proof
# ...other settings

**Run the bot**
python -m bot

**Bot Commands**
User Commands
/start - Start the bot and see the welcome message.

/help - Show help menu.

/myplan - Check your premium plan status.

Inline search - Use inline mode to search movies quickly.

Admin Commands (Private Chat)
/addpremium [user_id] [days] - Add premium user.

/removepremium [user_id] - Remove premium user.

/setplan [user_id] [days] - Manually set or extend the premium plan.

/checkplan [user_id] - Check if user is premium.

/premiumusers - List all premium users.

/broadcast - Send message to all users.

/warn, /unwarn, /delwarn - Manage user warnings.

/ban, /unban - Ban or unban users.

/setimage - Set rotating images for start/about/welcome/goodbye/wish.

/toggle - Toggle bot features (ForceSub, Shortener, etc.).

/reward, /resetref - Manage referral points.


Contribution
Feel free to open issues or submit pull requests for new features or bug fixes.

License
MIT License

Contact
Owner: @Leazy_Boy

Support Group: https://t.me/Leazy_support_group

Updates Channel: https://t.me/creazy_announcement_hub

Movie Group: https://t.me/Creazy_Movie_Surch_Group


