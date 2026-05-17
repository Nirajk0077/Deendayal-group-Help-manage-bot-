"""
Telegram Moderation Bot - Fixed for Deployment
Works on Railway, Render, Koyeb, etc.
"""
import logging
import asyncio
import sys
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Import config (this will validate credentials)
try:
    from config import API_ID, API_HASH, BOT_TOKEN
    logger.info(f"✅ Credentials loaded: API_ID={API_ID}, BOT_TOKEN={BOT_TOKEN[:20]}...")
except ImportError as e:
    logger.error(f"❌ Import error: {e}")
    sys.exit(1)
except ValueError as e:
    logger.error(f"❌ Configuration error: {e}")
    sys.exit(1)

# Import Pyrogram
try:
    from pyrogram import Client, filters
    from pyrogram.types import Message
    logger.info("✅ Pyrogram imported")
except ImportError as e:
    logger.error(f"❌ Failed to import Pyrogram: {e}")
    logger.error("Install with: pip install pyrogram TgCrypto")
    sys.exit(1)

# Initialize bot client
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
# COMMAND HANDLERS
# ============================================

@app.on_message(filters.command("start"))
async def start_cmd(client: Client, message: Message):
    try:
        text = """
👋 **Welcome to Moderation Bot!**

I'm a powerful moderation bot with:
✨ Admin Tools (ban, mute, warn)
📝 Custom Filters
🎯 Bad Word Filtering
👋 Welcome Messages

**Commands:**
/help - Show all commands
/ping - Test bot
/ban - Ban user
/mute - Mute user
/warn - Warn user
/settings - Configure group
"""
        await message.reply_text(text)
        logger.info(f"✅ /start by user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error: {e}")

@app.on_message(filters.command("help"))
async def help_cmd(client: Client, message: Message):
    try:
        text = """
**📚 Help Menu**

**Admin Commands:**
/ban @user - Ban user
/unban id - Unban user
/mute @user - Mute user
/unmute @user - Unmute user
/warn @user - Warn user
/kick @user - Kick user

**Info Commands:**
/id - Get IDs
/info @user - User info
/ping - Test bot

**Settings:**
/settings - Configure group
/help - Show this help
"""
        await message.reply_text(text)
    except Exception as e:
        logger.error(f"Error: {e}")

@app.on_message(filters.command("ping"))
async def ping_cmd(client: Client, message: Message):
    try:
        await message.reply_text("🏓 **Pong!** Bot is alive!")
        logger.info("✅ /ping executed")
    except Exception as e:
        logger.error(f"Error: {e}")

@app.on_message(filters.command("id"))
async def id_cmd(client: Client, message: Message):
    try:
        text = f"""
**ID Information**

**User ID:** `{message.from_user.id}`
**Chat ID:** `{message.chat.id}`
**Message ID:** `{message.message_id}`
"""
        await message.reply_text(text)
    except Exception as e:
        logger.error(f"Error: {e}")

@app.on_message(filters.command("ban") & filters.group)
async def ban_cmd(client: Client, message: Message):
    try:
        # Check admin
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ You need to be admin")
            return
        
        if not message.reply_to_message:
            await message.reply_text("❌ Reply to a message to ban")
            return
        
        user_id = message.reply_to_message.from_user.id
        await client.ban_chat_member(message.chat.id, user_id)
        await message.reply_text("✅ User banned!")
        logger.info(f"✅ Banned user {user_id}")
    except Exception as e:
        logger.error(f"Error: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("mute") & filters.group)
async def mute_cmd(client: Client, message: Message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ You need to be admin")
            return
        
        if not message.reply_to_message:
            await message.reply_text("❌ Reply to a message to mute")
            return
        
        user_id = message.reply_to_message.from_user.id
        from pyrogram.types import ChatPermissions
        await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions())
        await message.reply_text("✅ User muted!")
    except Exception as e:
        logger.error(f"Error: {e}")

@app.on_message(filters.command("unmute") & filters.group)
async def unmute_cmd(client: Client, message: Message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ You need to be admin")
            return
        
        if not message.reply_to_message:
            await message.reply_text("❌ Reply to a message to unmute")
            return
        
        user_id = message.reply_to_message.from_user.id
        from pyrogram.types import ChatPermissions
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            ChatPermissions(can_send_messages=True, can_send_media_messages=True)
        )
        await message.reply_text("✅ User unmuted!")
    except Exception as e:
        logger.error(f"Error: {e}")

@app.on_message(filters.command("warn") & filters.group)
async def warn_cmd(client: Client, message: Message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ You need to be admin")
            return
        
        if message.reply_to_message:
            await message.reply_text("⚠️ User warned!")
        else:
            await message.reply_text("❌ Reply to a message to warn")
    except Exception as e:
        logger.error(f"Error: {e}")

@app.on_message(filters.command("kick") & filters.group)
async def kick_cmd(client: Client, message: Message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ You need to be admin")
            return
        
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            await client.ban_chat_member(message.chat.id, user_id)
            await asyncio.sleep(1)
            await client.unban_chat_member(message.chat.id, user_id)
            await message.reply_text("✅ User kicked!")
        else:
            await message.reply_text("❌ Reply to a message to kick")
    except Exception as e:
        logger.error(f"Error: {e}")

@app.on_message(filters.command("settings") & filters.group)
async def settings_cmd(client: Client, message: Message):
    try:
        text = """
**⚙️ Group Settings**

🔗 Anti-Link
↩️ Anti-Forward
🎯 Anti-BadWords
👋 Welcome
🚨 Reports

(Settings panel coming soon)
"""
        await message.reply_text(text)
    except Exception as e:
        logger.error(f"Error: {e}")

# ============================================
# STARTUP
# ============================================

async def main():
    logger.info("\n" + "="*50)
    logger.info("🚀 Starting Moderation Bot v1.0")
    logger.info("="*50)
    
    try:
        logger.info(f"API_ID: {API_ID}")
        logger.info(f"API_HASH: {API_HASH[:20]}...")
        
        logger.info("📡 Connecting to Telegram...")
        async with app:
            logger.info("✅ Bot connected!")
            logger.info("🎯 Bot is running...")
            logger.info("\nAvailable commands:")
            logger.info("/ping - Test bot")
            logger.info("/help - Show commands")
            logger.info("/ban - Ban user (admin)")
            logger.info("/mute - Mute user (admin)")
            logger.info("/id - Get IDs")
            logger.info("="*50 + "\n")
            
            await asyncio.sleep(float('inf'))
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n✅ Bot stopped")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
