import re
from html import unescape

def clean_text(text: str) -> str:
    """
    Clean up input text by:
    - Unescaping HTML entities
    - Removing extra whitespaces
    - Removing Telegram markdown special characters to prevent formatting issues
    - Removing URLs
    - Stripping leading/trailing spaces
    
    Args:
        text (str): Raw input text
    
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Unescape HTML entities like &amp;, &lt;, &gt;, etc.
    text = unescape(text)

    # Remove URLs (http, https, t.me, telegram links, etc.)
    url_pattern = re.compile(r"https?://\S+|t\.me/\S+")
    text = url_pattern.sub("", text)

    # Remove Telegram markdown special characters that might break formatting
    # Telegram uses *, _, `, [, ], (, ), ~, >, #, +, -, =, |, {, }, ., !
    # We'll remove those that are not likely part of normal text.
    markdown_special_chars = r"[*_`\[\]()~>#+\-=|{}.!]"
    text = re.sub(markdown_special_chars, "", text)

    # Replace multiple spaces/newlines with a single space
    text = re.sub(r"\s+", " ", text)

    # Strip leading/trailing spaces
    return text.strip()


def clean_filename(filename: str) -> str:
    """
    Clean a filename by removing illegal characters for file systems
    and trimming extra spaces.
    
    Args:
        filename (str): Raw filename string
    
    Returns:
        str: Cleaned filename
    """
    if not filename:
        return "file"

    # Remove characters not allowed in filenames on Windows, macOS, Linux
    # For simplicity, remove: <>:"/\|?* and control chars
    filename = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename)

    # Replace multiple spaces with single space
    filename = re.sub(r"\s+", " ", filename)

    # Strip leading/trailing spaces and dots (dots at end can cause issues)
    filename = filename.strip(" .")

    # Fallback default name if empty after cleaning
    if not filename:
        return "file"

    return filename


def remove_telegram_markdown(text: str) -> str:
    """
    Remove Telegram markdown formatting from a string.
    This can help to prevent markdown injection issues.
    
    Args:
        text (str): Input text
    
    Returns:
        str: Text without markdown formatting characters
    """
    if not text:
        return ""

    # Remove Telegram markdown symbols
    markdown_chars = r"[*_`\[\]()~>#+\-=|{}.!]"
    return re.sub(markdown_chars, "", text).strip()
