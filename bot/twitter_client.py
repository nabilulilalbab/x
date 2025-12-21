"""
Twitter Client Wrapper
Wrapper around Twikit with safety features
"""

import asyncio
import random
import logging
from typing import Optional, List, Dict
from datetime import datetime
import httpx
from twikit import Client

from .database import Database
from .config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class SafetyLimiter:
    """Rate limiter for bot safety"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.counters = {
            'tweets': {'hour': 0, 'day': 0, 'last_reset_hour': datetime.now().hour},
            'follows': {'hour': 0, 'day': 0, 'last_reset_hour': datetime.now().hour},
            'likes': {'hour': 0, 'day': 0, 'last_reset_hour': datetime.now().hour},
            'replies': {'hour': 0, 'day': 0, 'last_reset_hour': datetime.now().hour},
        }
    
    def _reset_if_needed(self, action_type: str):
        """Reset counters if hour changed"""
        current_hour = datetime.now().hour
        counter = self.counters[action_type]
        
        if current_hour != counter['last_reset_hour']:
            counter['hour'] = 0
            counter['last_reset_hour'] = current_hour
        
        # Reset daily counter at midnight
        if current_hour == 0 and counter['day'] > 0:
            counter['day'] = 0
    
    def can_perform(self, action_type: str) -> bool:
        """Check if action can be performed"""
        self._reset_if_needed(action_type)
        
        counter = self.counters[action_type]
        limits = self.config['rate_limits']
        
        hourly_limit = limits.get(f'{action_type}_per_hour', 999)
        daily_limit = limits.get(f'{action_type}_per_day', 999)
        
        if counter['hour'] >= hourly_limit:
            logger.warning(f"Hourly limit reached for {action_type}")
            return False
        
        if counter['day'] >= daily_limit:
            logger.warning(f"Daily limit reached for {action_type}")
            return False
        
        return True
    
    def record_action(self, action_type: str):
        """Record that action was performed"""
        self._reset_if_needed(action_type)
        counter = self.counters[action_type]
        counter['hour'] += 1
        counter['day'] += 1
    
    def get_status(self, action_type: str) -> Dict:
        """Get current status for action type"""
        self._reset_if_needed(action_type)
        counter = self.counters[action_type]
        limits = self.config['rate_limits']
        
        return {
            'hour_count': counter['hour'],
            'hour_limit': limits.get(f'{action_type}_per_hour', 999),
            'day_count': counter['day'],
            'day_limit': limits.get(f'{action_type}_per_day', 999),
            'can_perform': self.can_perform(action_type)
        }


class TwitterClient:
    """Safe Twitter client wrapper"""
    
    def __init__(self, cookies_file: str, config: ConfigLoader, database: Database):
        self.cookies_file = cookies_file
        self.config = config
        self.db = database
        
        # Get safety config
        settings = config.get_settings()
        self.safety_config = settings['safety']
        self.limiter = SafetyLimiter(self.safety_config)
        
        # Setup client
        self.client = None
        self.http_client = None
        self.me = None
    
    async def setup(self) -> bool:
        """Initialize Twitter client"""
        try:
            # Setup timeout
            timeout_config = httpx.Timeout(
                connect=30.0, read=300.0, write=300.0, pool=30.0
            )
            
            self.http_client = httpx.AsyncClient(
                timeout=timeout_config,
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
                follow_redirects=True
            )
            
            # Setup client
            user_agent = (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
            
            self.client = Client(language="en-US", user_agent=user_agent)
            self.client.http = self.http_client
            
            # Load cookies
            self.client.load_cookies(self.cookies_file)
            
            # Verify login
            self.me = await self.client.user()
            
            logger.info(f"✅ Logged in as @{self.me.screen_name}")
            logger.info(f"   Followers: {self.me.followers_count}")
            logger.info(f"   Following: {self.me.following_count}")
            
            # Record follower count
            self.db.record_follower_count(
                self.me.followers_count,
                self.me.following_count
            )
            
            self.db.log_activity('login', f'Logged in as @{self.me.screen_name}', True)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup Twitter client: {e}")
            self.db.log_activity('login', None, False, str(e))
            return False
    
    async def random_delay(self, delay_type: str = 'default'):
        """Random delay for natural behavior"""
        delays = self.safety_config['delays']
        
        if delay_type in delays:
            min_delay, max_delay = delays[delay_type]
        else:
            min_delay = delays['min_delay']
            max_delay = delays['max_delay']
        
        delay = random.uniform(min_delay, max_delay)
        logger.debug(f"Waiting {delay:.1f}s...")
        await asyncio.sleep(delay)
    
    async def post_tweet(self, text: str, media_ids: Optional[List[str]] = None,
                        tweet_type: str = 'promo') -> Optional[str]:
        """
        Post tweet with safety checks
        
        Returns:
            Tweet ID if successful, None otherwise
        """
        if not self.limiter.can_perform('tweets'):
            logger.warning("Tweet rate limit reached!")
            return None
        
        try:
            tweet = await self.client.create_tweet(
                text=text,
                media_ids=media_ids
            )
            
            tweet_id = tweet.id
            
            # Record metrics
            self.limiter.record_action('tweets')
            self.db.increment_activity('tweet')
            self.db.add_tweet(tweet_id, text, tweet_type)
            
            media_note = f" (with {len(media_ids)} media)" if media_ids else ""
            self.db.log_activity('post_tweet', f'Posted{media_note}: {text[:50]}...', True)
            
            logger.info(f"✅ Tweet posted: {tweet_id}{media_note}")
            
            # Delay after tweet
            await self.random_delay('after_tweet')
            
            return tweet_id
            
        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            self.db.log_activity('post_tweet', text[:50], False, str(e))
            return None
    
    async def upload_media_file(self, file_path: str) -> Optional[str]:
        """
        Upload media file and return media_id
        
        Args:
            file_path: Path to media file
        
        Returns:
            Media ID if successful, None otherwise
        """
        try:
            # Detect media type
            if file_path.lower().endswith(('.mp4', '.mov')):
                media_type = 'video/mp4'
            elif file_path.lower().endswith(('.jpg', '.jpeg')):
                media_type = 'image/jpeg'
            elif file_path.lower().endswith('.png'):
                media_type = 'image/png'
            else:
                logger.error(f"Unsupported media type: {file_path}")
                return None
            
            logger.info(f"📤 Uploading media: {file_path}")
            
            media_id = await self.client.upload_media(
                file_path,
                media_type=media_type,
                wait_for_completion=True
            )
            
            logger.info(f"✅ Media uploaded: {media_id}")
            
            return media_id
            
        except Exception as e:
            logger.error(f"Failed to upload media: {e}")
            return None
    
    async def search_and_like(self, keyword: str, max_like: int = 5) -> int:
        """
        Search keyword and like relevant tweets
        
        Returns:
            Number of tweets liked
        """
        try:
            tweets = await self.client.search_tweet(
                keyword,
                product='Latest',
                count=20
            )
            
            liked_count = 0
            found_count = len(tweets) if tweets else 0
            
            if not tweets:
                logger.info(f"No tweets found for: {keyword}")
                return 0
            
            for tweet in tweets:
                if liked_count >= max_like:
                    break
                
                if not self.limiter.can_perform('likes'):
                    logger.warning("Like rate limit reached!")
                    break
                
                # Skip own tweets
                if tweet.user.id == self.me.id:
                    continue
                
                # Skip already liked
                if tweet.favorited:
                    continue
                
                try:
                    await self.client.favorite_tweet(tweet.id)
                    
                    self.limiter.record_action('likes')
                    self.db.increment_activity('like')
                    
                    liked_count += 1
                    logger.info(f"❤️  Liked tweet from @{tweet.user.screen_name}")
                    
                    await self.random_delay()
                    
                except Exception as e:
                    logger.error(f"Failed to like tweet: {e}")
            
            # Record keyword performance
            self.db.record_keyword_activity(keyword, found_count, liked_count)
            self.db.log_activity('search_like', f'{keyword}: {liked_count}/{found_count}', True)
            
            return liked_count
            
        except Exception as e:
            logger.error(f"Search and like error: {e}")
            self.db.log_activity('search_like', keyword, False, str(e))
            return 0
    
    async def follow_user(self, user_id: str) -> bool:
        """Follow user with safety checks"""
        if not self.limiter.can_perform('follows'):
            logger.warning("Follow rate limit reached!")
            return False
        
        try:
            await self.client.follow_user(user_id)
            
            self.limiter.record_action('follows')
            self.db.increment_activity('follow')
            self.db.log_activity('follow', f'Followed user {user_id}', True)
            
            logger.info(f"✅ Followed user: {user_id}")
            
            await self.random_delay('after_follow')
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to follow user: {e}")
            self.db.log_activity('follow', user_id, False, str(e))
            return False
    
    async def search_and_follow(self, keyword: str, max_follow: int = 5) -> int:
        """Search users by keyword and follow"""
        try:
            users = await self.client.search_user(keyword, count=20)
            
            followed_count = 0
            
            if not users:
                logger.info(f"No users found for: {keyword}")
                return 0
            
            for user in users:
                if followed_count >= max_follow:
                    break
                
                # Skip self
                if user.id == self.me.id:
                    continue
                
                # Skip if already following (check if attribute exists)
                if hasattr(user, 'following') and user.following:
                    continue
                
                # Filter by followers (100-5000 sweet spot)
                if user.followers_count < 100 or user.followers_count > 5000:
                    continue
                
                success = await self.follow_user(user.id)
                if success:
                    followed_count += 1
            
            logger.info(f"Followed {followed_count} users for keyword: {keyword}")
            return followed_count
            
        except Exception as e:
            logger.error(f"Search and follow error: {e}")
            return 0
    
    async def get_rate_limit_status(self) -> Dict:
        """Get current rate limit status"""
        return {
            'tweets': self.limiter.get_status('tweets'),
            'follows': self.limiter.get_status('follows'),
            'likes': self.limiter.get_status('likes'),
            'replies': self.limiter.get_status('replies'),
        }
    
    async def update_follower_count(self):
        """Update follower count in database"""
        try:
            # Refresh user data
            self.me = await self.client.user()
            
            self.db.record_follower_count(
                self.me.followers_count,
                self.me.friends_count
            )
            
            logger.info(f"Updated follower count: {self.me.followers_count}")
            
        except Exception as e:
            logger.error(f"Failed to update follower count: {e}")
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.http_client:
            await self.http_client.aclose()
