# bot/plugins/__init__.py

"""
This file is intentionally kept for plugin-level initializations.

You can use this space to:
- Register shared plugin-level variables/constants
- Import all plugin modules (optional)
- Initialize plugin-level utilities (e.g., a shared logger)
"""

# Example: Importing plugin submodules so they're always loaded
from . import url_shortener

# Optionally, preload/initialize something globally (like a logger)
import logging

logger = logging.getLogger("bot.plugins")
logger.setLevel(logging.INFO)

# If needed, attach default handler
if not logger.hasHandlers():
    from logging import StreamHandler
    handler = StreamHandler()
    logger.addHandler(handler)

logger.info("✅ bot.plugins initialized successfully.")
