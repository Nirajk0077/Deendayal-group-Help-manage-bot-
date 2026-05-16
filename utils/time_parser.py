"""
Time parsing and duration utilities
"""
import re
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class TimeParser:
    """Parse time strings to seconds"""
    
    TIME_UNITS = {
        's': 1,
        'sec': 1,
        'second': 1,
        'seconds': 1,
        'm': 60,
        'min': 60,
        'minute': 60,
        'minutes': 60,
        'h': 3600,
        'hour': 3600,
        'hours': 3600,
        'd': 86400,
        'day': 86400,
        'days': 86400,
        'w': 604800,
        'week': 604800,
        'weeks': 604800,
        'mon': 2592000,
        'month': 2592000,
        'months': 2592000,
        'y': 31536000,
        'year': 31536000,
        'years': 31536000,
    }
    
    @staticmethod
    def parse(time_str: str) -> int:
        """
        Parse time string to seconds
        Examples: "5m", "1h", "2d", "1w"
        """
        if not time_str:
            return 0
        
        try:
            time_str = time_str.lower().strip()
            
            # Try regex pattern
            match = re.match(r'(\d+)\s*([a-z]+)', time_str)
            if not match:
                return 0
            
            amount = int(match.group(1))
            unit = match.group(2)
            
            seconds_per_unit = TimeParser.TIME_UNITS.get(unit, 0)
            if seconds_per_unit == 0:
                return 0
            
            return amount * seconds_per_unit
        except Exception as e:
            logger.error(f"Error parsing time: {e}")
            return 0
    
    @staticmethod
    def format_seconds(seconds: int) -> str:
        """Format seconds to human readable"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}m"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{hours}h"
        elif seconds < 604800:
            days = seconds // 86400
            return f"{days}d"
        elif seconds < 2592000:
            weeks = seconds // 604800
            return f"{weeks}w"
        elif seconds < 31536000:
            months = seconds // 2592000
            return f"{months}mon"
        else:
            years = seconds // 31536000
            return f"{years}y"

class DateUtils:
    """Date and time utilities"""
    
    @staticmethod
    def get_readable_date(dt: datetime = None) -> str:
        """Get readable date format"""
        if dt is None:
            dt = datetime.utcnow()
        
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    @staticmethod
    def get_time_remaining(seconds: int) -> str:
        """Get human readable time remaining"""
        now = datetime.utcnow()
        future = now + timedelta(seconds=seconds)
        return future.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    @staticmethod
    def is_past(dt: datetime) -> bool:
        """Check if datetime is in the past"""
        return dt < datetime.utcnow()
