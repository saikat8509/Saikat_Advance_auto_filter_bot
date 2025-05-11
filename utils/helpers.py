# utils/helpers.py

import re
import aiohttp
from difflib import get_close_matches
from config import OMDB_API_KEY, SPELL_CHECK_ENABLED
from database.stats_data import log_search_query


async def fetch_imdb_data(title: str):
    """Fetch IMDb data using OMDb API."""
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def generate_imdb_template(filtered_files):
    """
    Generates a styled IMDb-rich message for a list of filtered files.
    """
    message = "🎬 **Filtered Results:**\n\n"
    for file in filtered_files:
        message += f"**📌 Title:** {file.get('title', 'N/A')}\n"
        message += f"⭐ **Rating:** {file.get('rating', 'N/A')} | 🎭 **Genre:** {file.get('genre', 'N/A')}\n"
        message += f"📅 **Year:** {file.get('year', 'N/A')} | 🎞️ **Quality:** {file.get('quality', 'N/A')}\n"
        message += f"🔗 [IMDb Link]({file.get('imdb_url', 'https://www.imdb.com')})\n"
        message += f"🆔 File ID: `{file.get('file_id')}`\n\n"
    return message


async def spell_check_movie(query: str, all_titles: list):
    """
    AI-based movie name spell check using fuzzy matching or Google.
    """
    if not SPELL_CHECK_ENABLED or not all_titles:
        return query

    matches = get_close_matches(query, all_titles, n=1, cutoff=0.6)
    if matches:
        return matches[0]
    return query


def clean_title(title: str) -> str:
    """Removes unwanted symbols for search indexing."""
    return re.sub(r'[^\w\s]', '', title).strip().lower()


async def log_user_search(user_id: int, query: str):
    """Logs user search queries to the database for trending search tracking."""
    await log_search_query(user_id, query)


def get_time_wish():
    """Returns a time-based greeting."""
    from datetime import datetime

    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "🌅 Good Morning"
    elif 12 <= hour < 17:
        return "🌞 Good Afternoon"
    elif 17 <= hour < 21:
        return "🌇 Good Evening"
    else:
        return "🌙 Good Night"

