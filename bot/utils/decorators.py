import functools
import logging
from typing import Callable, Any, Coroutine
from telegram import Update
from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)


def log_errors(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Coroutine[Any, Any, Any]]:
    """
    Decorator to log exceptions from async handler functions.
    """
    @functools.wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        try:
            return await func(update, context, *args, **kwargs)
        except Exception as e:
            user = update.effective_user
            logger.error(f"Exception in handler {func.__name__} for user {user.id if user else 'unknown'}: {e}", exc_info=True)
            # Optionally notify user or admin here
            # await update.message.reply_text("An unexpected error occurred. Please try again later.")
    return wrapper


def admin_only(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Coroutine[Any, Any, Any]]:
    """
    Decorator to restrict access to bot admins only.
    Requires context.bot_data['admins'] to be set with a list of user IDs.
    """
    @functools.wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id if update.effective_user else None
        admins = context.bot_data.get("admins", [])
        if user_id not in admins:
            if update.effective_message:
                await update.effective_message.reply_text("❌ You are not authorized to use this command.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


def restricted(allowed_user_ids: set):
    """
    Decorator factory that restricts command usage to specific user IDs.
    Usage:
        @restricted({123456789, 987654321})
        async def some_handler(update, context):
            ...
    """
    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
        @functools.wraps(func)
        async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
            user_id = update.effective_user.id if update.effective_user else None
            if user_id not in allowed_user_ids:
                if update.effective_message:
                    await update.effective_message.reply_text("❌ You don't have permission to use this command.")
                return
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator


def async_wrap(func: Callable) -> Callable[..., Coroutine[Any, Any, Any]]:
    """
    Utility decorator to wrap sync functions to async coroutines.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
