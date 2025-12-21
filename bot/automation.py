"""
Automation Engine
Main bot automation logic
"""

import asyncio
import logging
import random
from datetime import datetime
from typing import Dict, Optional

from .config_loader import ConfigLoader
from .database import Database
from .twitter_client import TwitterClient
from .ai_client import AIClient
from .content_generator import ContentGenerator

logger = logging.getLogger(__name__)


class BotAutomation:
    """Main bot automation engine"""
    
    def __init__(self, cookies_file: str = "cookies.json"):
        self.config = ConfigLoader()
        self.db = Database()
        
        # Get settings
        settings = self.config.get_settings()
        
        # Setup AI client
        ai_config = settings['ai']
        self.ai_client = None
        if ai_config['enabled']:
            self.ai_client = AIClient(
                api_url=ai_config['api_url'],
                timeout=ai_config['timeout']
            )
        
        # Setup components
        self.twitter = TwitterClient(cookies_file, self.config, self.db)
        self.content_gen = ContentGenerator(self.config, self.ai_client)
        
        self.is_running = False
    
    async def initialize(self) -> bool:
        """Initialize bot"""
        logger.info("🚀 Initializing bot...")
        
        success = await self.twitter.setup()
        
        if success:
            logger.info("✅ Bot initialized successfully!")
            self.db.log_activity('initialize', 'Bot started', True)
        else:
            logger.error("❌ Bot initialization failed!")
            self.db.log_activity('initialize', None, False, 'Setup failed')
        
        return success
    
    async def run_morning_slot(self):
        """Morning automation slot (08:00)"""
        logger.info("\n" + "="*60)
        logger.info("🌅 MORNING SLOT STARTING")
        logger.info("="*60)
        
        try:
            # 1. Post promo tweet
            logger.info("\n📝 Generating morning promo tweet...")
            tweet_text, media_path = await self.content_gen.generate_promo_tweet(use_ai=True)
            
            # Upload media if specified in template
            media_ids = None
            if media_path:
                logger.info(f"📸 Using media from template: {media_path}")
                media_id = await self.twitter.upload_media_file(media_path)
                if media_id:
                    media_ids = [media_id]
            
            logger.info(f"Tweet: {tweet_text}")
            tweet_id = await self.twitter.post_tweet(tweet_text, media_ids=media_ids, tweet_type='promo')
            
            if not tweet_id:
                logger.warning("Failed to post morning tweet")
            
            # 2. Search & engage
            logger.info("\n🔍 Searching and engaging...")
            keywords = self.content_gen.get_search_keywords('high')
            
            if keywords:
                keyword = random.choice(keywords)
                liked_count = await self.twitter.search_and_like(keyword, max_like=5)
                logger.info(f"Liked {liked_count} tweets for: {keyword}")
            
            # 3. Follow target users
            logger.info("\n👥 Following target users...")
            follow_keywords = ["mahasiswa kuota", "wfh internet", "butuh kuota"]
            keyword = random.choice(follow_keywords)
            followed_count = await self.twitter.search_and_follow(keyword, max_follow=5)
            logger.info(f"Followed {followed_count} users")
            
            # 4. Update metrics
            await self.twitter.update_follower_count()
            
            logger.info("\n✅ Morning slot completed!")
            self.db.log_activity('morning_slot', 'Completed successfully', True)
            
        except Exception as e:
            logger.error(f"❌ Morning slot error: {e}")
            self.db.log_activity('morning_slot', None, False, str(e))
    
    async def run_afternoon_slot(self):
        """Afternoon automation slot (13:00)"""
        logger.info("\n" + "="*60)
        logger.info("🌤️  AFTERNOON SLOT STARTING")
        logger.info("="*60)
        
        try:
            # 1. Post value content
            logger.info("\n📝 Generating value content tweet...")
            tweet_text = await self.content_gen.generate_value_tweet(use_ai=True)
            
            logger.info(f"Tweet: {tweet_text}")
            tweet_id = await self.twitter.post_tweet(tweet_text, tweet_type='value')
            
            if not tweet_id:
                logger.warning("Failed to post afternoon tweet")
            
            # 2. Search & engage (medium intent)
            logger.info("\n🔍 Searching and engaging...")
            keywords = self.content_gen.get_search_keywords('medium')
            
            if keywords:
                keyword = random.choice(keywords)
                liked_count = await self.twitter.search_and_like(keyword, max_like=5)
                logger.info(f"Liked {liked_count} tweets for: {keyword}")
            
            # 3. Update metrics
            await self.twitter.update_follower_count()
            
            logger.info("\n✅ Afternoon slot completed!")
            self.db.log_activity('afternoon_slot', 'Completed successfully', True)
            
        except Exception as e:
            logger.error(f"❌ Afternoon slot error: {e}")
            self.db.log_activity('afternoon_slot', None, False, str(e))
    
    async def run_evening_slot(self):
        """Evening automation slot (20:00)"""
        logger.info("\n" + "="*60)
        logger.info("🌙 EVENING SLOT STARTING")
        logger.info("="*60)
        
        try:
            # 1. Post promo tweet
            logger.info("\n📝 Generating evening promo tweet...")
            tweet_text, media_path = await self.content_gen.generate_promo_tweet(use_ai=True)
            
            # Upload media if specified in template
            media_ids = None
            if media_path:
                logger.info(f"📸 Using media from template: {media_path}")
                media_id = await self.twitter.upload_media_file(media_path)
                if media_id:
                    media_ids = [media_id]
            
            logger.info(f"Tweet: {tweet_text}")
            tweet_id = await self.twitter.post_tweet(tweet_text, media_ids=media_ids, tweet_type='promo')
            
            if not tweet_id:
                logger.warning("Failed to post evening tweet")
            
            # 2. Engage with followers (like their tweets)
            logger.info("\n💙 Engaging with followers...")
            # Note: This would require getting follower list and their tweets
            # For now, we'll just search and engage
            
            keywords = self.content_gen.get_search_keywords('high')
            if keywords:
                keyword = random.choice(keywords)
                liked_count = await self.twitter.search_and_like(keyword, max_like=3)
                logger.info(f"Liked {liked_count} tweets")
            
            # 3. Follow more users
            logger.info("\n👥 Following target users...")
            follow_keywords = ["gamer kuota", "streaming internet"]
            keyword = random.choice(follow_keywords)
            followed_count = await self.twitter.search_and_follow(keyword, max_follow=5)
            logger.info(f"Followed {followed_count} users")
            
            # 4. Daily summary
            logger.info("\n📊 Generating daily summary...")
            daily_stats = self.db.get_daily_activity()
            
            logger.info("\n" + "="*60)
            logger.info("📊 DAILY SUMMARY")
            logger.info("="*60)
            logger.info(f"Tweets posted: {daily_stats['tweets_posted']}")
            logger.info(f"Likes given: {daily_stats['likes_given']}")
            logger.info(f"Replies made: {daily_stats['replies_made']}")
            logger.info(f"Follows made: {daily_stats['follows_made']}")
            logger.info(f"Retweets made: {daily_stats['retweets_made']}")
            logger.info("="*60)
            
            # 5. Update metrics
            await self.twitter.update_follower_count()
            
            logger.info("\n✅ Evening slot completed!")
            self.db.log_activity('evening_slot', 'Completed successfully', True)
            
        except Exception as e:
            logger.error(f"❌ Evening slot error: {e}")
            self.db.log_activity('evening_slot', None, False, str(e))
    
    async def run_once(self, slot: str = 'morning'):
        """Run one slot manually"""
        await self.initialize()
        
        if slot == 'morning':
            await self.run_morning_slot()
        elif slot == 'afternoon':
            await self.run_afternoon_slot()
        elif slot == 'evening':
            await self.run_evening_slot()
        else:
            logger.error(f"Unknown slot: {slot}")
        
        await self.cleanup()
    
    async def run_scheduled(self):
        """Run bot with schedule"""
        await self.initialize()
        
        settings = self.config.get_settings()
        schedule_config = settings['schedule']
        
        if not schedule_config['enabled']:
            logger.warning("Schedule is disabled in config!")
            return
        
        logger.info("🕐 Starting scheduled bot...")
        logger.info(f"Morning slot: {schedule_config['morning']['time']}")
        logger.info(f"Afternoon slot: {schedule_config['afternoon']['time']}")
        logger.info(f"Evening slot: {schedule_config['evening']['time']}")
        
        self.is_running = True
        
        while self.is_running:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            
            # Check if it's time for a slot
            if (schedule_config['morning']['enabled'] and 
                current_time == schedule_config['morning']['time']):
                await self.run_morning_slot()
                await asyncio.sleep(60)  # Wait 1 minute to avoid duplicate
            
            elif (schedule_config['afternoon']['enabled'] and 
                  current_time == schedule_config['afternoon']['time']):
                await self.run_afternoon_slot()
                await asyncio.sleep(60)
            
            elif (schedule_config['evening']['enabled'] and 
                  current_time == schedule_config['evening']['time']):
                await self.run_evening_slot()
                await asyncio.sleep(60)
            
            # Check every 30 seconds
            await asyncio.sleep(30)
    
    def stop(self):
        """Stop bot"""
        logger.info("🛑 Stopping bot...")
        self.is_running = False
    
    async def cleanup(self):
        """Cleanup resources"""
        logger.info("🧹 Cleaning up...")
        
        if self.twitter:
            await self.twitter.cleanup()
        
        if self.ai_client:
            await self.ai_client.close()
        
        logger.info("✅ Cleanup complete!")
    
    def get_status(self) -> Dict:
        """Get current bot status"""
        return {
            'is_running': self.is_running,
            'rate_limits': asyncio.run(self.twitter.get_rate_limit_status()) if self.twitter.client else {},
            'daily_stats': self.db.get_daily_activity(),
            'dashboard_stats': self.db.get_dashboard_stats()
        }
