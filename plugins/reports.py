"""
Reports plugin
"""
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from config import LOG_GROUP

logger = logging.getLogger(__name__)
db = Database()

async def report_command(client: Client, message: Message):
    """Report message"""
    settings = await db.get_group_settings(message.chat.id)
    
    if not settings.get("reports_enabled", True):
        await message.reply_text("❌ Reports are disabled in this group")
        return
    
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to report")
        return
    
    try:
        reported_msg = message.reply_to_message
        
        text = f"""
**📢 New Report**

**Group:** {message.chat.title}
**Reporter:** {message.from_user.mention}
**Reported User:** {reported_msg.from_user.mention if reported_msg.from_user else "Unknown"}
**Message ID:** {reported_msg.message_id}

**Message Content:**
{reported_msg.text or reported_msg.caption or "No text"}
"""
        
        # Store report in database
        await db.add_report(
            message.chat.id,
            message.from_user.id,
            reported_msg.from_user.id if reported_msg.from_user else 0,
            reported_msg.message_id
        )
        
        # Notify in log group if configured
        if LOG_GROUP and LOG_GROUP < 0:
            try:
                await client.send_message(LOG_GROUP, text)
            except Exception as e:
                logger.error(f"Error sending to log group: {e}")
        
        await message.reply_text("✅ Report sent to admins")
    
    except Exception as e:
        logger.error(f"Report error: {e}")
        await message.reply_text("❌ Error submitting report")

def register(app: Client):
    """Register report handlers"""
    
    @app.on_message(filters.command("report") & filters.group)
    async def report_cmd(client: Client, message: Message):
        await report_command(client, message)
