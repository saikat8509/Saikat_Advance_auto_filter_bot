# templates/referral_template.py

from config import REFERRAL_REWARD_DAYS

def get_referral_template(referral_link: str, referral_count: int):
    return (
        "<b>🎁 Earn Premium for Free!</b>\n\n"
        f"<b>🔗 Your Referral Link:</b>\n<code>{referral_link}</code>\n\n"
        f"<b>📨 Send this to your friends. When they buy premium using your link, "
        f"you earn <u>{REFERRAL_REWARD_DAYS} days</u> of premium for each!</b>\n\n"
        f"<b>👥 Total Referrals:</b> <code>{referral_count}</code>\n\n"
        "💡 Tip: The more you refer, the more premium you earn!"
    )
