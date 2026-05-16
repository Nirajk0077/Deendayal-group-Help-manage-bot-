"""
Welcome and goodbye plugin
"""
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, ChatMember
from database import Database
from utils_permissions import check_admin_permission
from utils_helpers import TextFormatter

logger = logging.getLogger(__name__)
db = Database()

async def setwelcome_command(client: Client, message: Message):
    """Set welcome message"""
    if not await check_admin_permission(message):
        return
    
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to set as welcome")
        return
    
    try:
        welcome_text = (
            message.reply_to_message.text or 
            message.reply_to_message.caption or 
            ""
        )
        
        await db.set_welcome(message.chat.id, welcome_text)
        await message.reply_text("✅ Welcome message set")
    except Exception as e:
        logger.error(f"Set welcome error: {e}")
        await message.reply_text("❌ Error setting welcome")

async def welcome_toggle_command(client: Client, message: Message):
    """Toggle welcome"""
    if not await check_admin_permission(message):
        return
    
    if len(message.command) < 2:
        settings = await db.get_group_settings(message.chat.id)
        status = "✅ ON" if settings.get("welcome_enabled") else "❌ OFF"
        await message.reply_text(f"**Welcome:** {status}")
        return
    
    action = message.command[1].lower()
    
    if action == "on":
        await db.update_group_settings(message.chat.id, {"welcome_enabled": True})
        await message.reply_text("✅ Welcome enabled")
    elif action == "off":
        await db.update_group_settings(message.chat.id, {"welcome_enabled": False})
        await message.reply_text("✅ Welcome disabled")
    else:
        await message.reply_text("**Usage:** `/welcome on/off`")

async def clearwelcome_command(client: Client, message: Message):
    """Clear welcome message"""
    if not await check_admin_permission(message):
        return
    
    try:
        col = await db.db["welcome"]
        await col.delete_one({"group_id": message.chat.id})
        await message.reply_text("✅ Welcome message cleared")
    except Exception as e:
        logger.error(f"Clear welcome error: {e}")
        await message.reply_text("❌ Error clearing welcome")

async def setgoodbye_command(client: Client, message: Message):
    """Set goodbye message"""
    if not await check_admin_permission(message):
        return
    
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to set as goodbye")
        return
    
    try:
        goodbye_text = (
            message.reply_to_message.text or 
            message.reply_to_message.caption or 
            ""
        )
        
        await db.set_goodbye(message.chat.id, goodbye_text)
        await message.reply_text("✅ Goodbye message set")
    except Exception as e:
        logger.error(f"Set goodbye error: {e}")
        await message.reply_text("❌ Error setting goodbye")

async def goodbye_toggle_command(client: Client, message: Message):
    """Toggle goodbye"""
    if not await check_admin_permission(message):
        return
    
    if len(message.command) < 2:
        settings = await db.get_group_settings(message.chat.id)
        status = "✅ ON" if settings.get("goodbye_enabled") else "❌ OFF"
        await message.reply_text(f"**Goodbye:** {status}")
        return
    
    action = message.command[1].lower()
    
    if action == "on":
        await db.update_group_settings(message.chat.id, {"goodbye_enabled": True})
        await message.reply_text("✅ Goodbye enabled")
    elif action == "off":
        await db.update_group_settings(message.chat.id, {"goodbye_enabled": False})
        await message.reply_text("✅ Goodbye disabled")
    else:
        await message.reply_text("**Usage:** `/goodbye on/off`")

async def cleargoodbye_command(client: Client, message: Message):
    """Clear goodbye message"""
    if not await check_admin_permission(message):
        return
    
    try:
        col = await db.db["goodbye"]
        await col.delete_one({"group_id": message.chat.id})
        await message.reply_text("✅ Goodbye message cleared")
    except Exception as e:
        logger.error(f"Clear goodbye error: {e}")
        await message.reply_text("❌ Error clearing goodbye")

async def member_update_handler(client: Client, update):
    """Handle member join/leave"""
    try:
        new_member = update.new_chat_member
        old_member = update.old_chat_member
        
        group_id = update.chat.id
        user_id = new_member.user.id
        
        # Member joined
        if (old_member is None or old_member.status == "left") and new_member.status == "member":
            settings = await db.get_group_settings(group_id)
            
            if settings.get("welcome_enabled"):
                welcome = await db.get_welcome(group_id)
                
                if welcome:
                    text = welcome["text"]
                    
                    # Replace variables
                    variables = {
                        "user": new_member.user.mention,
                        "user_id": user_id,
                        "first_name": new_member.user.first_name,
                        "last_name": new_member.user.last_name or "",
                        "username": f"@{new_member.user.username}" if new_member.user.username else "None",
                        "group": update.chat.title,
                        "member_count": update.chat.members_count or "Unknown",
                    }
                    
                    formatted_text = TextFormatter.format_with_variables(text, variables)
                    
                    try:
                        await client.send_message(group_id, formatted_text, parse_mode="markdown")
                    except Exception as e:
                        logger.error(f"Error sending welcome: {e}")
        
        # Member left
        elif (old_member.status in ["member", "administrator", "creator"]) and new_member.status == "left":
            settings = await db.get_group_settings(group_id)
            
            if settings.get("goodbye_enabled"):
                goodbye = await db.get_goodbye(group_id)
                
                if goodbye:
                    text = goodbye["text"]
                    
                    # Replace variables
                    variables = {
                        "user": old_member.user.mention,
                        "user_id": user_id,
                        "first_name": old_member.user.first_name,
                        "last_name": old_member.user.last_name or "",
                        "username": f"@{old_member.user.username}" if old_member.user.username else "None",
                        "group": update.chat.title,
                    }
                    
                    formatted_text = TextFormatter.format_with_variables(text, variables)
                    
                    try:
                        await client.send_message(group_id, formatted_text, parse_mode="markdown")
                    except Exception as e:
                        logger.error(f"Error sending goodbye: {e}")
    
    except Exception as e:
        logger.error(f"Member update error: {e}")

def register(app: Client):
    """Register welcome handlers"""
    
    @app.on_message(filters.command("setwelcome") & filters.group)
    async def setwelcome_cmd(client: Client, message: Message):
        await setwelcome_command(client, message)
    
    @app.on_message(filters.command("welcome") & filters.group)
    async def welcome_cmd(client: Client, message: Message):
        await welcome_toggle_command(client, message)
    
    @app.on_message(filters.command("clearwelcome") & filters.group)
    async def clearwelcome_cmd(client: Client, message: Message):
        await clearwelcome_command(client, message)
    
    @app.on_message(filters.command("setgoodbye") & filters.group)
    async def setgoodbye_cmd(client: Client, message: Message):
        await setgoodbye_command(client, message)
    
    @app.on_message(filters.command("goodbye") & filters.group)
    async def goodbye_cmd(client: Client, message: Message):
        await goodbye_toggle_command(client, message)
    
    @app.on_message(filters.command("cleargoodbye") & filters.group)
    async def cleargoodbye_cmd(client: Client, message: Message):
        await cleargoodbye_command(client, message)
    
    @app.on_chat_member_updated()
    async def member_update(client: Client, update):
        await member_update_handler(client, update)
