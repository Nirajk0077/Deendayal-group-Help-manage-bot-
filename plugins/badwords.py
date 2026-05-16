"""
Bad word filtering plugin
"""
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from utils.permissions import check_admin_permission

logger = logging.getLogger(__name__)
db = Database()

async def addbadword_command(client: Client, message: Message):
    """Add bad word"""
    if not await check_admin_permission(message):
        return
    
    if len(message.command) < 2:
        await message.reply_text("**Usage:** `/addbadword word`")
        return
    
    word = " ".join(message.command[1:]).strip()
    
    if not word:
        await message.reply_text("❌ Please provide a word")
        return
    
    try:
        success = await db.add_badword(message.chat.id, word)
        
        if success:
            await message.reply_text(f"✅ Added bad word: `{word}`")
        else:
            await message.reply_text(f"⚠️ Word `{word}` already in list")
    except Exception as e:
        logger.error(f"Add badword error: {e}")
        await message.reply_text("❌ Error adding bad word")

async def removebadword_command(client: Client, message: Message):
    """Remove bad word"""
    if not await check_admin_permission(message):
        return
    
    if len(message.command) < 2:
        await message.reply_text("**Usage:** `/removebadword word`")
        return
    
    word = " ".join(message.command[1:]).strip()
    
    try:
        success = await db.remove_badword(message.chat.id, word)
        
        if success:
            await message.reply_text(f"✅ Removed bad word: `{word}`")
        else:
            await message.reply_text(f"❌ Word `{word}` not found")
    except Exception as e:
        logger.error(f"Remove badword error: {e}")
        await message.reply_text("❌ Error removing bad word")

async def badwords_command(client: Client, message: Message):
    """List bad words"""
    try:
        badwords = await db.get_badwords(message.chat.id)
        
        if not badwords:
            await message.reply_text("❌ No bad words in this group")
            return
        
        text = "**🎯 Bad Words List:**\n\n"
        for i, word in enumerate(badwords, 1):
            text += f"`{i}.` `{word}`\n"
        
        if len(text) > 4096:
            await message.reply_text(text[:4096])
            await message.reply_text(text[4096:])
        else:
            await message.reply_text(text)
    except Exception as e:
        logger.error(f"Badwords error: {e}")
        await message.reply_text("❌ Error retrieving bad words")

async def clearbadwords_command(client: Client, message: Message):
    """Clear all bad words"""
    if not await check_admin_permission(message):
        return
    
    try:
        badwords = await db.get_badwords(message.chat.id)
        
        if not badwords:
            await message.reply_text("❌ No bad words to clear")
            return
        
        await db.clear_badwords(message.chat.id)
        await message.reply_text("✅ Cleared all bad words")
    except Exception as e:
        logger.error(f"Clear badwords error: {e}")
        await message.reply_text("❌ Error clearing bad words")

async def antibadwords_command(client: Client, message: Message):
    """Toggle bad word filter"""
    if not await check_admin_permission(message):
        return
    
    if len(message.command) < 2:
        settings = await db.get_group_settings(message.chat.id)
        status = "✅ ON" if settings.get("anti_badwords") else "❌ OFF"
        await message.reply_text(f"**Anti-BadWords:** {status}")
        return
    
    action = message.command[1].lower()
    
    if action == "on":
        await db.update_group_settings(message.chat.id, {"anti_badwords": True})
        await message.reply_text("✅ Anti-BadWords filter enabled")
    elif action == "off":
        await db.update_group_settings(message.chat.id, {"anti_badwords": False})
        await message.reply_text("✅ Anti-BadWords filter disabled")
    else:
        await message.reply_text("**Usage:** `/antibadwords on/off`")

def register(app: Client):
    """Register badword handlers"""
    
    @app.on_message(filters.command("addbadword") & filters.group)
    async def addbadword_cmd(client: Client, message: Message):
        await addbadword_command(client, message)
    
    @app.on_message(filters.command("removebadword") & filters.group)
    async def removebadword_cmd(client: Client, message: Message):
        await removebadword_command(client, message)
    
    @app.on_message(filters.command("badwords") & filters.group)
    async def badwords_cmd(client: Client, message: Message):
        await badwords_command(client, message)
    
    @app.on_message(filters.command("clearbadwords") & filters.group)
    async def clearbadwords_cmd(client: Client, message: Message):
        await clearbadwords_command(client, message)
    
    @app.on_message(filters.command("antibadwords") & filters.group)
    async def antibadwords_cmd(client: Client, message: Message):
        await antibadwords_command(client, message)
