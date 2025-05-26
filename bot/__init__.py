# bot/__init__.py

from . import handlers
from . import plugins
from . import utils

# Handlers
from .handlers import (
    help,
    imdb,
    popular,
    premium,
    spelling,
    start,
    stats,
    trending,
    wishes
)

# Plugins
from .plugins import (
    referral,
    screenshot,
    shorten,
    url_shortener
)

# Utils
from .utils import (
    ai_spellcheck,
    buttons,
    clean_text,
    database,
    decorators,
    fsub_check,
    time_based
)

__all__ = [
    "handlers",
    "plugins",
    "utils",
    "help",
    "imdb",
    "popular",
    "premium",
    "spelling",
    "start",
    "stats",
    "trending",
    "wishes",
    "referral",
    "screenshot",
    "shorten",
    "url_shortener",
    "ai_spellcheck",
    "buttons",
    "clean_text",
    "database",
    "decorators",
    "fsub_check",
    "time_based"
]
