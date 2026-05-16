"""
Advanced Telegram Moderation Bot
Rose Bot + Support Bot Hybrid
Full production-ready implementation
"""
import logging
import asyncio
import sys
from pathlib import Path

from pyrogram import Client, idle
from pyrogram.errors import RPCError
from aiohttp import web

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import BOT_TOKEN, API_ID, API_HASH
from database import Database

# Initialize bot
app = Client(
    "moderation_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=24,
    max_concurrent_transmissions=10,
    plugins=dict(root="plugins"),
)

async def load_plugins():
    """Load all plugin modules"""
    try:
        # Import all plugins to register handlers
        from plugins import start, help_menu, admin, moderation, filters, notes, hashtags
        from plugins import security, welcome, reports, settings, badwords
        
        logger.info("✅ All plugins loaded successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Error loading plugins: {e}")
        import traceback
        traceback.print_exc()
        return False

async def on_startup():
    """Bot startup sequence"""
    logger.info("🚀 Starting Moderation Bot v1.0.0...")
    
    try:
        # Initialize database
        logger.info("🔄 Connecting to MongoDB...")
        try:
            db = Database()
            success = await db.connect()
            if not success:
                logger.error("❌ Database connection failed, continuing anyway")
            else:
                logger.info("✅ Database connected")
        except Exception as e:
            logger.error(f"❌ Database connection error: {e}")
        
        # Load plugins
        plugins_ok = await load_plugins()
        if not plugins_ok:
            return False
        
        logger.info("✅ Bot startup completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        return False

async def on_shutdown():
    """Bot shutdown sequence"""
    logger.info("🛑 Shutting down bot...")
    try:
        db = Database()
        await db.disconnect()
        logger.info("✅ Shutdown completed")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

async def health_check(request):
    return web.Response(text="OK")

async def main():
    """Main bot function"""
    startup_ok = await on_startup()
    if not startup_ok:
        logger.error("Startup failed, exiting")
        return
    
    # Start health check server
    app_web = web.Application()
    app_web.router.add_get('/', health_check)
    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()
    logger.info("✅ Health check server started on port 8000")

    try:
        logger.info("🎯 Bot is running...")
        await app.start()
        await idle()
        await app.stop()
    except KeyboardInterrupt:
        logger.info("⏹️ Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await on_shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
    except Exception as e:
        logger.error(f"Error: {e}")
