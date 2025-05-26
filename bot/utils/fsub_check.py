# bot/utils/fsub_check.py

from pyrogram import Client
from pyrogram.errors import UserNotParticipant
from config import AUTO_APPROVE, ADMINS
from bot.utils.database import get_required_channels

async def check_user_subscription(client: Client, user_id: int) -> bool:
    """
    Check if the user has joined all required Force Subscribe channels.
    Returns True if subscribed to all, False otherwise.
    """
    channels = await get_required_channels()

    for channel in channels:
        try:
            member = await client.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ("left", "kicked"):
                return False
        except UserNotParticipant:
            return False
        except Exception:
            continue  # Fail silently and skip channel if bot isn't admin

    return True

async def verify_subscription(client: Client, user_id: int, bypass_admin: bool = True) -> tuple[bool, list]:
    """
    Verifies whether the user is subscribed to all required channels.
    Returns a tuple (status, unsubscribed_channels).
    """
    unsubscribed_channels = []
    channels = await get_required_channels()

    if bypass_admin and user_id in ADMINS:
        return True, []

    for channel in channels:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status in ("left", "kicked"):
                unsubscribed_channels.append(channel)
        except UserNotParticipant:
            unsubscribed_channels.append(channel)
        except Exception:
            continue

    return (len(unsubscribed_channels) == 0), unsubscribed_channels

async def auto_approve_user_if_enabled(client: Client, user_id: int):
    """
    Automatically allow user to use bot if AUTO_APPROVE is enabled and user is subscribed.
    """
    if not AUTO_APPROVE:
        return False

    is_subscribed = await check_user_subscription(client, user_id)
    return is_subscribed
