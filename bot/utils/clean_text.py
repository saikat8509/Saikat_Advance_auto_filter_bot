# bot/utils/clean_text.py

import re
import html
import unicodedata

def clean_query(text: str) -> str:
    """
    Clean user input for search queries, IMDb titles, spell check, etc.
    Removes symbols, encodings, extra spaces, and HTML entities.
    """
    if not text:
        return ""
    
    text = html.unescape(text)
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\w\s]", " ", text)  # Replace punctuation with space
    text = re.sub(r"\s+", " ", text)  # Collapse multiple spaces
    return text.strip().lower()

def clean_filename(filename: str) -> str:
    """
    Clean file names by removing common unwanted patterns.
    Useful for matching file titles to IMDb/search queries.
    """
    if not filename:
        return ""
    
    filename = html.unescape(filename)
    filename = re.sub(r'[\[\]{}()@#$%^&*+=|\\<>`~]', '', filename)
    filename = re.sub(r'[_\-\.]', ' ', filename)
    filename = re.sub(r'\b(480p|720p|1080p|2160p|4k|x264|x265|BluRay|HDRip|WEBRip|WEB-DL|BRRip|HEVC|DDP5\.1|AAC|ESub|Hindi|Dual Audio|NF|AMZN|HD)\b', '', filename, flags=re.IGNORECASE)
    filename = re.sub(r'\s+', ' ', filename)
    return filename.strip()

def extract_year(text: str) -> str:
    """
    Extracts year from string if present in (YYYY) format.
    """
    match = re.search(r"\b(19|20)\d{2}\b", text)
    return match.group(0) if match else ""

def strip_html(text: str) -> str:
    """
    Remove all HTML tags from a string.
    """
    return re.sub(r"<.*?>", "", text or "")

def clean_title_for_imdb(title: str) -> str:
    """
    Prepare movie title for IMDb API search.
    """
    title = clean_filename(title)
    title = re.sub(r'\s+', ' ', title)
    return title.strip()

def normalize_name(name: str) -> str:
    """
    Remove case and accents for consistent comparison (e.g., for matching names, slugs).
    """
    name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode('utf-8')
    return name.lower()

def remove_emojis(text: str) -> str:
    """
    Strip all emojis for logs, filenames, and search.
    """
    emoji_pattern = re.compile(
        "["u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def clean_message_text(text: str) -> str:
    """
    Final catch-all cleaner for any user message, removing HTML, emojis, extra chars.
    """
    text = strip_html(text)
    text = remove_emojis(text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def safe_caption(text: str) -> str:
    """
    Cleans caption text to ensure safe rendering in Markdown/HTML.
    """
    if not text:
        return ""
    text = html.escape(text)
    text = text.replace("*", "").replace("_", "").replace("`", "")
    return text

