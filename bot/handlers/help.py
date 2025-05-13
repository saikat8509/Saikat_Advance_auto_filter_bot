# bot/handlers/help.py

from pyrogram import filters, Client
from pyrogram.types import Message
from config import ADMINS
from utils.helpers import is_admin

HELP_TEXT = """
<b>🤖 Bot Command Help</b>

<b>👥 Public Commands:</b>
/start - Show welcome and navigation buttons
/help - Show this help message
/plan - View premium membership plans
/buy - Instructions for buying premium
/myplan - View your current plan & expiry
/referral - Get your referral link & bonuses

<b>🔍 Search:</b>
Just send the movie name in the group or bot. The bot will filter and reply with matching results, IMDb info & files.

<b>⚙️ Admin Commands:</b>
/addchannel [channel_id] - Add new DB channel
/delchannel [channel_id] - Remove DB channel
/enable [feature] - Enable features like fsub, shortener etc.
/disable [feature] - Disable features
/setwelcome - Set custom welcome message
/setgoodbye - Set custom goodbye message
/setimdbtemplate - Set custom IMDb template
/broadcast - Broadcast message to all users
/leave [chat_id] - Make bot leave a group or channel
/ban [user_id] - Ban user
/unban [user_id] - Unban user
/prem [user_id] [days] - Grant premium manually
/unprem [user_id] - Remove premium
/reload - Reload all config and DB

<b>📊 Stats:</b>
/stats - Show MongoDB usage, total files & connected DBs

<b>💡 Notes:</b>
- File shortener auto disables for premium users or verified token users.
- Trending & New files auto-post to configured channels.
- "Movie Link" buttons redirect users to group.
- Add this bot to your groups/channels with proper admin rights.

"""

@Client.on_message(filters.command("help") & filters.private)
async def help_command(client, message: Message):
    if not await is_admin(message.from_user.id):
        await message.reply_text("🔐 This help section is only for admins.\n\nUse /start for basic help.")
        return
    await message.reply_text(
        HELP_TEXT,
        disable_web_page_preview=True
    )

