# database/file_data.py

from database.connection import get_active_db
import re

db = get_active_db()
files_collection = db.files


async def save_file(file_id, file_name, file_size, mime_type, chat_id, season=None, year=None, quality=None, lang=None):
    existing = await files_collection.find_one({"file_id": file_id})
    if existing:
        return

    data = {
        "file_id": file_id,
        "file_name": file_name,
        "file_size": file_size,
        "mime_type": mime_type,
        "chat_id": chat_id,
        "season": season,
        "year": year,
        "quality": quality,
        "language": lang,
    }
    await files_collection.insert_one(data)


async def get_files_by_query(query):
    regex = re.compile(f".*{re.escape(query)}.*", re.IGNORECASE)
    cursor = files_collection.find({"file_name": regex})
    return await cursor.to_list(length=100)


async def delete_files_by_keywords(keywords):
    """
    Used for PreDVD / CamRip Delete Mode.
    Example: keywords = ["predvd", "camrip", "hdcam"]
    """
    pattern = "|".join([re.escape(word) for word in keywords])
    regex = re.compile(pattern, re.IGNORECASE)
    result = await files_collection.delete_many({"file_name": regex})
    return result.deleted_count


async def get_total_files():
    return await files_collection.count_documents({})


async def delete_files_by_chat(chat_id):
    return await files_collection.delete_many({"chat_id": chat_id})


async def clear_all_files():
    return await files_collection.delete_many({})
