from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID, SUPPORT_GROUP, MOVIE_GROUP, BOT_USERNAME
from bot.utils.buttons import start_main_buttons
from bot.utils.tools import get_start_image


# /start command handler
@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    user = message.from_user
    user_id = user.id

    start_image_url = get_start_image(user_id)

    welcome_text = f"""
👋 Hi [{user.first_name}](tg://user?id={user_id})!

Welcome to **Creazy Movie Surch Bot** — your ultimate movie search and download assistant. 🎥🍿

Use the buttons below to explore features, join our groups, or upgrade your experience with Premium Membership!

Feel free to ask for help anytime via the Help Menu.
"""

    # Send photo with caption and inline keyboard
    await message.reply_photo(
        photo=start_image_url,
        caption=welcome_text,
        reply_markup=start_main_buttons(),
        parse_mode="md",
    )


# Callback Query Handlers for ABOUT, PREMIUM, HELP MENU and nested buttons

@Client.on_callback_query(filters.regex("^about_cb$"))
async def about_callback(client: Client, callback_query):
    about_text = """
**Creazy Movie Surch Bot**

This bot helps you search and download movies easily with features like:

- Auto-filtering from multiple sources
- IMDb data integration
- Premium membership for direct downloads
- Referral system and trial plans
- Support and update channels

Created and maintained by [OWNER](tg://user?id={owner_id}).
"""
    about_buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("OWNER", url=f"https://t.me/{OWNER_ID}"),
                InlineKeyboardButton("SUPPORT GROUP", url=SUPPORT_GROUP),
            ],
            [
                InlineKeyboardButton("MOVIE GROUP", url=MOVIE_GROUP),
            ],
            [
                InlineKeyboardButton("BACK", callback_data="start_back_cb"),
            ],
        ]
    )
    await callback_query.message.edit_text(
        about_text.format(owner_id=OWNER_ID),
        reply_markup=about_buttons,
        parse_mode="md",
        disable_web_page_preview=True,
    )
    await callback_query.answer()


@Client.on_callback_query(filters.regex("^premium_referral_cb$"))
async def premium_referral_callback(client: Client, callback_query):
    premium_text = """
**Premium Membership & Referral**

Upgrade for:

- Ads-free experience
- Direct downloads
- Fast support
- Exclusive trial plans

Earn rewards by inviting friends!

Choose an option below.
"""
    premium_buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("PREMIUM PLANS", callback_data="premium_plans_cb"),
                InlineKeyboardButton("REFERRAL", callback_data="referral_cb"),
            ],
            [
                InlineKeyboardButton("TAKE TRIAL", callback_data="take_trial_cb"),
                InlineKeyboardButton("BACK", callback_data="start_back_cb"),
            ],
        ]
    )
    await callback_query.message.edit_text(
        premium_text,
        reply_markup=premium_buttons,
        parse_mode="md",
    )
    await callback_query.answer()


@Client.on_callback_query(filters.regex("^premium_plans_cb$"))
async def premium_plans_callback(client: Client, callback_query):
    plans_text = """
**Premium Plans**

- 1 Week - ₹50
- 1 Month - ₹150
- 3 Months - ₹400

UPI ID: `yourupi@bank`

Check your active plan with /myplan

Proof of payments: [Payments Channel](https://t.me/creazy_payments_proof)

Send payment screenshot to @Leazy_Boy for activation.
"""
    plans_buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("SEND PAYMENT SCREENSHOT", url="https://t.me/Leazy_Boy"),
            ],
            [
                InlineKeyboardButton("BACK", callback_data="premium_referral_cb"),
                InlineKeyboardButton("HOME", callback_data="start_back_cb"),
            ],
        ]
    )
    await callback_query.message.edit_text(
        plans_text,
        reply_markup=plans_buttons,
        parse_mode="md",
        disable_web_page_preview=True,
    )
    await callback_query.answer()


@Client.on_callback_query(filters.regex("^referral_cb$"))
async def referral_callback(client: Client, callback_query):
    user_id = callback_query.from_user.id
    referral_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
    referral_count = 0  # Placeholder

    referral_text = f"""
**Referral Program**

Invite friends and earn points!

Your referral link:
`{referral_link}`

Total referrals: ⌛ {referral_count}
"""

    referral_buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("COPY LINK", url=referral_link),
                InlineKeyboardButton("⌛ Referrals", callback_data="referral_count_cb"),
            ],
            [
                InlineKeyboardButton("BACK", callback_data="premium_referral_cb"),
            ],
        ]
    )
    await callback_query.message.edit_text(
        referral_text,
        reply_markup=referral_buttons,
        parse_mode="md",
    )
    await callback_query.answer()


@Client.on_callback_query(filters.regex("^take_trial_cb$"))
async def take_trial_callback(client: Client, callback_query):
    trial_text = """
**Trial Plan**

Get a free trial premium membership for 1 day!

Contact @Leazy_Boy to activate your trial.

Enjoy exclusive benefits and fast downloads.
"""
    trial_buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("BACK", callback_data="premium_referral_cb"),
                InlineKeyboardButton("HOME", callback_data="start_back_cb"),
            ],
        ]
    )
    await callback_query.message.edit_text(
        trial_text,
        reply_markup=trial_buttons,
        parse_mode="md",
    )
    await callback_query.answer()


@Client.on_callback_query(filters.regex("^help_menu_cb$"))
async def help_menu_callback(client: Client, callback_query):
    help_text = """
**Admin Commands Help Menu**

/start - Start bot
/help - Show help
/spellcheck - Spell check text
/imdb - IMDb movie search
/popular - Show popular movies
/premium - Premium membership info
/referral - Referral info
/myplan - Show your premium plan
/addpremium - Add premium user (admin only)
/removepremium - Remove premium user (admin only)
/stats - Bot usage statistics
... and many more.
"""
    help_buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("BACK", callback_data="start_back_cb"),
            ]
        ]
    )
    await callback_query.message.edit_text(
        help_text,
        reply_markup=help_buttons,
        parse_mode="md",
    )
    await callback_query.answer()


@Client.on_callback_query(filters.regex("^start_back_cb$"))
async def start_back_callback(client: Client, callback_query):
    user_id = callback_query.from_user.id
    start_image_url = get_start_image(user_id)
    welcome_text = f"""
👋 Hi [{callback_query.from_user.first_name}](tg://user?id={user_id})!

Welcome to **Creazy Movie Surch Bot** — your ultimate movie search and download assistant. 🎥🍿

Use the buttons below to explore features, join our groups, or upgrade your experience with Premium Membership!

Feel free to ask for help anytime via the Help Menu.
"""
    await callback_query.message.edit_media(
        media=start_image_url,
        reply_markup=start_main_buttons(),
        caption=welcome_text,
        parse_mode="md"
    )
    await callback_query.answer()
