"""
Helper utilities
"""
import re
import logging
from typing import List, Tuple, Optional
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)

class TextFormatter:
    """Text formatting utilities"""
    
    @staticmethod
    def escape_html(text: str) -> str:
        """Escape HTML special characters"""
        if not text:
            return text
        replacements = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        }
        for char, escaped in replacements.items():
            text = text.replace(char, escaped)
        return text
    
    @staticmethod
    def format_with_variables(text: str, variables: dict) -> str:
        """Format text with variables"""
        if not variables or not text:
            return text
        
        try:
            for key, value in variables.items():
                text = text.replace(f"{{{key}}}", str(value))
            return text
        except Exception as e:
            logger.error(f"Error formatting text: {e}")
            return text
    
    @staticmethod
    def truncate(text: str, length: int = 100) -> str:
        """Truncate text to length"""
        if len(text) <= length:
            return text
        return text[:length] + "..."

class ButtonBuilder:
    """Build inline keyboards"""
    
    @staticmethod
    def build_keyboard(buttons: list) -> Optional[InlineKeyboardMarkup]:
        """Build keyboard from buttons list"""
        if not buttons:
            return None
        
        try:
            keyboard = []
            current_row = []
            
            for btn_data in buttons:
                try:
                    btn_type = btn_data.get("type")
                    text = btn_data.get("text")
                    
                    if btn_type == "url":
                        btn = InlineKeyboardButton(
                            text=text,
                            url=btn_data.get("url")
                        )
                    elif btn_type == "callback":
                        btn = InlineKeyboardButton(
                            text=text,
                            callback_data=btn_data.get("callback_data")
                        )
                    else:
                        continue
                    
                    current_row.append(btn)
                    
                    if len(current_row) >= btn_data.get("row", 1):
                        keyboard.append(current_row)
                        current_row = []
                except Exception as e:
                    logger.error(f"Error building button: {e}")
                    continue
            
            if current_row:
                keyboard.append(current_row)
            
            return InlineKeyboardMarkup(keyboard) if keyboard else None
        except Exception as e:
            logger.error(f"Error building keyboard: {e}")
            return None

class LinkDetector:
    """Detect links in text"""
    
    LINK_PATTERNS = [
        r'https?://[^\s]+',
        r'www\.[^\s]+',
        r't\.me/[^\s]+',
        r'tg://[^\s]+',
    ]
    
    @staticmethod
    def has_link(text: str) -> bool:
        """Check if text contains links"""
        if not text:
            return False
        
        for pattern in LinkDetector.LINK_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    @staticmethod
    def extract_links(text: str) -> List[str]:
        """Extract all links from text"""
        links = []
        for pattern in LinkDetector.LINK_PATTERNS:
            links.extend(re.findall(pattern, text, re.IGNORECASE))
        return list(set(links))

class MentionDetector:
    """Detect mentions in text"""
    
    @staticmethod
    def has_mention(text: str) -> bool:
        """Check if text contains mentions"""
        if not text:
            return False
        return bool(re.search(r'@[a-zA-Z0-9_]{5,32}', text))
    
    @staticmethod
    def extract_mentions(text: str) -> List[str]:
        """Extract all mentions"""
        return re.findall(r'@[a-zA-Z0-9_]+', text)

class BadWordFilter:
    """Bad word filtering with word boundaries"""
    
    @staticmethod
    def contains_badword(text: str, badwords: List[str]) -> Tuple[bool, Optional[str]]:
        """Check if text contains bad words"""
        if not text or not badwords:
            return False, None
        
        text_lower = text.lower()
        
        for word in badwords:
            pattern = r'\b' + re.escape(word.lower()) + r'\b'
            if re.search(pattern, text_lower):
                return True, word
        
        return False, None

class TextCleaner:
    """Clean text utilities"""
    
    @staticmethod
    def remove_links(text: str) -> str:
        """Remove links from text"""
        if not text:
            return text
        
        for pattern in LinkDetector.LINK_PATTERNS:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    @staticmethod
    def remove_mentions(text: str) -> str:
        """Remove mentions from text"""
        if not text:
            return text
        return re.sub(r'@[a-zA-Z0-9_]+', '', text).strip()
    
    @staticmethod
    def remove_markdown(text: str) -> str:
        """Remove markdown formatting"""
        if not text:
            return text
        
        # Remove bold, italic, code, etc.
        text = re.sub(r'[*_`~\[\]()]', '', text)
        return text.strip()
