# bot/filters/command_filter.py

from aiogram.filters import Command
from aiogram.types import Message
from config import COMMAND_PREFIXES


class CustomCommand(Command):
    def __init__(self, *commands):
        super().__init__(*commands, prefix=COMMAND_PREFIXES)


async def is_command(message: Message) -> bool:
    if message.text:
        for prefix in COMMAND_PREFIXES:
            if message.text.startswith(prefix):
                return True
    return False

