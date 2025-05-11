# database/chat_data.py

from database import get_active_db

chats_col = get_active_db().chats

async def add_chat(chat_id: int, title: str = None):
    chat_data = {
        "_id": chat_id,
        "title": title or "",
        "is_disabled": False,
        "auto_welcome": True,
        "auto_goodbye": True,
        "auto_wishes": True,
        "filter_enabled": True
    }
    await chats_col.update_one({"_id": chat_id}, {"$setOnInsert": chat_data}, upsert=True)

async def get_all_chats():
    return [chat["_id"] async for chat in chats_col.find()]

async def get_chat(chat_id: int) -> dict:
    return await chats_col.find_one({"_id": chat_id})

async def delete_chat(chat_id: int):
    await chats_col.delete_one({"_id": chat_id})

async def disable_chat(chat_id: int):
    await chats_col.update_one({"_id": chat_id}, {"$set": {"is_disabled": True}})

async def enable_chat(chat_id: int):
    await chats_col.update_one({"_id": chat_id}, {"$set": {"is_disabled": False}})

async def is_chat_disabled(chat_id: int) -> bool:
    chat = await get_chat(chat_id)
    return chat.get("is_disabled", False) if chat else False

async def set_welcome(chat_id: int, status: bool):
    await chats_col.update_one({"_id": chat_id}, {"$set": {"auto_welcome": status}})

async def set_goodbye(chat_id: int, status: bool):
    await chats_col.update_one({"_id": chat_id}, {"$set": {"auto_goodbye": status}})

async def set_wishes(chat_id: int, status: bool):
    await chats_col.update_one({"_id": chat_id}, {"$set": {"auto_wishes": status}})

async def toggle_filter(chat_id: int, status: bool):
    await chats_col.update_one({"_id": chat_id}, {"$set": {"filter_enabled": status}})

async def is_filter_enabled(chat_id: int) -> bool:
    chat = await get_chat(chat_id)
    return chat.get("filter_enabled", True) if chat else True

async def get_active_chat_count():
    return await chats_col.count_documents({"is_disabled": False})
