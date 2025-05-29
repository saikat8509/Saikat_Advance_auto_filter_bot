# bot/utils/premium.py

from bot.utils.database import get_user  # Assuming you have this function in database.py
from config import PREMIUM_PLANS

def get_premium_prompt():
    """
    Returns a premium membership prompt text.
    Customize this text or template for your bot.
    """
    prompt = (
        "🔥 **Premium Membership Benefits:**\n"
        "- Ad-free usage\n"
        "- Faster downloads\n"
        "- Direct file access\n\n"
        "💰 **Available Plans:**\n"
    )
    for plan_id, plan in PREMIUM_PLANS.items():
        prompt += f"• {plan['label']}: ₹{plan['price']} for {plan['days']} days\n"
    prompt += (
        "\nSend your payment screenshot to @Leazy_Boy for verification.\n"
        "Use /myplan to check your active subscription.\n"
    )
    return prompt


def is_user_premium(user_id: int) -> bool:
    """
    Check if a user is premium by querying the database.
    """
    user = get_user(user_id)
    if user and user.get("is_premium", False):
        return True
    return False


def get_user_plan_details(user_id: int):
    """
    Retrieve the user's current premium plan details from the database.
    """
    user = get_user(user_id)
    if not user or not user.get("is_premium"):
        return None

    plan_id = user.get("premium_plan_id")
    if plan_id and plan_id in PREMIUM_PLANS:
        return PREMIUM_PLANS[plan_id]

    return None


def get_premium_features_list():
    """
    Returns a list or formatted string of premium features.
    """
    features = [
        "⚡ Ad-free experience",
        "⚡ Unlimited downloads",
        "⚡ High-speed file access",
        "⚡ Priority support",
        "⚡ Access to exclusive content",
    ]
    return "\n".join(features)


def premium_welcome_message(user_name: str):
    """
    Generate a welcome message for premium users.
    """
    return (
        f"Welcome back, {user_name}! 🎉\n"
        "Thank you for being a Premium member.\n"
        "Enjoy your enhanced experience!"
    )
