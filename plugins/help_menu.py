"""
Help command handler
"""
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

logger = logging.getLogger(__name__)

async def help_handler(client: Client, message: Message):
    """Handle /help command"""
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚙️ Admin", callback_data="help_admin")],
        [InlineKeyboardButton("📝 Filters", callback_data="help_filters")],
        [InlineKeyboardButton("🎯 Words", callback_data="help_words")],
        [InlineKeyboardButton("👋 Welcome", callback_data="help_welcome")],
        [InlineKeyboardButton("🔐 Security", callback_data="help_security")],
        [InlineKeyboardButton("📊 Settings", callback_data="help_settings")],
    ])
    
    text = """
**📚 Help Menu**

Select a category to learn more:

⚙️ **Admin** - Ban, mute, warn, etc
📝 **Filters** - Add custom filters & notes
🎯 **Words** - Bad word filtering system
👋 **Welcome** - Welcome/goodbye messages
🔐 **Security** - Anti-link, anti-forward
📊 **Settings** - Group configuration
"""
    
    await message.reply_text(text, reply_markup=keyboard)

def register(app: Client):
    """Register help handlers"""
    
    @app.on_message(filters.command("help"))
    async def help_cmd(client: Client, message: Message):
        try:
            await help_handler(client, message)
        except Exception as e:
            logger.error(f"Error in help: {e}")
    
    @app.on_callback_query(filters.regex("^help_"))
    async def help_callback(client: Client, callback_query: CallbackQuery):
        try:
            query_type = callback_query.data.replace("help_", "")
            
            help_texts = {
                "admin": """
**⚙️ Admin Commands**

/ban [@user] - Ban user
/unban [id] - Unban user
/mute [@user] - Mute user
/unmute [@user] - Unmute user

/warn [@user] [reason] - Warn user
/warns [@user] - Check warnings
/resetwarn [@user] - Reset warnings

/promote [@user] - Make admin
/demote [@user] - Remove admin

/purge [count] - Delete messages
/pin - Pin replied message
/unpin - Unpin message

/id - Get IDs
/info [@user] - User info

Back /help
""",
                "filters": """
**📝 Filters & Notes**

/filter [keyword] - Add filter (reply with response)
/stop [keyword] - Remove filter
/filters - List all filters
/stopall - Clear all filters

/save [name] - Save note (reply with content)
/get [name] - Get note
/notes - List notes

#hashtag - Trigger filter/note

Back /help
""",
                "words": """
**🎯 Bad Word Filtering**

/addbadword [word] - Add bad word
/removebadword [word] - Remove bad word
/badwords - List bad words
/clearbadwords - Clear all

/antibadwords on/off - Toggle filter

Features:
✅ Case insensitive
✅ Word boundaries
✅ Unlimited words

Back /help
""",
                "welcome": """
**👋 Welcome & Goodbye**

/setwelcome - Set welcome (reply to message)
/welcome on/off - Toggle welcome
/clearwelcome - Clear welcome

/setgoodbye - Set goodbye
/goodbye on/off - Toggle goodbye
/cleargoodbye - Clear goodbye

Variables:
{user} - User mention
{user_id} - User ID
{first_name} - First name
{group} - Group name
{member_count} - Member count

Back /help
""",
                "security": """
**🔐 Security Features**

/antilink on/off - Toggle link filter
/antiforward on/off - Toggle forward filter

/lock [type] - Lock content type
/locks - View active locks
/unlock [type] - Unlock type

Types: links, forwards, media, stickers, bots

/report - Report message

Back /help
""",
                "settings": """
**📊 Settings**

/settings - Open settings panel

Available options:
• Anti-Link
• Anti-Forward
• Anti-BadWords
• Welcome/Goodbye
• Reports
• Locks
• Advanced settings

Only admins can change settings.

Back /help
""",
            }
            
            text = help_texts.get(query_type, "Help category not found")
            
            await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="help_main")],
            ]))
        
        except Exception as e:
            logger.error(f"Error in help callback: {e}")
    
    @app.on_callback_query(filters.regex("^help_main$"))
    async def help_main_callback(client: Client, callback_query: CallbackQuery):
        try:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("⚙️ Admin", callback_data="help_admin")],
                [InlineKeyboardButton("📝 Filters", callback_data="help_filters")],
                [InlineKeyboardButton("🎯 Words", callback_data="help_words")],
                [InlineKeyboardButton("👋 Welcome", callback_data="help_welcome")],
                [InlineKeyboardButton("🔐 Security", callback_data="help_security")],
                [InlineKeyboardButton("📊 Settings", callback_data="help_settings")],
            ])
            
            text = """
**📚 Help Menu**

Select a category:

⚙️ **Admin** - Ban, mute, warn, etc
📝 **Filters** - Custom filters & notes
🎯 **Words** - Bad word filtering
👋 **Welcome** - Welcome/goodbye
🔐 **Security** - Anti-link, locks
📊 **Settings** - Configuration
"""
            
            await callback_query.edit_message_text(text, reply_markup=keyboard)
        except Exception as e:
            logger.error(f"Error: {e}")
