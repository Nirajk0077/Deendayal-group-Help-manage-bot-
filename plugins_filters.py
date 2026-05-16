"""
Filters plugin
"""
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from utils_permissions import check_admin_permission

logger = logging.getLogger(__name__)
db = Database()

async def filter_command(client: Client, message: Message):
    """Add filter"""
    if not await check_admin_permission(message):
        return
    
    if len(message.command) < 2:
        await message.reply_text("**Usage:** `/filter keyword`\n\nReply with the response text.")
        return
    
    keyword = " ".join(message.command[1:])
    
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message with the filter response")
        return
    
    try:
        response_text = (
            message.reply_to_message.text or 
            message.reply_to_message.caption or 
            ""
        )
        
        success = await db.add_filter(message.chat.id, keyword, response_text)
        
        if success:
            await message.reply_text(f"✅ Filter added for `{keyword}`")
        else:
            await message.reply_text(f"⚠️ Filter for `{keyword}` already exists")
    except Exception as e:
        logger.error(f"Filter error: {e}")
        await message.reply_text("❌ Error adding filter")

async def stop_command(client: Client, message: Message):
    """Remove filter"""
    if not await check_admin_permission(message):
        return
    
    if len(message.command) < 2:
        await message.reply_text("**Usage:** `/stop keyword`")
        return
    
    keyword = " ".join(message.command[1:])
    
    try:
        success = await db.remove_filter(message.chat.id, keyword)
        
        if success:
            await message.reply_text(f"✅ Filter removed for `{keyword}`")
        else:
            await message.reply_text(f"❌ No filter found for `{keyword}`")
    except Exception as e:
        logger.error(f"Stop error: {e}")
        await message.reply_text("❌ Error removing filter")

async def filters_command(client: Client, message: Message):
    """List filters"""
    try:
        filters_list = await db.get_filters(message.chat.id)
        
        if not filters_list:
            await message.reply_text("❌ No filters set in this group")
            return
        
        text = "**📝 Active Filters:**\n\n"
        for i, f in enumerate(filters_list, 1):
            text += f"`{i}.` `{f['keyword']}`\n"
        
        if len(text) > 4096:
            await message.reply_text(text[:4096])
        else:
            await message.reply_text(text)
    except Exception as e:
        logger.error(f"Filters error: {e}")
        await message.reply_text("❌ Error retrieving filters")

async def stopall_command(client: Client, message: Message):
    """Clear all filters"""
    if not await check_admin_permission(message):
        return
    
    try:
        filters_list = await db.get_filters(message.chat.id)
        
        if not filters_list:
            await message.reply_text("❌ No filters to remove")
            return
        
        count = await db.clear_filters(message.chat.id)
        await message.reply_text(f"✅ Removed {count} filters")
    except Exception as e:
        logger.error(f"Stopall error: {e}")
        await message.reply_text("❌ Error clearing filters")

async def trigger_filter(client: Client, message: Message):
    """Trigger filter responses"""
    if not message.text:
        return
    
    try:
        settings = await db.get_group_settings(message.chat.id)
        filters_list = await db.get_filters(message.chat.id)
        
        if not filters_list:
            return
        
        filter_mode = settings.get("filter_mode", "partial")
        text_lower = message.text.lower()
        
        for f in filters_list:
            keyword = f.get("keyword", "").lower()
            
            if filter_mode == "exact":
                if text_lower.startswith(keyword):
                    await message.reply_text(f["response"], parse_mode="markdown")
                    break
            else:  # partial
                if keyword in text_lower:
                    await message.reply_text(f["response"], parse_mode="markdown")
                    break
    except Exception as e:
        logger.error(f"Filter trigger error: {e}")

def register(app: Client):
    """Register filter handlers"""
    
    @app.on_message(filters.command("filter") & filters.group)
    async def filter_cmd(client: Client, message: Message):
        await filter_command(client, message)
    
    @app.on_message(filters.command("stop") & filters.group)
    async def stop_cmd(client: Client, message: Message):
        await stop_command(client, message)
    
    @app.on_message(filters.command("filters") & filters.group)
    async def filters_cmd(client: Client, message: Message):
        await filters_command(client, message)
    
    @app.on_message(filters.command("stopall") & filters.group)
    async def stopall_cmd(client: Client, message: Message):
        await stopall_command(client, message)
    
    @app.on_message(filters.text & filters.group & ~filters.command(["filter", "stop", "filters", "stopall", "save", "get", "notes"]))
    async def filter_trigger(client: Client, message: Message):
        await trigger_filter(client, message)
