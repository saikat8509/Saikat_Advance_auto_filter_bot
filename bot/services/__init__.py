from .premium import start_premium_check_loop
from .trending import start_trending_post_loop

def start_services():
    # Starts the premium expiry check loop
    start_premium_check_loop()

    # Starts the trending posting service (if enabled)
    start_trending_post_loop()

