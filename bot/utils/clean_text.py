
import re
from html import unescape

def clean_text(text: str) -> str:
    """
    Clean up input text by:
    - Unescaping HTML entities
    - Removing extra whitespaces
    - Removing Telegram markdown special characters to prevent formatting issues
    - Removing URLs
    - Stripping leading/trailing spaces
    
    Args:
        text (str): Raw input text
    
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Unescape HTML entities like &amp;, &lt;, &gt;, etc.
    text = unescape(text)

    # Remove URLs (http, https, t.me, telegram links, etc.)
    url_pattern = re.compile(r"https?://\S+|t\.me/\S+")
    text = url_pattern.sub("", text)

    # Remove Telegram markdown special characters that might break formatting
    # Telegram uses *, _, `, [, ], (, ), ~, >, #, +, -, =, |, {, }, ., !
    # We'll remove those that are not likely part of normal text.
    markdown_special_chars = r"[*_`\[\]()~>#+\-=|{}.!]"
    text = re.sub(markdown_special_chars, "", text)

    # Replace multiple spaces/newlines with a single space
    text = re.sub(r"\s+", " ", text)

    # Strip leading/trailing spaces
    return text.strip()


def clean_filename(filename: str) -> str:
    """
    Clean a filename by removing illegal characters for file systems
    and trimming extra spaces.
    
    Args:
        filename (str): Raw filename string
    
    Returns:
        str: Cleaned filename
    """
    if not filename:
        return "file"

    # Remove characters not allowed in filenames on Windows, macOS, Linux
    # For simplicity, remove: <>:"/\|?* and control chars
    filename = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename)

    # Replace multiple spaces with single space
    filename = re.sub(r"\s+", " ", filename)

    # Strip leading/trailing spaces and dots (dots at end can cause issues)
    filename = filename.strip(" .")

    # Fallback default name if empty after cleaning
    if not filename:
        return "file"

    return filename


def remove_telegram_markdown(text: str) -> str:
    """
    Remove Telegram markdown formatting from a string.
    This can help to prevent markdown injection issues.
    
    Args:
        text (str): Input text
    
    Returns:
        str: Text without markdown formatting characters
    """
    if not text:
        return ""

    # Remove Telegram markdown symbols
    markdown_chars = r"[*_`\[\]()~>#+\-=|{}.!]"
    return re.sub(markdown_chars, "", text).strip()

                                                                            bot/utils/database.py

from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
from datetime import datetime, timedelta

client = AsyncIOMotorClient(MONGO_DB_URI)
db = client.autofilter_bot

# === COLLECTIONS ===
users_col = db.users
searches_col = db.searches
premium_col = db.premium
referrals_col = db.referrals

# === USER FUNCTIONS ===
async def add_user(user_id: int):
    await users_col.update_one({"_id": user_id}, {"$setOnInsert": {"joined": datetime.utcnow()}}, upsert=True)

async def total_users() -> int:
    return await users_col.count_documents({})

# === PREMIUM FUNCTIONS ===
async def is_premium_user(user_id: int) -> bool:
    user = await premium_col.find_one({"_id": user_id})
    if user and "expiry" in user:
        return datetime.utcnow() < user["expiry"]
    return False

async def count_premium_users() -> int:
    return await premium_col.count_documents({"expiry": {"$gt": datetime.utcnow()}})

async def count_trial_users() -> int:
    return await premium_col.count_documents({"trial": True})

async def add_premium_user(user_id: int, duration_days: int, is_trial=False):
    expiry = datetime.utcnow() + timedelta(days=duration_days)
    await premium_col.update_one(
        {"_id": user_id},
        {"$set": {"expiry": expiry, "trial": is_trial}},
        upsert=True
    )

# === REFERRAL FUNCTIONS ===
async def add_referral(referrer_id: int, referred_id: int):
    await referrals_col.insert_one({
        "referrer": referrer_id,
        "referred": referred_id,
        "timestamp": datetime.utcnow()
    })

async def total_referred_users(referrer_id: int) -> int:
    return await referrals_col.count_documents({"referrer": referrer_id})

async def total_referral_count() -> int:
    return await referrals_col.count_documents({})

# === SPELLING / SIMILAR SEARCH ===
async def get_similar_queries(query: str) -> list:
    # Basic regex based search
    cursor = searches_col.find({"query": {"$regex": query, "$options": "i"}}).limit(10)
    results = []
    async for doc in cursor:
        results.append(doc["query"])
    return results

async def log_search(user_id: int, query: str):
    await searches_col.insert_one({
        "user_id": user_id,
        "query": query,
        "timestamp": datetime.utcnow()
    })

