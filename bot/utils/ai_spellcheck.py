# bot/utils/ai_spellcheck.py

import difflib
from typing import List, Optional
from rapidfuzz import fuzz, process

# Optional: You can replace this with OpenAI GPT, spellchecker, or other AI models
# For now, we use fuzzy string matching as a fast and offline solution

def suggest_titles(user_query: str, database_titles: List[str], max_suggestions: int = 5) -> List[str]:
    """
    Suggests close-matching titles from the indexed movie titles using fuzzy matching.
    """
    if not user_query or not database_titles:
        return []

    # Using RapidFuzz for better performance and accuracy
    matches = process.extract(
        user_query, database_titles, scorer=fuzz.ratio, limit=max_suggestions
    )

    # Return only the matched titles
    return [match[0] for match in matches if match[1] >= 60]  # Only high-similarity matches


def get_best_match(user_query: str, database_titles: List[str]) -> Optional[str]:
    """
    Returns the single best match for a given user query.
    """
    if not user_query or not database_titles:
        return None

    best_match = process.extractOne(user_query, database_titles, scorer=fuzz.ratio)
    if best_match and best_match[1] >= 70:
        return best_match[0]

    return None


# Optional AI fallback using OpenAI (if you enable it)
# Requires setting OPENAI_API_KEY in your env

"""
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def ai_correct_query(query: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for correcting movie titles."},
                {"role": "user", "content": f"Correct this movie title spelling: {query}"}
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[OpenAI ERROR] {e}")
        return query  # Fallback to original query
"""

