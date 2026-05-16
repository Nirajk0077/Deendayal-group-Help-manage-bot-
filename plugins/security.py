"""
Security filtering plugin
"""
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from database import Database
from utils_permissions import check_admin_permission
from utils_helpers import LinkDetector, BadWordFilter
from config import FLOODWAIT

logger = logging.getLogger(__name__)
db = Database()

async def message_security_monitor(client: Client, message: Message):
    """Monitor messages for security threats"""
    try:
        # Skip if from bot or admin
        if message.from_user.is_bot:
            return
        
        group_id = message.chat.id
        
        # Get settings
        settings = await db.get_group_settings(group_id)
        
        if not settings:
            return
        
        should_delete = False
        reason = None
        
        # Get full text
        text = f"{message.text or ''} {message.caption or ''}".lower()
        
        # Check for links
        if settings.get("anti_link") and LinkDetector.has_link(text):
            should_delete = True
            reason = "Link detected"
        
        # Check for forwards
        elif settings.get("anti_forward") and (
            message.forward_from or 
            message.forward_from_chat or 
            message.forward_origin
        ):
            should_delete = True
            reason = "Forwarded message"
        
        # Check for bad words
        elif settings.get("anti_badwords"):
            badwords = await db.get_badwords(group_id)
            if badwords:
                has_bad, word = BadWordFilter.contains_badword(text, badwords)
                if has_bad:
                    should_delete = True
                    reason = f"Bad word: {word}"
        
        # Delete if necessary
        if should_delete:
            try:
                can_delete = await check_can_delete(client, group_id)
                if can_delete:
                    await message.delete()
                    logger.info(f"Deleted message in {group_id}: {reason}")
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                logger.error(f"Error deleting message: {e}")
    
    except Exception as e:
        logger.error(f"Security monitor error: {e}")

async def antilink_command(client: Client, message: Message):
    """Toggle anti-link"""
    if not await check_admin_permission(message):
        return
    
    if len(message.command) < 2:
        settings = await db.get_group_settings(message.chat.id)
        status = "✅ ON" if settings.get("anti_link") else "❌ OFF"
        await message.reply_text(f"**Anti-Link:** {status}")
        return
    
    action = message.command[1].lower()
    
    if action == "on":
        await db.update_group_settings(message.chat.id, {"anti_link": True})
        await message.reply_text("✅ Anti-Link enabled")
    elif action == "off":
        await db.update_group_settings(message.chat.id, {"anti_link": False})
        await message.reply_text("✅ Anti-Link disabled")
    else:
        await message.reply_text("**Usage:** `/antilink on/off`")

async def antiforward_command(client: Client, message: Message):
    """Toggle anti-forward"""
    if not await check_admin_permission(message):
        return
    
    if len(message.command) < 2:
        settings = await db.get_group_settings(message.chat.id)
        status = "✅ ON" if settings.get("anti_forward") else "❌ OFF"
        await message.reply_text(f"**Anti-Forward:** {status}")
        return
    
    action = message.command[1].lower()
    
    if action == "on":
        await db.update_group_settings(message.chat.id, {"anti_forward": True})
        await message.reply_text("✅ Anti-Forward enabled")
    elif action == "off":
        await db.update_group_settings(message.chat.id, {"anti_forward": False})
        await message.reply_text("✅ Anti-Forward disabled")
    else:
        await message.reply_text("**Usage:** `/antiforward on/off`")

async def check_can_delete(client: Client, group_id: int) -> bool:
    """Check if bot can delete messages"""
    try:
        member = await client.get_chat_member(group_id, client.me.id)
        return member.can_delete_messages if member else False
    except:
        return False

def register(app: Client):
    """Register security handlers"""
    
    @app.on_message(filters.group & filters.incoming & ~filters.bot)
    async def security_monitor(client: Client, message: Message):
        await message_security_monitor(client, message)
    
    @app.on_message(filters.command("antilink") & filters.group)
    async def antilink_cmd(client: Client, message: Message):
        await antilink_command(client, message)
    
    @app.on_message(filters.command("antiforward") & filters.group)
    async def antiforward_cmd(client: Client, message: Message):
        await antiforward_command(client, message)
