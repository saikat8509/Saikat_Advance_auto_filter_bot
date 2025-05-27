# templates/premium_template.py

from config import (
    PREMIUM_HEADER,
    PREMIUM_FEATURES,
    PREMIUM_FOOTER,
    PREMIUM_PLANS,
    OWNER_USERNAME,
    PAYMENT_PROOF_CHANNEL_URL
)


def get_premium_template():
    plans_text = ""
    plan_icons = ["🔹", "🔸", "🌟", "💫", "🚀", "✨"]
    for i, (days, details) in enumerate(sorted(PREMIUM_PLANS.items())):
        icon = plan_icons[i % len(plan_icons)]
        plans_text += f"<b>{icon} {details['label']}:</b> ₹{details['price']}\n"

    return (
        f"{PREMIUM_HEADER}\n\n"
        f"<b>💳 Available Plans:</b>\n"
        f"{plans_text}\n"
        f"<b>📢 Payment UPI ID:</b> <code>creazy@upi</code>\n"
        f"<b>📂 Check your active plan:</b> /myplan\n"
        f"<b>📸 Payment Proof Channel:</b> {PAYMENT_PROOF_CHANNEL_URL}\n\n"
        f"{PREMIUM_FEATURES}\n\n"
        f"{PREMIUM_FOOTER}"
    )
