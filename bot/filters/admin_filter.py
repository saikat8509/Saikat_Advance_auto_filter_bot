# bot/filters/admin_filter.py

from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import ADMIN_USERS

class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) in ADMIN_USERS

