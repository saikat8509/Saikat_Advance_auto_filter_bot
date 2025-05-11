# bot/__init__.py

"""
AutoFilter Bot — Telegram File Indexer & Search Bot

This initializer file marks the 'bot' directory as a Python package.
It optionally preloads key components used across the entire bot structure.
"""

import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging Configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Import essential bot submodules
from . import handlers            # All message/callback/command handlers
from . import database            # MongoDB connection and CRUD logic
from . import templates           # Custom button layouts and message templates
from . import utils               # Helper functions: IMDB, Spelling, Shorteners, etc.
from . import config              # Loaded via os.environ
