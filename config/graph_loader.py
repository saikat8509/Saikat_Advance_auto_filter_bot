import os

def load_graph_images(env_var_name: str, default_list=None):
    """
    Load a list of image URLs from an environment variable (comma separated),
    strip spaces, and validate simple URL format (starts with https://graph.org/file/).
    Returns a list of valid URLs or the default list if env var not set or empty.
    """
    raw = os.getenv(env_var_name, "")
    if not raw and default_list is not None:
        return default_list

    urls = [url.strip() for url in raw.split(",") if url.strip()]
    valid_urls = [url for url in urls if url.startswith("https://graph.org/file/")]

    return valid_urls if valid_urls else (default_list or [])

# Example usage loading START_IMAGES with default fallback
START_IMAGES = load_graph_images(
    "START_IMAGES",
    default_list=[
        "https://graph.org/file/801034beee0bc9024e364-43f7d2f29bba359564.jpg",
        "https://graph.org/file/1e999a80d917ff157d848-c90ea0fda9b6650053.jpg",
        "https://graph.org/file/1ed6d39fca02e42826bbd-4a9cb52ea057b3ff6d.jpg"
    ],
)

# Similarly you can load other image lists, e.g., WELCOME_IMAGES, GOODBYE_IMAGES, etc.
