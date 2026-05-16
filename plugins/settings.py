"""
Settings panel plugin - Rose Bot style
"""
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import Database
from utils.permissions import check_admin_permission, PermissionChecker

logger = logging.getLogger(__name__)
db = Database()

def get_settings_keyboard(settings: dict) -> InlineKeyboardMarkup:
    """Create settings keyboard"""
    
    def toggle_icon(val):
        return "✅" if val else "❌"
    
    keyboard = [
        [
            InlineKeyboardButton(
                f"🔗 Anti-Link {toggle_icon(settings.get('anti_link', False))}",
                callback_data="setting_antilink"
            ),
        ],
        [
            InlineKeyboardButton(
                f"↩️ Anti-Forward {toggle_icon(settings.get('anti_forward', False))}",
                callback_data="setting_antiforward"
            ),
        ],
        [
            InlineKeyboardButton(
                f"🎯 Anti-BadWords {toggle_icon(settings.get('anti_badwords', False))}",
                callback_data="setting_antibadwords"
            ),
        ],
        [
            InlineKeyboardButton(
                f"👋 Welcome {toggle_icon(settings.get('welcome_enabled', False))}",
                callback_data="setting_welcome"
            ),
        ],
        [
            InlineKeyboardButton(
                f"👋 Goodbye {toggle_icon(settings.get('goodbye_enabled', False))}",
                callback_data="setting_goodbye"
            ),
        ],
        [
            InlineKeyboardButton(
                f"🚨 Reports {toggle_icon(settings.get('reports_enabled', True))}",
                callback_data="setting_reports"
            ),
        ],
        [
            InlineKeyboardButton("⚙️ Advanced", callback_data="settings_advanced"),
        ],
        [
            InlineKeyboardButton("❌ Close", callback_data="close_menu"),
        ],
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_advanced_keyboard(settings: dict) -> InlineKeyboardMarkup:
    """Create advanced settings keyboard"""
    
    warn_limit = settings.get('warn_limit', 3)
    filter_mode = settings.get('filter_mode', 'partial')
    
    keyboard = [
        [
            InlineKeyboardButton(f"⚠️ Warn Limit: {warn_limit}", callback_data="set_warnlimit"),
        ],
        [
            InlineKeyboardButton(f"🔎 Mode: {filter_mode}", callback_data="set_filtermode"),
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="settings_main"),
        ],
    ]
    
    return InlineKeyboardMarkup(keyboard)

async def settings_command(client: Client, message: Message):
    """Open settings panel"""
    if not await check_admin_permission(message):
        return
    
    try:
        settings = await db.get_group_settings(message.chat.id)
        
        text = """
**⚙️ Group Settings**

Configure your group moderation:

🔗 Anti-Link
↩️ Anti-Forward
🎯 Anti-BadWords
👋 Welcome Message
👋 Goodbye Message
🚨 Reports
⚙️ Advanced Settings
"""
        
        keyboard = get_settings_keyboard(settings)
        await message.reply_text(text, reply_markup=keyboard)
    
    except Exception as e:
        logger.error(f"Settings error: {e}")
        await message.reply_text("❌ Error opening settings")

async def setting_callback(client: Client, callback_query: CallbackQuery):
    """Handle setting toggles"""
    try:
        setting_type = callback_query.data.replace("setting_", "")
        group_id = callback_query.message.chat.id
        user_id = callback_query.from_user.id
        
        # Check permission
        if not await PermissionChecker.is_group_admin(client, group_id, user_id):
            await callback_query.answer("❌ You don't have permission", show_alert=True)
            return
        
        settings = await db.get_group_settings(group_id)
        
        # Toggle settings
        if setting_type == "antilink":
            settings["anti_link"] = not settings.get("anti_link", False)
            text = "🔗 Anti-Link " + ("✅ ON" if settings["anti_link"] else "❌ OFF")
        
        elif setting_type == "antiforward":
            settings["anti_forward"] = not settings.get("anti_forward", False)
            text = "↩️ Anti-Forward " + ("✅ ON" if settings["anti_forward"] else "❌ OFF")
        
        elif setting_type == "antibadwords":
            settings["anti_badwords"] = not settings.get("anti_badwords", False)
            text = "🎯 Anti-BadWords " + ("✅ ON" if settings["anti_badwords"] else "❌ OFF")
        
        elif setting_type == "welcome":
            settings["welcome_enabled"] = not settings.get("welcome_enabled", False)
            text = "👋 Welcome " + ("✅ ON" if settings["welcome_enabled"] else "❌ OFF")
        
        elif setting_type == "goodbye":
            settings["goodbye_enabled"] = not settings.get("goodbye_enabled", False)
            text = "👋 Goodbye " + ("✅ ON" if settings["goodbye_enabled"] else "❌ OFF")
        
        elif setting_type == "reports":
            settings["reports_enabled"] = not settings.get("reports_enabled", True)
            text = "🚨 Reports " + ("✅ ON" if settings["reports_enabled"] else "❌ OFF")
        
        else:
            return
        
        await db.update_group_settings(group_id, settings)
        
        # Refresh
        settings_text = """
**⚙️ Group Settings**

Configure your group moderation:

🔗 Anti-Link
↩️ Anti-Forward
🎯 Anti-BadWords
👋 Welcome Message
👋 Goodbye Message
🚨 Reports
⚙️ Advanced Settings
"""
        
        keyboard = get_settings_keyboard(settings)
        await callback_query.edit_message_text(settings_text, reply_markup=keyboard)
        await callback_query.answer(text, show_alert=False)
    
    except Exception as e:
        logger.error(f"Setting callback error: {e}")
        await callback_query.answer("❌ Error", show_alert=True)

async def advanced_callback(client: Client, callback_query: CallbackQuery):
    """Open advanced settings"""
    try:
        group_id = callback_query.message.chat.id
        settings = await db.get_group_settings(group_id)
        
        warn_limit = settings.get('warn_limit', 3)
        filter_mode = settings.get('filter_mode', 'partial')
        
        text = f"""
**⚙️ Advanced Settings**

**Warn Limit:** {warn_limit}
Change the number of warnings before action.

**Filter Mode:** {filter_mode}
Exact: Match whole words
Partial: Match anywhere in text
"""
        
        keyboard = get_advanced_keyboard(settings)
        await callback_query.edit_message_text(text, reply_markup=keyboard)
    
    except Exception as e:
        logger.error(f"Advanced callback error: {e}")

async def main_callback(client: Client, callback_query: CallbackQuery):
    """Return to main settings"""
    try:
        group_id = callback_query.message.chat.id
        settings = await db.get_group_settings(group_id)
        
        text = """
**⚙️ Group Settings**

Configure your group moderation:

🔗 Anti-Link
↩️ Anti-Forward
🎯 Anti-BadWords
👋 Welcome Message
👋 Goodbye Message
🚨 Reports
⚙️ Advanced Settings
"""
        
        keyboard = get_settings_keyboard(settings)
        await callback_query.edit_message_text(text, reply_markup=keyboard)
    
    except Exception as e:
        logger.error(f"Main callback error: {e}")

async def close_callback(client: Client, callback_query: CallbackQuery):
    """Close settings"""
    try:
        await callback_query.message.delete()
    except:
        pass

def register(app: Client):
    """Register settings handlers"""
    
    @app.on_message(filters.command("settings") & filters.group)
    async def settings_cmd(client: Client, message: Message):
        await settings_command(client, message)
    
    @app.on_callback_query(filters.regex("^setting_"))
    async def setting_cb(client: Client, callback_query: CallbackQuery):
        await setting_callback(client, callback_query)
    
    @app.on_callback_query(filters.regex("^settings_advanced$"))
    async def advanced_cb(client: Client, callback_query: CallbackQuery):
        await advanced_callback(client, callback_query)
    
    @app.on_callback_query(filters.regex("^settings_main$"))
    async def main_cb(client: Client, callback_query: CallbackQuery):
        await main_callback(client, callback_query)
    
    @app.on_callback_query(filters.regex("^close_menu$"))
    async def close_cb(client: Client, callback_query: CallbackQuery):
        await close_callback(client, callback_query)
