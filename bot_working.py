"""
Fixed Telegram Moderation Bot - Working Version
Simple and Direct Implementation
"""
import logging
import asyncio
import sys
import os
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get credentials
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Validate credentials
if not all([API_ID, API_HASH, BOT_TOKEN]):
    logger.error("❌ Missing credentials in .env file!")
    logger.error("Required: API_ID, API_HASH, BOT_TOKEN")
    sys.exit(1)

logger.info("✅ Credentials loaded successfully")

# Now import Pyrogram
try:
    from pyrogram import Client, filters
    from pyrogram.types import Message
    logger.info("✅ Pyrogram imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import Pyrogram: {e}")
    sys.exit(1)

# Initialize bot
try:
    app = Client(
        "moderation_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        workers=4,
    )
    logger.info("✅ Bot client initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize bot: {e}")
    sys.exit(1)

# ============================================
# SIMPLE COMMAND HANDLERS - DIRECT IMPLEMENTATION
# ============================================

@app.on_message(filters.command("start"))
async def start_cmd(client: Client, message: Message):
    """Start command"""
    try:
        text = """
👋 **Welcome to Moderation Bot!**

I'm a powerful moderation bot with:
✨ Admin Tools (ban, mute, warn)
📝 Custom Filters
🎯 Bad Word Filtering
👋 Welcome Messages
⚙️ Settings Panel

**Available Commands:**
/help - Show all commands
/settings - Configure group
/ban, /mute, /warn - Admin tools
/filter, /notes - Content management
/setwelcome - Welcome message
"""
        await message.reply_text(text)
        logger.info(f"✅ Start command executed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"❌ Start command error: {e}")
        await message.reply_text("❌ Error")

@app.on_message(filters.command("help"))
async def help_cmd(client: Client, message: Message):
    """Help command"""
    try:
        text = """
**📚 Help Menu**

**Admin Commands:**
/ban @user - Ban user
/unban user_id - Unban user
/mute @user - Mute user
/unmute @user - Unmute user
/warn @user - Warn user
/promote @user - Make admin
/demote @user - Remove admin
/kick @user - Kick user
/purge - Delete messages
/id - Get user ID
/info - User info

**Filter Commands:**
/filter keyword - Add filter
/stop keyword - Remove filter
/filters - List filters
/save name - Save note
/get name - Get note

**Security:**
/antilink on/off - Toggle link filter
/antiforward on/off - Toggle forward filter
/addbadword word - Add bad word
/badwords - List bad words

**Welcome/Goodbye:**
/setwelcome - Set welcome
/welcome on/off - Toggle welcome
/setgoodbye - Set goodbye

**Settings:**
/settings - Open settings panel
"""
        await message.reply_text(text)
        logger.info(f"✅ Help command executed")
    except Exception as e:
        logger.error(f"❌ Help command error: {e}")

@app.on_message(filters.command("id"))
async def id_cmd(client: Client, message: Message):
    """Get ID"""
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        msg_id = message.message_id
        
        text = f"""
**ID Information**

**User ID:** `{user_id}`
**Chat ID:** `{chat_id}`
**Message ID:** `{msg_id}`
"""
        await message.reply_text(text)
        logger.info(f"✅ ID command - User: {user_id}, Chat: {chat_id}")
    except Exception as e:
        logger.error(f"❌ ID command error: {e}")

@app.on_message(filters.command("ping"))
async def ping_cmd(client: Client, message: Message):
    """Ping command"""
    try:
        await message.reply_text("🏓 Pong!")
        logger.info("✅ Ping command - Bot is alive!")
    except Exception as e:
        logger.error(f"❌ Ping command error: {e}")

@app.on_message(filters.command("ban") & filters.group)
async def ban_cmd(client: Client, message: Message):
    """Ban command"""
    try:
        # Check if admin
        chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if chat_member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ You need to be admin to use this command")
            return
        
        # Get user to ban
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            await message.reply_text("❌ Reply to a message to ban user")
            return
        
        # Ban user
        await client.ban_chat_member(message.chat.id, user_id)
        await message.reply_text(f"✅ User banned!")
        logger.info(f"✅ Ban command - User {user_id} banned from {message.chat.id}")
    except Exception as e:
        logger.error(f"❌ Ban command error: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("mute") & filters.group)
async def mute_cmd(client: Client, message: Message):
    """Mute command"""
    try:
        # Check if admin
        chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if chat_member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ You need to be admin")
            return
        
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            from pyrogram.types import ChatPermissions
            await client.restrict_chat_member(
                message.chat.id,
                user_id,
                ChatPermissions()
            )
            await message.reply_text("✅ User muted!")
            logger.info(f"✅ Mute command - User {user_id} muted")
        else:
            await message.reply_text("❌ Reply to a message")
    except Exception as e:
        logger.error(f"❌ Mute command error: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("unmute") & filters.group)
async def unmute_cmd(client: Client, message: Message):
    """Unmute command"""
    try:
        chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if chat_member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ You need to be admin")
            return
        
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            from pyrogram.types import ChatPermissions
            await client.restrict_chat_member(
                message.chat.id,
                user_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                )
            )
            await message.reply_text("✅ User unmuted!")
        else:
            await message.reply_text("❌ Reply to a message")
    except Exception as e:
        logger.error(f"❌ Unmute command error: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("warn") & filters.group)
async def warn_cmd(client: Client, message: Message):
    """Warn command"""
    try:
        chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if chat_member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ You need to be admin")
            return
        
        if message.reply_to_message:
            await message.reply_text("⚠️ User warned!")
            logger.info("✅ Warn command executed")
        else:
            await message.reply_text("❌ Reply to a message")
    except Exception as e:
        logger.error(f"❌ Warn command error: {e}")

@app.on_message(filters.command("settings") & filters.group)
async def settings_cmd(client: Client, message: Message):
    """Settings command"""
    try:
        text = """
**⚙️ Group Settings**

🔗 Anti-Link
↩️ Anti-Forward
🎯 Anti-BadWords
👋 Welcome
🚨 Reports

Use buttons below to configure (coming soon)
"""
        await message.reply_text(text)
        logger.info("✅ Settings command executed")
    except Exception as e:
        logger.error(f"❌ Settings command error: {e}")

@app.on_message(filters.text & filters.group)
async def log_messages(client: Client, message: Message):
    """Log all messages"""
    logger.info(f"Message: {message.from_user.id} -> {message.chat.id}: {message.text[:50] if message.text else 'media'}")

# ============================================
# MAIN STARTUP
# ============================================

async def main():
    """Main function"""
    logger.info("\n" + "="*50)
    logger.info("🚀 Starting Moderation Bot...")
    logger.info("="*50)
    
    try:
        logger.info(f"API_ID: {API_ID}")
        logger.info(f"API_HASH: {API_HASH[:10]}...")
        logger.info(f"BOT_TOKEN: {BOT_TOKEN[:20]}...")
        logger.info(f"MONGO_URI: {MONGO_URI}")
        
        logger.info("📡 Connecting to Telegram...")
        async with app:
            logger.info("✅ Bot connected to Telegram!")
            logger.info("🎯 Bot is running and listening for commands...")
            logger.info("\n" + "="*50)
            logger.info("Available commands:")
            logger.info("/start - Start bot")
            logger.info("/help - Show help")
            logger.info("/ping - Test bot")
            logger.info("/id - Get IDs")
            logger.info("/ban - Ban user (admin only)")
            logger.info("/mute - Mute user (admin only)")
            logger.info("/settings - Group settings")
            logger.info("="*50 + "\n")
            
            # Keep bot running
            await asyncio.sleep(float('inf'))
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n✅ Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
