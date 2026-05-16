"""
Plugins package - loads all handlers
"""
from pyrogram import Client

async def load_all_plugins(app: Client):
    """Load all plugins"""
    from . import (
        start, help_menu, admin, moderation, filters, notes, hashtags,
        security, welcome, reports, badwords, settings
    )
    
    # Register all plugin handlers
    start.register(app)
    help_menu.register(app)
    admin.register(app)
    moderation.register(app)
    filters.register(app)
    notes.register(app)
    hashtags.register(app)
    security.register(app)
    welcome.register(app)
    reports.register(app)
    badwords.register(app)
    settings.register(app)

__all__ = ['load_all_plugins']
