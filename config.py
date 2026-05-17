"""
Configuration and settings for the Telegram bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API Configuration - REQUIRED
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Validate credentials
if not API_ID or API_ID == 0:
    raise ValueError("❌ API_ID is required in .env file")
if not API_HASH:
    raise ValueError("❌ API_HASH is required in .env file")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN is required in .env file")

# Database Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
SUDO_USERS = list(map(int, os.getenv("SUDO_USERS", "").split())) if os.getenv("SUDO_USERS") else []
LOG_GROUP = int(os.getenv("LOG_GROUP", -1001234567890))

# Database Configuration
DB_NAME = "moderationbot"

# Bot Settings
BOT_USERNAME = os.getenv("BOT_USERNAME", "ModBotAdmin")
PREFIX = "/"

# Rate Limiting
FLOODWAIT = 0.1
MAX_RETRIES = 3

# Collections
COLLECTIONS = {
    "group_settings": "group_settings",
    "filters": "filters",
    "notes": "notes",
    "hashtags": "hashtags",
    "badwords": "badwords",
    "warnings": "warnings",
    "locks": "locks",
    "welcome": "welcome",
    "goodbye": "goodbye",
    "reports": "reports",
    "users": "users",
}

# Default Settings
DEFAULT_SETTINGS = {
    "anti_link": False,
    "anti_forward": False,
    "anti_badwords": False,
    "welcome_enabled": False,
    "goodbye_enabled": False,
    "reports_enabled": True,
    "filter_mode": "partial",  # exact or partial
    "lock_links": False,
    "lock_forwards": False,
    "lock_media": False,
    "lock_stickers": False,
    "lock_bots": False,
    "warn_limit": 3,
    "punishment_mode": "delete",  # delete, warn, mute, ban
}

# Regex Patterns
LINK_PATTERNS = [
    r'https?://[^\s]+',
    r'www\.[^\s]+',
    r't\.me/[^\s]+',
    r'@[a-zA-Z0-9_]+',
    r'tg://join\?invite=[^\s]+',
]

# Messages
MESSAGES = {
    "no_permission": "❌ You don't have permission to use this command.",
    "group_only": "❌ This command works only in groups.",
    "admin_only": "❌ This command is for group admins only.",
    "not_replied": "❌ Please reply to a message to use this command.",
    "success": "✅ Done!",
    "error": "❌ An error occurred.",
    "feature_disabled": "⚙️ This feature is disabled.",
}
