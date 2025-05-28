# Import all handlers to ensure they are registered when the bot starts
from .handlers import (
    start,
    help,
    about,
    premium,
    referral,
    verify,
    filters,
    imdb,
    requests,
    trending,
    popular,
    wishes,
    welcome,
    force_subscribe,
    admin,
    payment_screenshot
)
