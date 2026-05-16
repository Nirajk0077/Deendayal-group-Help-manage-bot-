"""
MongoDB async database operations
"""
import logging
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DB_NAME, COLLECTIONS, DEFAULT_SETTINGS

logger = logging.getLogger(__name__)

class Database:
    """MongoDB database handler with async support"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
        return cls._instance
    
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(MONGO_URI)
            self.db = self.client[DB_NAME]
            await self.db.command('ping')
            logger.info("✅ MongoDB connected")
            await self._ensure_indexes()
            return True
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Database disconnected")
    
    async def _ensure_indexes(self):
        """Create necessary indexes"""
        try:
            await self.db.group_settings.create_index("group_id")
            await self.db.filters.create_index([("group_id", 1), ("keyword", 1)])
            await self.db.badwords.create_index("group_id")
            await self.db.notes.create_index([("group_id", 1), ("name", 1)])
            await self.db.warnings.create_index([("group_id", 1), ("user_id", 1)])
        except Exception as e:
            logger.warning(f"Index creation warning: {e}")
    
    async def get_collection(self, name: str):
        """Get collection by name"""
        if not self.db:
            raise RuntimeError("Database not connected")
        return self.db[name]
    
    # Group Settings Operations
    async def get_group_settings(self, group_id: int) -> dict:
        """Get group settings"""
        try:
            col = await self.get_collection(COLLECTIONS["group_settings"])
            settings = await col.find_one({"group_id": group_id})
            
            if not settings:
                settings = {
                    "group_id": group_id,
                    "created_at": datetime.utcnow(),
                    **DEFAULT_SETTINGS
                }
                await col.insert_one(settings)
            
            return settings
        except Exception as e:
            logger.error(f"Error getting settings: {e}")
            return {}
    
    async def update_group_settings(self, group_id: int, settings: dict) -> bool:
        """Update group settings"""
        try:
            col = await self.get_collection(COLLECTIONS["group_settings"])
            settings["updated_at"] = datetime.utcnow()
            
            result = await col.update_one(
                {"group_id": group_id},
                {"$set": settings},
                upsert=True
            )
            return bool(result.modified_count or result.upserted_id)
        except Exception as e:
            logger.error(f"Error updating settings: {e}")
            return False
    
    # Filter Operations
    async def get_filters(self, group_id: int) -> list:
        """Get all filters for group"""
        try:
            col = await self.get_collection(COLLECTIONS["filters"])
            filters = await col.find({"group_id": group_id}).to_list(None)
            return filters or []
        except Exception as e:
            logger.error(f"Error getting filters: {e}")
            return []
    
    async def add_filter(self, group_id: int, keyword: str, response: str, buttons: list = None) -> bool:
        """Add filter"""
        try:
            col = await self.get_collection(COLLECTIONS["filters"])
            
            existing = await col.find_one({
                "group_id": group_id,
                "keyword": keyword.lower()
            })
            
            if existing:
                return False
            
            await col.insert_one({
                "group_id": group_id,
                "keyword": keyword.lower(),
                "response": response,
                "buttons": buttons or [],
                "created_at": datetime.utcnow()
            })
            return True
        except Exception as e:
            logger.error(f"Error adding filter: {e}")
            return False
    
    async def remove_filter(self, group_id: int, keyword: str) -> bool:
        """Remove filter"""
        try:
            col = await self.get_collection(COLLECTIONS["filters"])
            result = await col.delete_one({
                "group_id": group_id,
                "keyword": keyword.lower()
            })
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error removing filter: {e}")
            return False
    
    async def clear_filters(self, group_id: int) -> int:
        """Clear all filters for group"""
        try:
            col = await self.get_collection(COLLECTIONS["filters"])
            result = await col.delete_many({"group_id": group_id})
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error clearing filters: {e}")
            return 0
    
    # Bad Words Operations
    async def get_badwords(self, group_id: int) -> list:
        """Get all bad words"""
        try:
            col = await self.get_collection(COLLECTIONS["badwords"])
            doc = await col.find_one({"group_id": group_id})
            return doc.get("words", []) if doc else []
        except Exception as e:
            logger.error(f"Error getting badwords: {e}")
            return []
    
    async def add_badword(self, group_id: int, word: str) -> bool:
        """Add bad word"""
        try:
            col = await self.get_collection(COLLECTIONS["badwords"])
            result = await col.update_one(
                {"group_id": group_id},
                {"$addToSet": {"words": word.lower()}},
                upsert=True
            )
            return bool(result.modified_count or result.upserted_id)
        except Exception as e:
            logger.error(f"Error adding badword: {e}")
            return False
    
    async def remove_badword(self, group_id: int, word: str) -> bool:
        """Remove bad word"""
        try:
            col = await self.get_collection(COLLECTIONS["badwords"])
            result = await col.update_one(
                {"group_id": group_id},
                {"$pull": {"words": word.lower()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error removing badword: {e}")
            return False
    
    async def clear_badwords(self, group_id: int) -> bool:
        """Clear all bad words"""
        try:
            col = await self.get_collection(COLLECTIONS["badwords"])
            await col.delete_one({"group_id": group_id})
            return True
        except Exception as e:
            logger.error(f"Error clearing badwords: {e}")
            return False
    
    # Notes Operations
    async def get_notes(self, group_id: int) -> list:
        """Get all notes"""
        try:
            col = await self.get_collection(COLLECTIONS["notes"])
            notes = await col.find({"group_id": group_id}).to_list(None)
            return notes or []
        except Exception as e:
            logger.error(f"Error getting notes: {e}")
            return []
    
    async def get_note(self, group_id: int, name: str):
        """Get specific note"""
        try:
            col = await self.get_collection(COLLECTIONS["notes"])
            return await col.find_one({
                "group_id": group_id,
                "name": name.lower()
            })
        except Exception as e:
            logger.error(f"Error getting note: {e}")
            return None
    
    async def add_note(self, group_id: int, name: str, content: str, buttons: list = None) -> bool:
        """Add note"""
        try:
            col = await self.get_collection(COLLECTIONS["notes"])
            
            existing = await col.find_one({
                "group_id": group_id,
                "name": name.lower()
            })
            
            if existing:
                return False
            
            await col.insert_one({
                "group_id": group_id,
                "name": name.lower(),
                "content": content,
                "buttons": buttons or [],
                "created_at": datetime.utcnow()
            })
            return True
        except Exception as e:
            logger.error(f"Error adding note: {e}")
            return False
    
    async def remove_note(self, group_id: int, name: str) -> bool:
        """Remove note"""
        try:
            col = await self.get_collection(COLLECTIONS["notes"])
            result = await col.delete_one({
                "group_id": group_id,
                "name": name.lower()
            })
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error removing note: {e}")
            return False
    
    async def clear_notes(self, group_id: int) -> int:
        """Clear all notes"""
        try:
            col = await self.get_collection(COLLECTIONS["notes"])
            result = await col.delete_many({"group_id": group_id})
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error clearing notes: {e}")
            return 0
    
    # Warning Operations
    async def add_warning(self, group_id: int, user_id: int, reason: str = None) -> int:
        """Add warning"""
        try:
            col = await self.get_collection(COLLECTIONS["warnings"])
            
            result = await col.update_one(
                {"group_id": group_id, "user_id": user_id},
                {
                    "$inc": {"count": 1},
                    "$push": {
                        "warnings": {
                            "reason": reason or "No reason",
                            "date": datetime.utcnow()
                        }
                    }
                },
                upsert=True
            )
            
            doc = await col.find_one({
                "group_id": group_id,
                "user_id": user_id
            })
            return doc.get("count", 0) if doc else 1
        except Exception as e:
            logger.error(f"Error adding warning: {e}")
            return 0
    
    async def get_warnings(self, group_id: int, user_id: int) -> int:
        """Get warning count"""
        try:
            col = await self.get_collection(COLLECTIONS["warnings"])
            doc = await col.find_one({
                "group_id": group_id,
                "user_id": user_id
            })
            return doc.get("count", 0) if doc else 0
        except Exception as e:
            logger.error(f"Error getting warnings: {e}")
            return 0
    
    async def reset_warnings(self, group_id: int, user_id: int) -> bool:
        """Reset warnings"""
        try:
            col = await self.get_collection(COLLECTIONS["warnings"])
            await col.delete_one({
                "group_id": group_id,
                "user_id": user_id
            })
            return True
        except Exception as e:
            logger.error(f"Error resetting warnings: {e}")
            return False
    
    # Welcome/Goodbye Operations
    async def set_welcome(self, group_id: int, text: str) -> bool:
        """Set welcome message"""
        try:
            col = await self.get_collection(COLLECTIONS["welcome"])
            await col.update_one(
                {"group_id": group_id},
                {"$set": {"text": text}},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Error setting welcome: {e}")
            return False
    
    async def get_welcome(self, group_id: int):
        """Get welcome message"""
        try:
            col = await self.get_collection(COLLECTIONS["welcome"])
            return await col.find_one({"group_id": group_id})
        except Exception as e:
            logger.error(f"Error getting welcome: {e}")
            return None
    
    async def set_goodbye(self, group_id: int, text: str) -> bool:
        """Set goodbye message"""
        try:
            col = await self.get_collection(COLLECTIONS["goodbye"])
            await col.update_one(
                {"group_id": group_id},
                {"$set": {"text": text}},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Error setting goodbye: {e}")
            return False
    
    async def get_goodbye(self, group_id: int):
        """Get goodbye message"""
        try:
            col = await self.get_collection(COLLECTIONS["goodbye"])
            return await col.find_one({"group_id": group_id})
        except Exception as e:
            logger.error(f"Error getting goodbye: {e}")
            return None
    
    # Reports Operations
    async def add_report(self, group_id: int, reporter_id: int, reported_id: int, message_id: int, reason: str = None) -> bool:
        """Add report"""
        try:
            col = await self.get_collection(COLLECTIONS["reports"])
            await col.insert_one({
                "group_id": group_id,
                "reporter_id": reporter_id,
                "reported_id": reported_id,
                "message_id": message_id,
                "reason": reason or "No reason specified",
                "created_at": datetime.utcnow()
            })
            return True
        except Exception as e:
            logger.error(f"Error adding report: {e}")
            return False
