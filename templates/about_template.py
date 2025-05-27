from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_USERNAME, SUPPORT_GROUP_URL, MOVIE_GROUP_URL

ABOUT_IMAGE_URL = "https://graph.org/file/b31d7bc58c555fa3c62a5.jpg"  # Update this URL as needed

ABOUT_TEXT = """
🤖 **Bot Name:** Princess Surch Bot

🧠 **Developed By:** [Leazy Boy](https://t.me/{owner})

📣 **Update Channel:** [Click Here](https://t.me/creazy_announcement_hub)
🎥 **Movie Group:** [Join Us](https://t.me/Creazy_Movie_Surch_Group)
💬 **Support Group:** [Get Help](https://t.me/Leazy_support_group)

🔗 **Source Code:** Private
🛠️ **Features:**
- Advanced Autofilter
- IMDb Integration
- Premium Membership
- Token-Based Short Link
- Referral System
- Trending & Popular Sections
- Screenshot AI Payment Verification

💎 **Premium Includes:**
- No Ads / Instant Download
- Direct File Access
- Unlimited Movies/Series
- Full Admin Support

✨ Enjoy smart searching and lightning-fast results!
""".format(owner=OWNER_USERNAME)

ABOUT_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("👑 Owner", url=f"https://t.me/{OWNER_USERNAME}"),
        InlineKeyboardButton("💬 Support Group", url=SUPPORT_GROUP_URL),
    ],
    [
        InlineKeyboardButton("🎬 Movie Group", url=MOVIE_GROUP_URL),
        InlineKeyboardButton("⬅️ Back", callback_data="start_menu")
    ]
])

def get_about_template():
    return ABOUT_IMAGE_URL, ABOUT_TEXT, ABOUT_BUTTONS
