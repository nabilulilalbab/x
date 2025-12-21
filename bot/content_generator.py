"""
Content Generator
Generate tweets from templates with AI improvement
"""

import random
import logging
import os
from typing import Dict, Optional, List, Tuple
from pathlib import Path
from .config_loader import ConfigLoader
from .ai_client import AIClient

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Generate dynamic content from templates"""
    
    def __init__(self, config: ConfigLoader, ai_client: Optional[AIClient] = None):
        self.config = config
        self.ai_client = ai_client
    
    def _fill_wa_variables(self, text: str) -> str:
        """Fill only WA number and link variables"""
        try:
            settings = self.config.get_settings()
            business = settings['business']
            
            variables = {
                'wa_number': business.get('wa_number', ''),
                'wa_link': business.get('wa_link', '')
            }
            
            return text.format(**variables)
        except KeyError as e:
            logger.error(f"Missing variable in template: {e}")
            return text
        except Exception as e:
            logger.error(f"Error filling variables: {e}")
            return text
    
    async def generate_promo_tweet(self, use_ai: bool = True) -> Tuple[str, Optional[str]]:
        """Generate promotional tweet with optional media
        
        Returns:
            Tuple[str, Optional[str]]: (tweet_text, media_path)
        """
        templates_config = self.config.get_templates()
        promo_templates = templates_config.get('promo_templates', [])
        
        if not promo_templates:
            logger.error("No promo templates found!")
            return ("Kuota XL murah! DM untuk info.", None)
        
        # Pick random template
        template_item = random.choice(promo_templates)
        
        # Support both old format (string) and new format (dict)
        if isinstance(template_item, str):
            # Old format: plain string
            tweet = self._fill_wa_variables(template_item)
            media = None
        else:
            # New format: dict with text and media
            tweet = template_item.get('text', '')
            tweet = self._fill_wa_variables(tweet)
            media = template_item.get('media')
            
            # Validate media path (if specified)
            if media:
                if os.path.exists(media):
                    logger.info(f"✅ Using media: {media}")
                else:
                    logger.info(f"ℹ️  Media not found: {media}, posting text-only (this is OK if media is optional)")
                    media = None
            else:
                logger.debug(f"📝 Text-only tweet (no media assigned)")
        
        # AI improvement
        if use_ai and self.ai_client:
            settings = self.config.get_settings()
            if settings['ai']['enabled']:
                prompt = settings['ai']['improve_prompt']
                improved = await self.ai_client.improve_tweet(tweet, prompt)
                if improved:
                    tweet = improved
        
        return (tweet, media)
    
    async def generate_value_tweet(self, use_ai: bool = True) -> str:
        """Generate value content tweet"""
        templates_config = self.config.get_templates()
        value_templates = templates_config.get('value_templates', [])
        tips = templates_config.get('tips', [])
        tutorials = templates_config.get('tutorials', [])
        faqs = templates_config.get('faqs', [])
        facts = templates_config.get('facts', [])
        locations = templates_config.get('locations', [])
        reviews = templates_config.get('reviews', [])
        
        # Pick random template
        if not value_templates:
            return "Tips: Hemat kuota dengan matikan auto-play video!"
        
        template = random.choice(value_templates)
        
        # Get WA variables
        settings = self.config.get_settings()
        business = settings['business']
        
        variables = {
            'wa_number': business.get('wa_number', ''),
            'wa_link': business.get('wa_link', '')
        }
        
        # Add random value content
        if '{tip}' in template and tips:
            variables['tip'] = random.choice(tips)
            variables['number'] = random.randint(1, 50)
        
        if '{tutorial_title}' in template and tutorials:
            tutorial = random.choice(tutorials)
            variables['tutorial_title'] = tutorial['title']
            variables['tutorial_content'] = tutorial['content']
        
        if '{question}' in template and faqs:
            faq = random.choice(faqs)
            variables['question'] = faq['question']
            variables['answer'] = faq['answer']
        
        if '{fact}' in template and facts:
            variables['fact'] = random.choice(facts)
        
        if '{location}' in template and locations:
            variables['location'] = random.choice(locations)
        
        if '{review}' in template and reviews:
            variables['review'] = random.choice(reviews)
        
        try:
            tweet = template.format(**variables)
        except KeyError as e:
            logger.error(f"Missing variable in value template: {e}")
            tweet = template
        
        # AI improvement
        if use_ai and self.ai_client:
            if settings['ai']['enabled']:
                prompt = settings['ai']['improve_prompt']
                improved = await self.ai_client.improve_tweet(tweet, prompt)
                if improved:
                    tweet = improved
        
        return tweet
    
    def get_engagement_reply(self) -> str:
        """Get random engagement reply"""
        templates_config = self.config.get_templates()
        engagement_templates = templates_config.get('engagement_templates', [])
        
        if not engagement_templates:
            return "👍"
        
        return random.choice(engagement_templates)
    
    def get_search_keywords(self, intent_level: str = 'high') -> List[str]:
        """Get keywords by intent level"""
        keywords_config = self.config.get_keywords()
        
        intent_map = {
            'high': 'high_intent',
            'medium': 'medium_intent',
            'low': 'low_intent'
        }
        
        key = intent_map.get(intent_level, 'high_intent')
        return keywords_config.get(key, [])
    
    async def generate_custom_tweet(self, template: str, use_ai: bool = True) -> str:
        """Generate tweet from custom template (only fills WA variables)"""
        tweet = self._fill_wa_variables(template)
        
        if use_ai and self.ai_client:
            settings = self.config.get_settings()
            if settings['ai']['enabled']:
                prompt = settings['ai']['improve_prompt']
                improved = await self.ai_client.improve_tweet(tweet, prompt)
                if improved:
                    tweet = improved
        
        return tweet
