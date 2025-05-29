# bot/handlers/__init__.py

# 1. Autofilter Search
from . import filter

# 2. Inline Mode
# (Handled within filter.py as inline_query handlers)

# 3. Formats (.mkv, .mp4, .avi)
# (Handled within filter.py)

# 4. /start with rotating image + welcome message
from . import start

# 5. Goodbye, Welcome, Static Wishes
from . import wishes

# 6. Admin Commands
from . import admin

# 7. Premium System: add/remove, /myplan
from . import premium

# 8. Force Subscribe (Multi-channel, Toggle, Auto Approve)
from . import force_subscribe

# 9. Batch + Link Generator (if implemented)
# from . import batch

# 10. IMDb Template, Year Buttons
from . import imdb

# 11. Trending Section (based on DB search)
from . import trending

# 12. Popular Section (by downloads/views/admin-pick)
from . import popular

# 13. Help Command List (for /start Help Menu)
from . import help

# 14. Referral System
from . import referral

# 15. AI Spell Check on user search (if implemented)
# from . import ai_spellcheck

# 16. Token Shortlink Handler (if implemented)
# from . import shortlink

# 17. URL Shortener + How to Download Tutorial (if implemented)
# from . import tutorial

# 18. Payment Screenshot AI Verification
from . import payment_screenshot
