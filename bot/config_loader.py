"""
Configuration loader
Load and reload YAML configs dynamically
"""

import yaml
import os
from typing import Dict, Any
from pathlib import Path


class ConfigLoader:
    """Dynamic config loader with hot reload support"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self._cache = {}
        self._mtime = {}
    
    def _should_reload(self, filepath: Path) -> bool:
        """Check if file should be reloaded"""
        if not filepath.exists():
            return False
        
        current_mtime = filepath.stat().st_mtime
        cached_mtime = self._mtime.get(str(filepath))
        
        if cached_mtime is None or current_mtime > cached_mtime:
            self._mtime[str(filepath)] = current_mtime
            return True
        
        return False
    
    def load(self, filename: str, force_reload: bool = False) -> Dict[str, Any]:
        """Load config file with caching"""
        filepath = self.config_dir / filename
        
        if force_reload or self._should_reload(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                self._cache[filename] = yaml.safe_load(f)
        
        return self._cache.get(filename, {})
    
    def get_settings(self) -> Dict:
        """Get main settings"""
        return self.load('settings.yaml')
    
    def get_templates(self) -> Dict:
        """Get templates"""
        return self.load('templates.yaml')
    
    def get_keywords(self) -> Dict:
        """Get keywords"""
        return self.load('keywords.yaml')
    
    def reload_all(self):
        """Force reload all configs"""
        for filename in ['settings.yaml', 'templates.yaml', 'keywords.yaml']:
            self.load(filename, force_reload=True)
