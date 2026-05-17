"""
Telegram Moderation Bot - Simple Working Version
No database imports - works on Railway immediately
"""
import logging
import asyncio
import sys
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Get credentials
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Validate
if not API_ID or API_ID == 0:
    logger.error("❌ API_ID missing in .env")
    sys.exit(1)
if not API_HASH:
    logger.error("❌ API_HASH missing in .env")
    sys.exit(1)
if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN missing in .env")
    sys.exit(1)

logger.info("✅ Credentials loaded")

# Import Pyrogram
try:
    from pyrogram import Client, filters
    from pyrogram.types import Message
except ImportError:
    logger.error("❌ Pyrogram not installed. Run: pip install pyrogram TgCrypto")
    sys.exit(1)

# Create bot
app = Client(
    "moderation_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

logger.info("✅ Bot initialized")

# ============================================
# COMMANDS
# ============================================

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    try:
        await message.reply_text("""
👋 **Welcome to Moderation Bot!**

I'm a powerful moderation bot.

**Commands:**
/help - Show all commands
/ping - Test bot
/ban @user - Ban user
/mute @user - Mute user
/unmute @user - Unmute user
/warn @user - Warn user
/kick @user - Kick user
/id - Get IDs
/info @user - User info
/settings - Group settings
""")
    except Exception as e:
        logger.error(f"Error: {e}")

@app.on_message(filters.command("help"))
async def help_cmd(client: Client, message: Message):
    try:
        await message.reply_text("""
**📚 Help Menu**

**Admin Commands:**
/ban @user - Ban user from group
/unban user_id - Unban user
/mute @user - Mute user (no messages)
/unmute @user - Let user talk again
/warn @user - Warn user
/kick @user - Remove user from group

**Info Commands:**
/id - Get your ID, chat ID, message ID
/info @user - Get user information
/ping - Test if bot is alive

**Group Commands:**
/settings - Configure group
/help - Show this help

**Note:** Most commands need you to be group admin!
""")
    except Exception as e:
        logger.error(f"Error: {e}")

@app.on_message(filters.command("ping"))
async def ping(client: Client, message: Message):
    try:
        await message.reply_text("🏓 **Pong!** Bot is alive! ✅")
    except Exception as e:
        logger.error(f"Error: {e}")

@app.on_message(filters.command("id"))
async def get_id(client: Client, message: Message):
    try:
        text = f"""
**ID Information:**

👤 Your ID: `{message.from_user.id}`
💬 Chat ID: `{message.chat.id}`
📧 Message ID: `{message.message_id}`
"""
        await message.reply_text(text)
    except Exception as e:
        logger.error(f"Error: {e}")

@app.on_message(filters.command("ban") & filters.group)
async def ban(client: Client, message: Message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ You must be group admin!")
            return
        
        if not message.reply_to_message:
            await message.reply_text("❌ Reply to a message to ban!")
            return
        
        user_id = message.reply_to_message.from_user.id
        await client.ban_chat_member(message.chat.id, user_id)
        await message.reply_text(f"✅ User banned!")
    except Exception as e:
        logger.error(f"Ban error: {e}")
        await message.reply_text(f"❌ Error: {str(e)[:100]}")

@app.on_message(filters.command("mute") & filters.group)
async def mute(client: Client, message: Message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ You must be admin!")
            return
        
        if not message.reply_to_message:
            await message.reply_text("❌ Reply to mute!")
            return
        
        user_id = message.reply_to_message.from_user.id
        from pyrogram.types import ChatPermissions
        await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions())
        await message.reply_text("✅ User muted!")
    except Exception as e:
        logger.error(f"Mute error: {e}")

@app.on_message(filters.command("unmute") & filters.group)
async def unmute(client: Client, message: Message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ You must be admin!")
            return
        
        if not message.reply_to_message:
            await message.reply_text("❌ Reply to unmute!")
            return
        
        user_id = message.reply_to_message.from_user.id
        from pyrogram.types import ChatPermissions
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            ChatPermissions(can_send_messages=True)
        )
        await message.reply_text("✅ User unmuted!")
    except Exception as e:
        logger.error(f"Unmute error: {e}")

@app.on_message(filters.command("warn") & filters.group)
async def warn(client: Client, message: Message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ You must be admin!")
            return
        
        if not message.reply_to_message:
            await message.reply_text("❌ Reply to warn!")
            return
        
        await message.reply_text("⚠️ User warned!")
    except Exception as e:
        logger.error(f"Warn error: {e}")

@app.on_message(filters.command("kick") & filters.group)
async def kick(client: Client, message: Message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ You must be admin!")
            return
        
        if not message.reply_to_message:
            await message.reply_text("❌ Reply to kick!")
            return
        
        user_id = message.reply_to_message.from_user.id
        await client.ban_chat_member(message.chat.id, user_id)
        await asyncio.sleep(1)
        await client.unban_chat_member(message.chat.id, user_id)
        await message.reply_text("✅ User kicked!")
    except Exception as e:
        logger.error(f"Kick error: {e}")

@app.on_message(filters.command("info"))
async def info(client: Client, message: Message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        else:
            user = message.from_user
        
        text = f"""
**👤 User Info:**

**Name:** {user.first_name} {user.last_name or ''}
**Username:** @{user.username or 'None'}
**ID:** `{user.id}`
"""
        await message.reply_text(text)
    except Exception as e:
        logger.error(f"Error: {e}")

@app.on_message(filters.command("settings"))
async def settings(client: Client, message: Message):
    try:
        await message.reply_text("""
⚙️ **Group Settings**

Coming soon!
""")
    except Exception as e:
        logger.error(f"Error: {e}")

# ============================================
# MAIN
# ============================================

async def main():
    logger.info("\n" + "="*60)
    logger.info("🚀 Starting Telegram Moderation Bot")
    logger.info("="*60)
    
    try:
        async with app:
            logger.info("✅ Bot connected!")
            logger.info("\n🎯 Commands: /start /help /ping /ban /mute /warn /id")
            logger.info("="*60 + "\n")
            
            await asyncio.sleep(float('inf'))
    except Exception as e:
        logger.error(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n✅ Bot stopped")
