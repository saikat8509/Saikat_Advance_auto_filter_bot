# bot/plugins/shorten.py

import httpx
import logging
from config import SHORTENER_APIS

logger = logging.getLogger(__name__)

# Mapping known shorteners to their API URLs and request data format
SHORTENER_API_DETAILS = {
    "shortzon": {
        "api_url": "https://api.shortzon.com/v1/shorten",  # example URL
        "headers": lambda api_key: {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        "json_data": lambda url: {"url": url},
        "extract_short_url": lambda resp_json: resp_json.get("short_url") or resp_json.get("result"),
    },
    "try2link": {
        "api_url": "https://api.try2link.com/shorten",  # example URL
        "headers": lambda api_key: {"apikey": api_key},
        "json_data": lambda url: {"long_url": url},
        "extract_short_url": lambda resp_json: resp_json.get("short_link"),
    },
    # Add more shorteners here as needed
}

async def shorten_url(url: str, service_name: str = None) -> str:
    """
    Shortens a URL using the configured shortener APIs from SHORTENER_APIS.
    service_name is optional; defaults to the first available shortener.
    """
    if not SHORTENER_APIS:
        logger.warning("No shortener API keys configured in SHORTENER_APIS.")
        return url

    service_key = (service_name or next(iter(SHORTENER_APIS))).lower()

    if service_key not in SHORTENER_APIS:
        logger.warning(f"Shortener service '{service_key}' not configured with API key.")
        return url

    api_key = SHORTENER_APIS[service_key]

    if service_key not in SHORTENER_API_DETAILS:
        logger.warning(f"Shortener service '{service_key}' is not supported in code.")
        return url

    api_info = SHORTENER_API_DETAILS[service_key]
    api_url = api_info["api_url"]
    headers = api_info["headers"](api_key)
    json_data = api_info["json_data"](url)

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(api_url, json=json_data, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            short_url = api_info["extract_short_url"](data)
            return short_url or url
    except Exception as e:
        logger.error(f"Error shortening URL with {service_key}: {e}")
        return url
