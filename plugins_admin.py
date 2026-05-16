"""
Admin commands handler
"""
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from pyrogram.errors import FloodWait
from database import Database
from utils_permissions import check_admin_permission, PermissionChecker, ChatChecker
from config import FLOODWAIT, MESSAGES

logger = logging.getLogger(__name__)
db = Database()

async def ban_command(client: Client, message: Message):
    """Ban user"""
    if not await check_admin_permission(message):
        return
    
    user_id = None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1].replace("@", ""))
        except:
            pass
    
    if not user_id:
        await message.reply_text("❌ No user specified. Reply to message or use `/ban user_id`")
        return
    
    try:
        if await PermissionChecker.is_group_admin(client, message.chat.id, user_id):
            await message.reply_text("❌ Cannot ban group admins")
            return
        
        await client.ban_chat_member(message.chat.id, user_id)
        await message.reply_text(f"✅ User banned")
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        logger.error(f"Ban error: {e}")
        await message.reply_text("❌ Error banning user")

async def unban_command(client: Client, message: Message):
    """Unban user"""
    if not await check_admin_permission(message):
        return
    
    if len(message.command) < 2:
        await message.reply_text("**Usage:** `/unban user_id`")
        return
    
    try:
        user_id = int(message.command[1])
        await client.unban_chat_member(message.chat.id, user_id)
        await message.reply_text("✅ User unbanned")
    except Exception as e:
        logger.error(f"Unban error: {e}")
        await message.reply_text("❌ Error unbanning user")

async def mute_command(client: Client, message: Message):
    """Mute user"""
    if not await check_admin_permission(message):
        return
    
    user_id = None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1].replace("@", ""))
        except:
            pass
    
    if not user_id:
        await message.reply_text("❌ No user specified")
        return
    
    try:
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            ChatPermissions()
        )
        await message.reply_text("✅ User muted")
    except Exception as e:
        logger.error(f"Mute error: {e}")
        await message.reply_text("❌ Error muting user")

async def unmute_command(client: Client, message: Message):
    """Unmute user"""
    if not await check_admin_permission(message):
        return
    
    user_id = None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1].replace("@", ""))
        except:
            pass
    
    if not user_id:
        await message.reply_text("❌ No user specified")
        return
    
    try:
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
        await message.reply_text("✅ User unmuted")
    except Exception as e:
        logger.error(f"Unmute error: {e}")
        await message.reply_text("❌ Error unmuting user")

async def warn_command(client: Client, message: Message):
    """Warn user"""
    if not await check_admin_permission(message):
        return
    
    user_id = None
    reason = None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        if len(message.command) > 1:
            reason = " ".join(message.command[1:])
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1].replace("@", ""))
            if len(message.command) > 2:
                reason = " ".join(message.command[2:])
        except:
            pass
    
    if not user_id:
        await message.reply_text("❌ No user specified")
        return
    
    try:
        settings = await db.get_group_settings(message.chat.id)
        warn_limit = settings.get("warn_limit", 3)
        
        warn_count = await db.add_warning(message.chat.id, user_id, reason)
        
        text = f"⚠️ User warned. ({warn_count}/{warn_limit})"
        
        if warn_count >= warn_limit:
            await client.ban_chat_member(message.chat.id, user_id)
            text += "\n🚫 User banned (warn limit reached)"
            await db.reset_warnings(message.chat.id, user_id)
        
        await message.reply_text(text)
    except Exception as e:
        logger.error(f"Warn error: {e}")
        await message.reply_text("❌ Error warning user")

async def promote_command(client: Client, message: Message):
    """Promote user to admin"""
    if not await check_admin_permission(message):
        return
    
    user_id = None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1].replace("@", ""))
        except:
            pass
    
    if not user_id:
        await message.reply_text("❌ No user specified")
        return
    
    try:
        from pyrogram.types import ChatPrivileges
        await client.promote_chat_member(
            message.chat.id,
            user_id,
            privileges=ChatPrivileges(
                can_manage_messages=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_manage_video_chats=True,
            )
        )
        await message.reply_text("✅ User promoted")
    except Exception as e:
        logger.error(f"Promote error: {e}")
        await message.reply_text("❌ Error promoting user")

async def demote_command(client: Client, message: Message):
    """Demote user from admin"""
    if not await check_admin_permission(message):
        return
    
    user_id = None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1].replace("@", ""))
        except:
            pass
    
    if not user_id:
        await message.reply_text("❌ No user specified")
        return
    
    try:
        from pyrogram.types import ChatPrivileges
        await client.promote_chat_member(
            message.chat.id,
            user_id,
            privileges=ChatPrivileges()
        )
        await message.reply_text("✅ User demoted")
    except Exception as e:
        logger.error(f"Demote error: {e}")
        await message.reply_text("❌ Error demoting user")

async def kick_command(client: Client, message: Message):
    """Kick user from group"""
    if not await check_admin_permission(message):
        return
    
    user_id = None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1].replace("@", ""))
        except:
            pass
    
    if not user_id:
        await message.reply_text("❌ No user specified")
        return
    
    try:
        await client.ban_chat_member(message.chat.id, user_id)
        await asyncio.sleep(1)
        await client.unban_chat_member(message.chat.id, user_id)
        await message.reply_text("✅ User kicked")
    except Exception as e:
        logger.error(f"Kick error: {e}")
        await message.reply_text("❌ Error kicking user")

async def purge_command(client: Client, message: Message):
    """Delete messages"""
    if not await check_admin_permission(message):
        return
    
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to purge from")
        return
    
    count = 0
    try:
        async for msg in client.get_chat_history(
            message.chat.id,
            offset_id=message.reply_to_message.message_id,
            reverse=True
        ):
            if count >= 100:
                break
            try:
                await msg.delete()
                count += 1
            except:
                pass
        
        await message.reply_text(f"✅ Purged {count} messages")
    except Exception as e:
        logger.error(f"Purge error: {e}")
        await message.reply_text("❌ Error purging messages")

async def id_command(client: Client, message: Message):
    """Get ID information"""
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.from_user.id
    
    text = f"""
**🔍 ID Information**

**Chat ID:** `{message.chat.id}`
**User ID:** `{user_id}`
**Message ID:** `{message.message_id}`
"""
    await message.reply_text(text)

async def info_command(client: Client, message: Message):
    """Get user info"""
    user_id = None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1].replace("@", ""))
        except:
            pass
    
    if not user_id:
        await message.reply_text("❌ No user specified")
        return
    
    try:
        member = await client.get_chat_member(message.chat.id, user_id)
        user = member.user
        
        text = f"""
**👤 User Information**

**Name:** {user.first_name} {user.last_name or ''}
**Username:** @{user.username or 'None'}
**ID:** `{user.id}`
**Status:** {member.status}
**Bot:** {'Yes' if user.is_bot else 'No'}
"""
        await message.reply_text(text)
    except Exception as e:
        logger.error(f"Info error: {e}")
        await message.reply_text("❌ Error getting user info")

def register(app: Client):
    """Register admin handlers"""
    handlers = [
        (filters.command("ban"), ban_command),
        (filters.command("unban"), unban_command),
        (filters.command("mute"), mute_command),
        (filters.command("unmute"), unmute_command),
        (filters.command("warn"), warn_command),
        (filters.command("promote"), promote_command),
        (filters.command("demote"), demote_command),
        (filters.command("kick"), kick_command),
        (filters.command("purge"), purge_command),
        (filters.command("id"), id_command),
        (filters.command("info"), info_command),
    ]
    
    for filter_obj, handler in handlers:
        @app.on_message(filter_obj & filters.group)
        async def handle(client: Client, message: Message, h=handler):
            try:
                await h(client, message)
            except Exception as e:
                logger.error(f"Handler error: {e}")
