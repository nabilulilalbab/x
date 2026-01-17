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
    
    def __init__(self, cookies_file: str = "cookies.json", account_folder: Optional[str] = None):
        """
        Initialize BotAutomation.
        
        Args:
            cookies_file: Path to cookies.json (used if account_folder not provided)
            account_folder: Account folder path (e.g., "accounts/account1_GrnStore4347")
                          If provided, all paths will be relative to this folder.
                          If None, uses default paths (backward compatible).
        """
        # Store account folder for multi-account support
        self.account_folder = account_folder
        
        # Determine paths based on account_folder
        if account_folder:
            # Multi-account mode: Use paths relative to account folder
            self.config_path = f"{account_folder}/config"
            self.data_path = f"{account_folder}/data"
            self.media_path = f"{account_folder}/media"
            self.cookies_file = f"{account_folder}/cookies.json"
            
            logger.info(f"🔀 Multi-account mode: {account_folder}")
        else:
            # Single-account mode: Use default paths (backward compatible)
            self.config_path = "config"
            self.data_path = "data"
            self.media_path = "media"
            self.cookies_file = cookies_file
            
            logger.info("📱 Single-account mode (default paths)")
        
        # Initialize components with appropriate paths
        self.config = ConfigLoader(config_dir=self.config_path)
        self.db = Database(db_path=f"{self.data_path}/metrics.db")
        
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
        self.twitter = TwitterClient(self.cookies_file, self.config, self.db)
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
                # Resolve media path (relative to account folder if multi-account)
                if self.account_folder:
                    # Multi-account mode: prepend account folder
                    full_media_path = f"{self.account_folder}/{media_path}"
                else:
                    # Single-account mode: use as-is
                    full_media_path = media_path
                
                # Check if file exists
                from pathlib import Path
                if Path(full_media_path).exists():
                    logger.info(f"📸 Using media from template: {full_media_path}")
                    media_id = await self.twitter.upload_media_file(full_media_path)
                    if media_id:
                        media_ids = [media_id]
                else:
                    logger.warning(f"⚠️  Media file not found: {full_media_path}")
            
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
                # Resolve media path (relative to account folder if multi-account)
                if self.account_folder:
                    # Multi-account mode: prepend account folder
                    full_media_path = f"{self.account_folder}/{media_path}"
                else:
                    # Single-account mode: use as-is
                    full_media_path = media_path
                
                # Check if file exists
                from pathlib import Path
                if Path(full_media_path).exists():
                    logger.info(f"📸 Using media from template: {full_media_path}")
                    media_id = await self.twitter.upload_media_file(full_media_path)
                    if media_id:
                        media_ids = [media_id]
                else:
                    logger.warning(f"⚠️  Media file not found: {full_media_path}")
            
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
    
    def _is_suitable_for_reply(self, tweet) -> bool:
        """Filter tweets that are suitable for replying"""
        try:
            # Check if we already replied to this tweet
            if self.db.has_replied_to_tweet(tweet.id):
                logger.debug(f"⏭️  Skip: Already replied to tweet {tweet.id}")
                return False
            
            # Check if we already replied to this author today
            author = tweet.user.screen_name if hasattr(tweet.user, 'screen_name') else tweet.user.username
            if self.db.has_replied_to_author_today(f"@{author}"):
                logger.debug(f"⏭️  Skip: Already replied to @{author} today")
                return False
            
            # Skip if tweet has too many replies (viral tweet, risky)
            if hasattr(tweet, 'reply_count') and tweet.reply_count and tweet.reply_count > 50:
                logger.debug(f"⏭️  Skip: Too many replies ({tweet.reply_count})")
                return False
            
            # Skip if tweet is too old (>24 hours)
            from datetime import datetime, timezone, timedelta
            if hasattr(tweet, 'created_at'):
                if isinstance(tweet.created_at, datetime):
                    tweet_age = datetime.now(timezone.utc) - tweet.created_at
                else:
                    # Try to parse if it's a string
                    try:
                        from dateutil import parser
                        created = parser.parse(tweet.created_at)
                        tweet_age = datetime.now(timezone.utc) - created
                    except:
                        tweet_age = timedelta(hours=0)  # Assume recent if can't parse
                
                if tweet_age.total_seconds() > 86400:  # 24 hours
                    logger.debug(f"⏭️  Skip: Tweet too old ({tweet_age.total_seconds()/3600:.1f}h)")
                    return False
            
            # Get tweet text
            text = tweet.text.lower() if hasattr(tweet, 'text') else ""
            
            # Skip if it's a brand/competitor tweet (has promotional keywords)
            skip_keywords = ['promo', 'diskon', 'sale', 'jualan', 'order', 'ready stock', 'dm untuk', 'wa:', 'whatsapp']
            if any(keyword in text for keyword in skip_keywords):
                logger.debug(f"⏭️  Skip: Promotional tweet")
                return False
            
            # Prioritize questions and keluhan (complaints)
            priority_indicators = [
                '?',  # Questions
                'gimana', 'bagaimana', 'kenapa', 'kok', 'dong',  # Question words
                'habis', 'lemot', 'lelet', 'jelek', 'buruk', 'parah', 'lambat',  # Complaints
                'butuh', 'cari', 'perlu', 'mau', 'pengen',  # Looking for solution
                'rekomendasi', 'saran', 'recommend', 'suggest'  # Asking for advice
            ]
            
            has_priority = any(indicator in text for indicator in priority_indicators)
            
            if not has_priority:
                logger.debug(f"⏭️  Skip: Not a question or complaint")
                return False
            
            logger.debug(f"✅ Suitable for reply: {text[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error checking tweet suitability: {e}")
            return False
    
    async def search_and_reply_tweets(self, keyword: str, max_replies: int = 3) -> int:
        """Search tweets and reply with helpful content (with safety filters)"""
        try:
            logger.info(f"🔍 Searching tweets for: {keyword} (max replies: {max_replies})")
            
            # Check daily limit
            replies_today = self.db.get_reply_count_today()
            if replies_today >= 9:  # Daily limit
                self.logger.warning(f"⚠️  Daily reply limit reached ({replies_today}/9)")
                return 0
            
            # Adjust max_replies based on remaining daily quota
            remaining = 9 - replies_today
            max_replies = min(max_replies, remaining)
            
            # Search tweets
            tweets = await self.twitter.search_tweets(keyword, count=20)  # Get more to filter
            
            if not tweets:
                self.logger.info("No tweets found")
                return 0
            
            self.logger.info(f"Found {len(tweets)} tweets, filtering...")
            
            # Filter suitable tweets
            suitable_tweets = [tweet for tweet in tweets if self._is_suitable_for_reply(tweet)]
            
            self.logger.info(f"✅ {len(suitable_tweets)} tweets suitable for reply")
            
            if not suitable_tweets:
                return 0
            
            # Limit to max_replies
            suitable_tweets = suitable_tweets[:max_replies]
            
            replied_count = 0
            for tweet in suitable_tweets:
                try:
                    # Generate reply using templates
                    reply_text = await self._generate_reply()
                    
                    # Post reply
                    self.logger.info(f"💬 Replying to @{tweet.user.username}: {reply_text[:50]}...")
                    reply_id = await self.twitter.reply_to_tweet(tweet.id, reply_text)
                    
                    if reply_id:
                        # Track in database
                        author = f"@{tweet.user.username if hasattr(tweet.user, 'username') else tweet.user.screen_name}"
                        self.db.add_replied_tweet(
                            tweet_id=tweet.id,
                            tweet_author=author,
                            tweet_text=tweet.text[:200] if hasattr(tweet, 'text') else "",
                            our_reply_id=reply_id,
                            our_reply_text=reply_text
                        )
                        
                        replied_count += 1
                        self.logger.info(f"✅ Reply posted successfully!")
                        
                        # Random delay between replies (10-15 minutes)
                        import random
                        delay = random.randint(600, 900)  # 10-15 minutes
                        self.logger.info(f"⏳ Waiting {delay/60:.1f} minutes before next reply...")
                        await asyncio.sleep(delay)
                    
                except Exception as e:
                    self.logger.error(f"Error replying to tweet: {e}")
                    continue
            
            return replied_count
            
        except Exception as e:
            self.logger.error(f"Error in search_and_reply_tweets: {e}")
            return 0
    
    async def _generate_reply(self) -> str:
        """Generate a reply using templates"""
        import random
        
        # Get reply templates
        reply_templates = self.config.get('templates', {}).get('reply_templates', {})
        
        if not reply_templates:
            # Fallback
            return "Coba pakai mode hemat data di HP, lumayan hemat! Btw kalau butuh kuota murah, DM ya 😊"
        
        # Random category
        category = random.choice(list(reply_templates.keys()))
        templates = reply_templates[category]
        
        # Random template
        template = random.choice(templates)
        
        # Replace variables
        wa_number = self.config.get('business', {}).get('wa_number', 'DM')
        reply_text = template.replace('{wa_number}', wa_number)
        
        # AI enhancement (if available)
        if hasattr(self, 'ai_client') and self.ai_client:
            try:
                enhanced = await self.ai_client.improve_tweet(reply_text)
                if enhanced and len(enhanced) <= 280:
                    reply_text = enhanced
            except:
                pass  # Use original if AI fails
        
        return reply_text
    
    async def search_and_like_tweets(self, keyword: str, count: int = 5):
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
            'rate_limits': {} if self.twitter.client else {},
            'daily_stats': self.db.get_daily_activity(),
            'dashboard_stats': self.db.get_dashboard_stats()
        }
