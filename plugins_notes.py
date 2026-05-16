"""
Notes plugin
"""
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from utils_permissions import check_admin_permission

logger = logging.getLogger(__name__)
db = Database()

async def save_command(client: Client, message: Message):
    """Save note"""
    if not await check_admin_permission(message):
        return
    
    if len(message.command) < 2:
        await message.reply_text("**Usage:** `/save note_name`")
        return
    
    note_name = " ".join(message.command[1:])
    
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to save as note")
        return
    
    try:
        response_text = (
            message.reply_to_message.text or 
            message.reply_to_message.caption or 
            ""
        )
        
        success = await db.add_note(message.chat.id, note_name, response_text)
        
        if success:
            await message.reply_text(f"✅ Note `{note_name}` saved")
        else:
            await message.reply_text(f"⚠️ Note `{note_name}` already exists")
    except Exception as e:
        logger.error(f"Save error: {e}")
        await message.reply_text("❌ Error saving note")

async def get_command(client: Client, message: Message):
    """Get note"""
    if len(message.command) < 2:
        await message.reply_text("**Usage:** `/get note_name`")
        return
    
    note_name = " ".join(message.command[1:])
    
    try:
        note = await db.get_note(message.chat.id, note_name)
        
        if not note:
            await message.reply_text(f"❌ Note `{note_name}` not found")
            return
        
        await message.reply_text(note["content"], parse_mode="markdown")
    except Exception as e:
        logger.error(f"Get error: {e}")
        await message.reply_text("❌ Error retrieving note")

async def notes_command(client: Client, message: Message):
    """List notes"""
    try:
        notes_list = await db.get_notes(message.chat.id)
        
        if not notes_list:
            await message.reply_text("❌ No notes in this group")
            return
        
        text = "**📝 Saved Notes:**\n\n"
        for i, note in enumerate(notes_list, 1):
            text += f"`{i}.` `{note['name']}`\n"
        
        if len(text) > 4096:
            await message.reply_text(text[:4096])
        else:
            await message.reply_text(text)
    except Exception as e:
        logger.error(f"Notes error: {e}")
        await message.reply_text("❌ Error retrieving notes")

async def clearnotes_command(client: Client, message: Message):
    """Clear all notes"""
    if not await check_admin_permission(message):
        return
    
    try:
        notes_list = await db.get_notes(message.chat.id)
        
        if not notes_list:
            await message.reply_text("❌ No notes to remove")
            return
        
        count = await db.clear_notes(message.chat.id)
        await message.reply_text(f"✅ Removed {count} notes")
    except Exception as e:
        logger.error(f"Clearnotes error: {e}")
        await message.reply_text("❌ Error clearing notes")

def register(app: Client):
    """Register note handlers"""
    
    @app.on_message(filters.command("save") & filters.group)
    async def save_cmd(client: Client, message: Message):
        await save_command(client, message)
    
    @app.on_message(filters.command("get") & filters.group)
    async def get_cmd(client: Client, message: Message):
        await get_command(client, message)
    
    @app.on_message(filters.command("notes") & filters.group)
    async def notes_cmd(client: Client, message: Message):
        await notes_command(client, message)
    
    @app.on_message(filters.command("clearnotes") & filters.group)
    async def clearnotes_cmd(client: Client, message: Message):
        await clearnotes_command(client, message)
