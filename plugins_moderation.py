"""
Moderation commands plugin
"""
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from utils_permissions import check_admin_permission

logger = logging.getLogger(__name__)
db = Database()

async def warns_command(client: Client, message: Message):
    """Get user warnings"""
    user_id = None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1].replace("@", ""))
        except:
            pass
    
    if not user_id:
        await message.reply_text("❌ No user specified")
        return
    
    try:
        settings = await db.get_group_settings(message.chat.id)
        warn_limit = settings.get("warn_limit", 3)
        warn_count = await db.get_warnings(message.chat.id, user_id)
        
        await message.reply_text(f"⚠️ User has {warn_count}/{warn_limit} warnings")
    except Exception as e:
        logger.error(f"Warns error: {e}")
        await message.reply_text("❌ Error retrieving warnings")

async def resetwarn_command(client: Client, message: Message):
    """Reset user warnings"""
    if not await check_admin_permission(message):
        return
    
    user_id = None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1].replace("@", ""))
        except:
            pass
    
    if not user_id:
        await message.reply_text("❌ No user specified")
        return
    
    try:
        await db.reset_warnings(message.chat.id, user_id)
        await message.reply_text("✅ Warnings reset")
    except Exception as e:
        logger.error(f"Reset warn error: {e}")
        await message.reply_text("❌ Error resetting warnings")

async def pin_command(client: Client, message: Message):
    """Pin message"""
    if not await check_admin_permission(message):
        return
    
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to pin")
        return
    
    try:
        await client.pin_chat_message(
            message.chat.id,
            message.reply_to_message.message_id
        )
        await message.reply_text("✅ Message pinned")
    except Exception as e:
        logger.error(f"Pin error: {e}")
        await message.reply_text("❌ Error pinning message")

async def unpin_command(client: Client, message: Message):
    """Unpin message"""
    if not await check_admin_permission(message):
        return
    
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to unpin")
        return
    
    try:
        await client.unpin_chat_message(
            message.chat.id,
            message.reply_to_message.message_id
        )
        await message.reply_text("✅ Message unpinned")
    except Exception as e:
        logger.error(f"Unpin error: {e}")
        await message.reply_text("❌ Error unpinning message")

def register(app: Client):
    """Register moderation handlers"""
    handlers = [
        (filters.command("warns"), warns_command),
        (filters.command("resetwarn"), resetwarn_command),
        (filters.command("pin"), pin_command),
        (filters.command("unpin"), unpin_command),
    ]
    
    for filter_obj, handler in handlers:
        @app.on_message(filter_obj & filters.group)
        async def handle(client: Client, message: Message, h=handler):
            try:
                await h(client, message)
            except Exception as e:
                logger.error(f"Handler error: {e}")
