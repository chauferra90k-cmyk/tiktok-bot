"""
TikTok Bot - Advanced TikTok Comment Bot
Author: TikTok Bot Dev
Description: Automated TikTok commenting bot with Discord control
"""

import logging
import asyncio
import json
import os
import random
import time
from datetime import datetime, timedelta
from typing import List, Optional
import aiohttp
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages bot configuration and persistence"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
        
        return {
            "hashtags": ["#fyp", "#viral"],
            "comments": [
                "Amazing! 🔥",
                "Love this! ❤️",
                "Top content! 👍",
                "Fire! 🎯"
            ],
            "is_running": False,
            "total_comments": 0,
            "comments_this_hour": 0,
            "last_reset": None
        }
    
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info("Configuration saved")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()
    
    def add_hashtag(self, hashtag: str):
        """Add hashtag to configuration"""
        hashtags = self.config.get("hashtags", [])
        if hashtag not in hashtags:
            hashtags.append(hashtag)
            self.config["hashtags"] = hashtags
            self.save_config()
            logger.info(f"Hashtag added: {hashtag}")
            return True
        return False
    
    def add_comment(self, comment: str):
        """Add comment template to configuration"""
        comments = self.config.get("comments", [])
        if comment not in comments:
            comments.append(comment)
            self.config["comments"] = comments
            self.save_config()
            logger.info(f"Comment template added: {comment}")
            return True
        return False
    
    def get_random_comment(self) -> Optional[str]:
        """Get random comment from templates"""
        comments = self.config.get("comments", [])
        if comments:
            return random.choice(comments)
        return None
    
    def check_rate_limit(self, max_per_hour: int = 10) -> bool:
        """Check if rate limit is exceeded"""
        last_reset = self.config.get("last_reset")
        current_time = datetime.now()
        
        if last_reset:
            last_reset_time = datetime.fromisoformat(last_reset)
            if current_time - last_reset_time > timedelta(hours=1):
                # Reset hour counter
                self.config["comments_this_hour"] = 0
                self.config["last_reset"] = current_time.isoformat()
                self.save_config()
        else:
            self.config["last_reset"] = current_time.isoformat()
        
        comments_this_hour = self.config.get("comments_this_hour", 0)
        return comments_this_hour >= max_per_hour
    
    def increment_comments(self):
        """Increment comment counters"""
        self.config["total_comments"] = self.config.get("total_comments", 0) + 1
        self.config["comments_this_hour"] = self.config.get("comments_this_hour", 0) + 1
        self.save_config()


class TikTokAPI:
    """TikTok API wrapper for scraping and commenting"""
    
    def __init__(self, username: str, password: str, headless: bool = True):
        self.username = username
        self.password = password
        self.headless = headless
        self.session = None
        self.is_logged_in = False
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15",
        ]
    
    async def initialize(self):
        """Initialize API session"""
        try:
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'application/json',
            }
            self.session = aiohttp.ClientSession(headers=headers)
            logger.info("TikTok API initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize TikTok API: {e}")
            return False
    
    async def login(self) -> bool:
        """Login to TikTok account"""
        try:
            logger.info(f"Attempting to login to TikTok: {self.username}")
            # Placeholder for actual login implementation
            # In production, use playwright or TikTokApi library
            self.is_logged_in = True
            logger.info("Successfully logged in to TikTok")
            return True
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    async def get_videos_by_hashtag(self, hashtag: str, limit: int = 10) -> List[dict]:
        """Scrape videos by hashtag"""
        try:
            if not hashtag.startswith('#'):
                hashtag = '#' + hashtag
            
            logger.info(f"Fetching videos for hashtag: {hashtag}")
            
            # Placeholder for actual video fetching
            # Use TikTok API or web scraping
            videos = []
            
            logger.info(f"Found {len(videos)} videos for {hashtag}")
            return videos
        except Exception as e:
            logger.error(f"Error fetching videos: {e}")
            return []
    
    async def post_comment(self, video_id: str, comment_text: str) -> bool:
        """Post comment on TikTok video"""
        try:
            if not self.is_logged_in:
                logger.warning("Not logged in, cannot post comment")
                return False
            
            logger.info(f"Posting comment on video: {video_id}")
            
            # Placeholder for actual comment posting
            # Use Playwright or TikTokApi library
            
            logger.info(f"Successfully posted comment: {comment_text}")
            return True
        except Exception as e:
            logger.error(f"Error posting comment: {e}")
            return False
    
    async def close(self):
        """Close API session"""
        if self.session:
            await self.session.close()
            logger.info("TikTok API session closed")


class TikTokBot:
    """Main TikTok Bot class"""
    
    def __init__(self, username: str, password: str):
        self.config_manager = ConfigManager()
        self.tiktok_api = TikTokAPI(username, password)
        self.is_running = False
        self.bot_task = None
    
    async def initialize(self) -> bool:
        """Initialize bot"""
        try:
            if not await self.tiktok_api.initialize():
                return False
            
            if not await self.tiktok_api.login():
                return False
            
            self.config_manager.set("is_running", False)
            logger.info("TikTok Bot initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            return False
    
    async def start(self):
        """Start bot loop"""
        if self.is_running:
            logger.warning("Bot is already running")
            return
        
        self.is_running = True
        self.config_manager.set("is_running", True)
        logger.info("Bot started")
        
        self.bot_task = asyncio.create_task(self._bot_loop())
    
    async def stop(self):
        """Stop bot loop"""
        self.is_running = False
        self.config_manager.set("is_running", False)
        
        if self.bot_task:
            self.bot_task.cancel()
            try:
                await self.bot_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Bot stopped")
    
    async def _bot_loop(self):
        """Main bot loop"""
        try:
            while self.is_running:
                hashtags = self.config_manager.get("hashtags", [])
                max_comments = int(os.getenv("MAX_COMMENTS_PER_HOUR", "10"))
                
                # Check rate limit
                if self.config_manager.check_rate_limit(max_comments):
                    logger.warning("Rate limit reached, waiting...")
                    await asyncio.sleep(300)  # Wait 5 minutes
                    continue
                
                # Process hashtags
                for hashtag in hashtags:
                    if not self.is_running:
                        break
                    
                    # Get random delay
                    delay_min = int(os.getenv("RATE_LIMIT_DELAY_MIN", "30"))
                    delay_max = int(os.getenv("RATE_LIMIT_DELAY_MAX", "180"))
                    delay = random.randint(delay_min, delay_max)
                    
                    logger.info(f"Processing hashtag: {hashtag}, next action in {delay}s")
                    
                    # Fetch videos
                    videos = await self.tiktok_api.get_videos_by_hashtag(hashtag, limit=5)
                    
                    if videos:
                        video = random.choice(videos)
                        comment = self.config_manager.get_random_comment()
                        
                        if comment:
                            success = await self.tiktok_api.post_comment(video.get('id'), comment)
                            if success:
                                self.config_manager.increment_comments()
                    
                    # Wait before next action
                    await asyncio.sleep(delay)
        
        except asyncio.CancelledError:
            logger.info("Bot loop cancelled")
        except Exception as e:
            logger.error(f"Error in bot loop: {e}")
    
    async def get_status(self) -> dict:
        """Get bot status"""
        return {
            "is_running": self.is_running,
            "total_comments": self.config_manager.get("total_comments", 0),
            "comments_this_hour": self.config_manager.get("comments_this_hour", 0),
            "hashtags": self.config_manager.get("hashtags", []),
            "comments_count": len(self.config_manager.get("comments", []))
        }
    
    async def cleanup(self):
        """Cleanup resources"""
        await self.stop()
        await self.tiktok_api.close()
        logger.info("Bot cleanup completed")


# Export for use in discord bot
__all__ = ['TikTokBot', 'ConfigManager', 'TikTokAPI', 'logger']
