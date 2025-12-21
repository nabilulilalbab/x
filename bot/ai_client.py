"""
AI Client for content improvement
Using ElrayyXml Copilot API
"""

import httpx
import asyncio
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class AIClient:
    """AI client for improving tweet content"""
    
    def __init__(self, api_url: str, timeout: int = 10):
        self.api_url = api_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def improve_tweet(self, tweet: str, prompt_template: str) -> Optional[str]:
        """
        Improve tweet using AI
        
        Args:
            tweet: Original tweet text
            prompt_template: Prompt template with {tweet} placeholder
        
        Returns:
            Improved tweet or original if failed
        """
        try:
            # Format prompt
            prompt = prompt_template.format(tweet=tweet)
            
            # Call API
            response = await self.client.get(
                self.api_url,
                params={"text": prompt}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') and 'result' in data:
                    improved = data['result'].strip()
                    
                    # Validate: must be under 280 chars
                    if len(improved) <= 280:
                        logger.info(f"AI improved tweet: {tweet[:50]}... -> {improved[:50]}...")
                        return improved
                    else:
                        logger.warning(f"AI result too long ({len(improved)} chars), using original")
                        return tweet
                else:
                    logger.error(f"AI API error: {data}")
                    return tweet
            else:
                logger.error(f"AI API returned status {response.status_code}")
                return tweet
                
        except httpx.TimeoutException:
            logger.error("AI API timeout, using original tweet")
            return tweet
        except Exception as e:
            logger.error(f"AI improvement error: {e}")
            return tweet
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Sync wrapper for convenience
def improve_tweet_sync(api_url: str, tweet: str, prompt_template: str, 
                       timeout: int = 10) -> str:
    """Synchronous wrapper for improve_tweet"""
    async def _improve():
        client = AIClient(api_url, timeout)
        result = await client.improve_tweet(tweet, prompt_template)
        await client.close()
        return result
    
    return asyncio.run(_improve())
