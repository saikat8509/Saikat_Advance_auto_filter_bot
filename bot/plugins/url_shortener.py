import aiohttp
import random
from config import TOKEN_VERIFICATION, PREMIUM_HEADER, PREMIUM_FEATURES, PREMIUM_FOOTER
from bot.utils.database import is_premium_user
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def shorten_url(api_name: str, api_key: str, url: str) -> str:
    """
    Shorten a URL using the specified shortener service.
    """
    try:
        if api_name == "short2url":
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://short2url.in/api", params={"api": api_key, "url": url}) as resp:
                    data = await resp.json()
                    return data.get("shortenedUrl", url)

        elif api_name == "cuttly":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://cutt.ly/api/api.php", params={"key": api_key, "short": url}) as resp:
                    data = await resp.json()
                    return data.get("url", {}).get("shortLink", url)

        elif api_name == "tinyurl":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.tinyurl.com/create", headers={"Authorization": f"Bearer {api_key}"}, json={"url": url}) as resp:
                    data = await resp.json()
                    return data.get("data", {}).get("tiny_url", url)

        # Add more services here as needed

        return url
    except Exception as e:
        print(f"[Shortener Error] {e}")
        return url


async def get_shortened_link(user_id: int, url: str) -> (str, InlineKeyboardMarkup, str):
    """
    Returns the shortened link with premium message and buttons if user is not premium.
    """
    if await is_premium_user(user_id):
        return url, None, ""  # Direct link for premium

    # Non-premium user - apply token verification with shortener
    shortener_list = list(TOKEN_VERIFICATION.items())
    if not shortener_list:
        return url, None, ""

    selected_api = random.choice(shortener_list)
    api_name, api_key = selected_api
    shortened_url = await shorten_url(api_name, api_key, url)

    # Construct message and buttons
    message = f"<b>{PREMIUM_HEADER}</b>\n\n{PREMIUM_FEATURES}\n\n<b>{PREMIUM_FOOTER}</b>"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Buy Premium Membership", callback_data="show_premium")],
        [InlineKeyboardButton("📥 Download Now", url=shortened_url)],
        [InlineKeyboardButton("❓ How To Download", url="https://t.me/How_to_open_file_to_link")]
    ])

    return shortened_url, buttons, message
