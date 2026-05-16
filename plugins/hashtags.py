"""
Hashtag triggers plugin
"""
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database

logger = logging.getLogger(__name__)
db = Database()

async def hashtag_trigger(client: Client, message: Message):
    """Trigger hashtag filters and notes"""
    if not message.text:
        return
    
    # Check if message starts with hashtag
    if not message.text.startswith("#"):
        return
    
    try:
        hashtag = message.text.split()[0].lower()
        
        # Get corresponding note
        note_name = hashtag[1:]  # Remove #
        note = await db.get_note(message.chat.id, note_name)
        
        if note:
            await message.reply_text(note["content"], parse_mode="markdown")
    except Exception as e:
        logger.error(f"Hashtag trigger error: {e}")

def register(app: Client):
    """Register hashtag handlers"""
    
    @app.on_message(filters.text & filters.group & filters.regex(r"^#"))
    async def hashtag_cmd(client: Client, message: Message):
        await hashtag_trigger(client, message)
