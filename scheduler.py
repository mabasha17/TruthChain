"""
Simple scheduler for news updates.
"""

from datetime import datetime, timedelta
import config

class StreamlitScheduler:
    """Simple scheduler for Streamlit UI updates."""
    
    def __init__(self):
        self.last_update = None
        self.update_interval = config.UPDATE_INTERVAL_MINUTES * 60  # Convert to seconds
    
    def should_update(self) -> bool:
        """Check if it's time for an update."""
        if not self.last_update:
            return True
        
        time_since_update = (datetime.now() - self.last_update).total_seconds()
        return time_since_update >= self.update_interval
    
    def mark_updated(self):
        """Mark that an update has been performed."""
        self.last_update = datetime.now()
    
    def get_time_since_update(self) -> str:
        """Get human-readable time since last update."""
        if not self.last_update:
            return "Never"
        
        time_diff = datetime.now() - self.last_update
        minutes = int(time_diff.total_seconds() // 60)
        
        if minutes < 1:
            return "Just now"
        elif minutes == 1:
            return "1 minute ago"
        elif minutes < 60:
            return f"{minutes} minutes ago"
        else:
            hours = minutes // 60
            return f"{hours} hours ago"
    
    def get_next_update_time(self) -> str:
        """Get human-readable time until next update."""
        if not self.last_update:
            return "Unknown"
        
        time_since = (datetime.now() - self.last_update).total_seconds()
        time_until = self.update_interval - time_since
        
        if time_until <= 0:
            return "Due now"
        
        minutes_until = int(time_until // 60)
        if minutes_until < 1:
            return "Less than 1 minute"
        elif minutes_until == 1:
            return "1 minute"
        else:
            return f"{minutes_until} minutes"

def create_auto_refresh_scheduler():
    """Create a simple scheduler for Streamlit."""
    return StreamlitScheduler() 