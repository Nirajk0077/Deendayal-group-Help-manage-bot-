"""
Permission checking utilities
"""
import logging
from pyrogram import Client
from pyrogram.types import Message, User
from pyrogram.errors import UserNotParticipant
from config import SUDO_USERS, MESSAGES

logger = logging.getLogger(__name__)

class PermissionChecker:
    """Check user permissions"""
    
    @staticmethod
    async def is_group_admin(client: Client, group_id: int, user_id: int) -> bool:
        """Check if user is group admin"""
        try:
            member = await client.get_chat_member(group_id, user_id)
            return member.status in ["administrator", "creator"]
        except UserNotParticipant:
            return False
        except Exception as e:
            logger.error(f"Error checking admin: {e}")
            return False
    
    @staticmethod
    async def is_group_owner(client: Client, group_id: int, user_id: int) -> bool:
        """Check if user is group owner"""
        try:
            member = await client.get_chat_member(group_id, user_id)
            return member.status == "creator"
        except UserNotParticipant:
            return False
        except Exception as e:
            logger.error(f"Error checking owner: {e}")
            return False
    
    @staticmethod
    async def is_sudo_user(user_id: int) -> bool:
        """Check if user is SUDO"""
        return user_id in SUDO_USERS
    
    @staticmethod
    async def can_delete_messages(client: Client, group_id: int, bot_id: int) -> bool:
        """Check if bot can delete messages"""
        try:
            member = await client.get_chat_member(group_id, bot_id)
            return member.can_delete_messages if member else False
        except Exception as e:
            logger.error(f"Error checking delete permission: {e}")
            return False
    
    @staticmethod
    async def can_restrict_members(client: Client, group_id: int, bot_id: int) -> bool:
        """Check if bot can restrict members"""
        try:
            member = await client.get_chat_member(group_id, bot_id)
            return member.can_restrict_members if member else False
        except Exception as e:
            logger.error(f"Error checking restrict permission: {e}")
            return False
    
    @staticmethod
    async def can_pin_messages(client: Client, group_id: int, bot_id: int) -> bool:
        """Check if bot can pin messages"""
        try:
            member = await client.get_chat_member(group_id, bot_id)
            return member.can_pin_messages if member else False
        except Exception as e:
            logger.error(f"Error checking pin permission: {e}")
            return False

class MessageChecker:
    """Check message properties"""
    
    @staticmethod
    def is_reply(message: Message) -> bool:
        """Check if message is a reply"""
        return message.reply_to_message is not None
    
    @staticmethod
    def is_forwarded(message: Message) -> bool:
        """Check if message is forwarded"""
        return (
            message.forward_from is not None or
            message.forward_from_chat is not None or
            message.forward_origin is not None
        )
    
    @staticmethod
    def has_text(message: Message) -> bool:
        """Check if message has text"""
        return message.text is not None and len(message.text) > 0
    
    @staticmethod
    def has_caption(message: Message) -> bool:
        """Check if message has caption"""
        return message.caption is not None and len(message.caption) > 0
    
    @staticmethod
    def has_media(message: Message) -> bool:
        """Check if message has media"""
        return (
            message.photo is not None or
            message.video is not None or
            message.audio is not None or
            message.document is not None or
            message.animation is not None or
            message.video_note is not None or
            message.voice is not None or
            message.sticker is not None
        )
    
    @staticmethod
    def get_full_text(message: Message) -> str:
        """Get full text (text + caption)"""
        text = message.text or ""
        caption = message.caption or ""
        return f"{text} {caption}".strip()

class UserChecker:
    """Check user properties"""
    
    @staticmethod
    def is_bot(user: User) -> bool:
        """Check if user is a bot"""
        return user.is_bot if user else False
    
    @staticmethod
    def is_self(user_id: int, self_id: int) -> bool:
        """Check if user is self"""
        return user_id == self_id
    
    @staticmethod
    def get_username(user: User) -> str:
        """Get user username"""
        return f"@{user.username}" if user and user.username else "Unknown"
    
    @staticmethod
    def get_mention(user: User) -> str:
        """Get user mention"""
        if not user:
            return "Unknown User"
        
        if user.username:
            return f"@{user.username}"
        
        name = user.first_name or "User"
        if user.last_name:
            name += f" {user.last_name}"
        
        return f"[{name}](tg://user?id={user.id})"

class ChatChecker:
    """Check chat properties"""
    
    @staticmethod
    def is_private(message: Message) -> bool:
        """Check if chat is private"""
        return message.chat.type == "private"
    
    @staticmethod
    def is_group(message: Message) -> bool:
        """Check if chat is group"""
        return message.chat.type in ["group", "supergroup"]
    
    @staticmethod
    def is_channel(message: Message) -> bool:
        """Check if chat is channel"""
        return message.chat.type == "channel"

async def check_admin_permission(message: Message) -> bool:
    """Check if sender is admin"""
    if not message.chat:
        return False
    
    if not ChatChecker.is_group(message):
        await message.reply_text(MESSAGES["group_only"])
        return False
    
    if await PermissionChecker.is_sudo_user(message.from_user.id):
        return True
    
    is_admin = await PermissionChecker.is_group_admin(
        message._client,
        message.chat.id,
        message.from_user.id
    )
    
    if not is_admin:
        await message.reply_text(MESSAGES["admin_only"])
        return False
    
    return True

async def check_group_only(message: Message) -> bool:
    """Check if command is in group"""
    if not ChatChecker.is_group(message):
        await message.reply_text(MESSAGES["group_only"])
        return False
    return True
