# bot/handlers/__init__.py

from aiogram import Router

# Import all sub-handlers
from .user import user_router
from .admin import admin_router
from .callback import callback_router
from .welcome import welcome_router
from .shortlink import shortlink_router
from .premium import premium_router
from .stats import stats_router
from .trending import trending_router
from .search import search_router

# Create the main router
main_router = Router()

# Include all feature routers
main_router.include_router(user_router)
main_router.include_router(admin_router)
main_router.include_router(callback_router)
main_router.include_router(welcome_router)
main_router.include_router(shortlink_router)
main_router.include_router(premium_router)
main_router.include_router(stats_router)
main_router.include_router(trending_router)
main_router.include_router(search_router)

