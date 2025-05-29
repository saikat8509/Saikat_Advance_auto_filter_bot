# bot/utils/premium.py

from datetime import datetime, timedelta
from config import PREMIUM_PLANS, REFERRAL_REWARD_DAYS, TRIAL_DURATION_DAYS
from .database import get_user, save_user, get_all_users

# Get current UTC time
def now():
    return datetime.utcnow()

# Checks if a user is a premium member
def is_premium_user(user_id: int) -> bool:
    user = get_user(user_id)
    if not user:
        return False
    expiry = user.get("premium_expiry")
    return expiry and datetime.fromisoformat(expiry) > now()

# Grant premium plan to user
def grant_premium(user_id: int, plan_days: int):
    user = get_user(user_id) or {"user_id": user_id}
    current_expiry = datetime.fromisoformat(user["premium_expiry"]) if user.get("premium_expiry") else now()
    new_expiry = max(current_expiry, now()) + timedelta(days=plan_days)
    user["premium_expiry"] = new_expiry.isoformat()
    save_user(user)

# Revoke premium access from user
def revoke_premium(user_id: int):
    user = get_user(user_id)
    if user and "premium_expiry" in user:
        del user["premium_expiry"]
        save_user(user)

# Grant free trial to a user (once only)
def grant_trial(user_id: int):
    user = get_user(user_id) or {"user_id": user_id}
    if user.get("trial_used"):
        return False
    expiry = now() + timedelta(days=TRIAL_DURATION_DAYS)
    user["premium_expiry"] = expiry.isoformat()
    user["trial_used"] = True
    save_user(user)
    return True

# Grant referral reward to inviter
def reward_referral(inviter_id: int):
    inviter = get_user(inviter_id) or {"user_id": inviter_id}
    current_expiry = datetime.fromisoformat(inviter["premium_expiry"]) if inviter.get("premium_expiry") else now()
    new_expiry = max(current_expiry, now()) + timedelta(days=REFERRAL_REWARD_DAYS)
    inviter["premium_expiry"] = new_expiry.isoformat()
    inviter["referral_count"] = inviter.get("referral_count", 0) + 1
    save_user(inviter)

# Get user's current plan info
def get_user_plan(user_id: int) -> str:
    user = get_user(user_id)
    if not user:
        return "❌ Not found"
    expiry = user.get("premium_expiry")
    if not expiry:
        return "🔒 Free user"
    expiry_dt = datetime.fromisoformat(expiry)
    remaining = (expiry_dt - now()).days
    if remaining < 0:
        return "🔒 Free user (Expired)"
    return f"🌟 Premium (valid for {remaining} days)"

# List all active premium users (for admin stats)
def get_all_premium_users():
    all_users = get_all_users()
    return [
        user for user in all_users
        if user.get("premium_expiry") and datetime.fromisoformat(user["premium_expiry"]) > now()
    ]

# Checks if a user has already used a trial
def trial_used(user_id: int) -> bool:
    user = get_user(user_id)
    return user.get("trial_used", False) if user else False

# Get referral count for a user
def get_referral_count(user_id: int) -> int:
    user = get_user(user_id)
    return user.get("referral_count", 0) if user else 0
