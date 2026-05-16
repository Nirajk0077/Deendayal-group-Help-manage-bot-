"""
Start command handler
"""
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)

async def start_handler(client: Client, message: Message):
    """Handle /start command"""
    
    if message.chat.type == "private":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{client.me.username}?startgroup=new"),
                InlineKeyboardButton("❓ Help", callback_data="help_main"),
            ],
            [
                InlineKeyboardButton("📚 Commands", callback_data="commands_list"),
                InlineKeyboardButton("⚙️ Settings", callback_data="settings_info"),
            ],
            [
                InlineKeyboardButton("💬 Support", url="https://t.me/your_support"),
                InlineKeyboardButton("📢 Updates", url="https://t.me/your_updates"),
            ],
        ])
        
        text = """
👋 **Welcome to Advanced Moderation Bot!**

I'm a powerful Rose Bot style moderation and management bot.

**Features:**
✨ Advanced Admin Tools
🔐 Security & Filters
📝 Unlimited Notes
🎯 Bad Word Filtering
👋 Welcome/Goodbye
⚠️ Warning System
🔗 Anti-Link/Forward
📊 Reports

**Version:** 1.0.0
**Status:** Production Ready

Click the buttons below to get started!
"""
        
        await message.reply_text(text, reply_markup=keyboard, disable_web_page_preview=True)
    else:
        text = "👋 **Thanks for adding me to your group!**\n\nVisit my DM for setup and features."
        await message.reply_text(text)

def register(app: Client):
    """Register start handler"""
    @app.on_message(filters.command("start"))
    async def start(client: Client, message: Message):
        try:
            await start_handler(client, message)
        except Exception as e:
            logger.error(f"Error in start: {e}")
