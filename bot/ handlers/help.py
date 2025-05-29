from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMIN_ID

HELP_TEXT = """
**🛠️ Admin Help Menu 🛠️**

Here are the available admin commands:

🔹 `/addpremium <user_id> <days>`  
‣ Manually grant premium to a user for specific days.

🔹 `/removepremium <user_id>`  
‣ Revoke premium access from a user.

🔹 `/myplan`  
‣ Let a user check their active premium plan and expiry.

🔹 `/broadcast <message>`  
‣ Send a message to all users (admin only).

🔹 `/stats`  
‣ Get total user count and active premium users.

🔹 `/referralstats`  
‣ Show referral points of a user.

🔹 `/settrial <minutes>`  
‣ Set free trial duration for new users.

🔹 `/popular`  
‣ Show popular movies/files.

🔹 `/trending`  
‣ Show trending searches based on user activity.

🔹 `/imdb <movie name>`  
‣ Fetch IMDb details for a movie or series.

🔹 `/setwelcome`  
‣ Update the welcome message and image.

🔹 `/setgoodbye`  
‣ Update the goodbye message and image.

🔹 `/addfsub @channelusername`  
‣ Add a Force Subscribe channel.

🔹 `/rmfsub @channelusername`  
‣ Remove a Force Subscribe channel.

🔹 `/fsubtoggle`  
‣ Toggle Force Subscribe on/off.

🔹 `/popularchannel @channelusername`  
‣ Set the channel for "Popular" section.

🔹 `/trendingchannel @channelusername`  
‣ Set the channel for "Trending" section.
"""

@Client.on_message(filters.command(["help"]) & filters.private)
async def show_help(client: Client, message: Message):
    await message.reply_photo(
        photo="https://graph.org/file/056e9629b0ff9882d7ab6.jpg",  # Replace with your stylish help image
        caption=HELP_TEXT,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔙 Back", callback_data="back_to_start")
            ],
            [
                InlineKeyboardButton("👤 Admin", user_id=ADMIN_ID),
                InlineKeyboardButton("📢 Support", url="https://t.me/Leazy_support_group")
            ]
        ])
    )
