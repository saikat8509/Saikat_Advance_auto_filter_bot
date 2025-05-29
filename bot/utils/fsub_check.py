from telegram import Update, ChatMember, ChatMemberUpdated
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

# Example: force subscribe channel usernames or IDs from config, e.g.
# FORCE_SUB_CHANNELS = ["@channel1", "@channel2"] or [channel_id1, channel_id2]
# AUTO_APPROVE = True or False

async def is_user_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE, channels: list) -> bool:
    """
    Check if the user is a member of all given channels.
    Returns True if user is member of all, else False.
    """
    for channel in channels:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            # Check if user is not banned/kicked and is a member
            if member.status in [ChatMember.LEFT, ChatMember.BANNED, ChatMember.KICKED]:
                return False
        except Exception as e:
            logger.warning(f"Failed to get chat member for channel {channel} user {user_id}: {e}")
            return False
    return True


async def force_subscribe_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Checks if the user has joined all required force subscribe channels.
    Returns True if subscribed (passes check), False otherwise.
    If user is not subscribed, sends a message asking them to join.
    """
    user = update.effective_user
    chat = update.effective_chat

    if not user or not chat:
        return False  # Cannot verify

    channels = context.bot_data.get("force_sub_channels", [])
    auto_approve = context.bot_data.get("auto_approve", False)

    if not channels:
        # No force subscribe channels configured, allow access
        return True

    subscribed = await is_user_subscribed(user.id, context, channels)
    if subscribed:
        # If auto approve is enabled, approve the user in group (if applicable)
        if auto_approve and chat.type in ["group", "supergroup"]:
            try:
                await context.bot.approve_chat_join_request(chat.id, user.id)
            except Exception as e:
                logger.error(f"Failed to auto-approve join request for user {user.id}: {e}")
        return True
    else:
        # Ask user to join channels
        channel_links = "\n".join([f"➡️ <a href='{ch}'>Join {ch}</a>" for ch in channels])
        text = (
            "❗️ You must join the following channels before using this bot/group:\n\n"
            f"{channel_links}\n\n"
            "After joining, please try again."
        )
        if update.message:
            await update.message.reply_html(text, disable_web_page_preview=True)
        elif update.callback_query:
            await update.callback_query.answer(text, show_alert=True)
        return False


async def chat_member_update_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for ChatMemberUpdated updates.
    Automatically approves users who join required channels if auto_approve enabled.
    """
    chat_member_update: ChatMemberUpdated = update.chat_member
    user = chat_member_update.from_user
    chat = chat_member_update.chat
    new_status = chat_member_update.new_chat_member.status

    channels = context.bot_data.get("force_sub_channels", [])
    auto_approve = context.bot_data.get("auto_approve", False)

    if not auto_approve:
        return

    # Only process join requests in groups/supergroups
    if chat.type not in ["group", "supergroup"]:
        return

    # Check if this update is a join request approval opportunity
    # new_status can be 'member' (approved) or 'restricted' (pending approval)
    # Here, we approve if user joined a force sub channel.

    # This function is mainly for handling join request approvals if your bot manages group join requests.
    # If you want to auto approve group join requests after user joined force sub channels,
    # you must have logic to detect that.

    # Placeholder: This depends on your bot's usage of chat join requests.
    # You may implement according to your bot logic.

    pass
