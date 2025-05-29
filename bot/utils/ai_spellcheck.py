# bot/utils/ai_spellcheck.py

import difflib
import logging
from typing import List, Optional

from bot.utils.database import get_all_keywords

logger = logging.getLogger(__name__)

async def get_close_matches_from_db(query: str, limit: int = 5) -> List[str]:
    """
    Return a list of close matching keywords from the database using difflib.
    
    Args:
        query (str): User's query input.
        limit (int): Max number of close matches to return.

    Returns:
        List[str]: List of similar keyword strings.
    """
    try:
        all_keywords = await get_all_keywords()
        if not all_keywords:
            return []

        matches = difflib.get_close_matches(query, all_keywords, n=limit, cutoff=0.5)
        return matches
    except Exception as e:
        logger.error(f"Failed to find close matches: {e}")
        return []

async def suggest_spelling(query: str) -> Optional[List[str]]:
    """
    Suggest similar spellings for a user's misspelled query.

    Args:
        query (str): The input query to correct.

    Returns:
        Optional[List[str]]: A list of suggested keywords, or None if none found.
    """
    if not query or len(query) < 3:
        return None

    suggestions = await get_close_matches_from_db(query)
    return suggestions if suggestions else None
