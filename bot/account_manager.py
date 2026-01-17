"""
Account Manager - Manage multiple Twitter accounts

This module handles loading and managing multiple Twitter accounts
from the accounts.yaml configuration file.
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class AccountManager:
    """
    Manages multiple Twitter accounts.
    
    Responsibilities:
    - Load accounts from accounts.yaml
    - Provide account information
    - Track enabled/disabled accounts
    """
    
    def __init__(self, config_path: str = 'config/accounts.yaml'):
        """
        Initialize AccountManager.
        
        Args:
            config_path: Path to accounts.yaml file
        """
        self.config_path = config_path
        self.config = None
        self.accounts = []
        
        # Load configuration
        self.reload()
    
    def reload(self):
        """Reload accounts configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            
            self.accounts = self.config.get('accounts', [])
            
            logger.info(f"✅ Loaded {len(self.accounts)} account(s) from {self.config_path}")
            
        except FileNotFoundError:
            logger.error(f"❌ Config file not found: {self.config_path}")
            self.config = {'accounts': [], 'settings': {}}
            self.accounts = []
        except Exception as e:
            logger.error(f"❌ Error loading config: {e}")
            self.config = {'accounts': [], 'settings': {}}
            self.accounts = []
    
    def get_account(self, account_id: str) -> Optional[Dict]:
        """
        Get account configuration by ID.
        
        Args:
            account_id: Account ID (e.g., 'account1')
        
        Returns:
            Account dict or None if not found
        """
        for account in self.accounts:
            if account.get('id') == account_id:
                return account
        return None
    
    def get_enabled_accounts(self) -> List[Dict]:
        """
        Get list of enabled accounts.
        
        Returns:
            List of enabled account dicts
        """
        return [acc for acc in self.accounts if acc.get('enabled', False)]
    
    def get_all_accounts(self) -> List[Dict]:
        """
        Get list of all accounts.
        
        Returns:
            List of all account dicts
        """
        return self.accounts
    
    def get_settings(self) -> Dict:
        """
        Get global settings.
        
        Returns:
            Settings dict
        """
        return self.config.get('settings', {})
    
    def get_max_concurrent(self) -> int:
        """
        Get max concurrent accounts setting.
        
        Returns:
            Max concurrent accounts
        """
        return self.get_settings().get('max_concurrent_accounts', 3)
    
    def get_global_rate_limits(self) -> Dict:
        """
        Get global rate limits.
        
        Returns:
            Rate limits dict
        """
        return self.get_settings().get('global_rate_limit', {})
    
    def account_exists(self, account_id: str) -> bool:
        """
        Check if account exists.
        
        Args:
            account_id: Account ID
        
        Returns:
            True if account exists
        """
        return self.get_account(account_id) is not None
    
    def is_enabled(self, account_id: str) -> bool:
        """
        Check if account is enabled.
        
        Args:
            account_id: Account ID
        
        Returns:
            True if account is enabled
        """
        account = self.get_account(account_id)
        return account.get('enabled', False) if account else False
    
    def get_account_folder(self, account_id: str) -> Optional[str]:
        """
        Get account folder path.
        
        Args:
            account_id: Account ID
        
        Returns:
            Folder path or None
        """
        account = self.get_account(account_id)
        return account.get('folder') if account else None
    
    def __repr__(self):
        """String representation."""
        enabled = len(self.get_enabled_accounts())
        total = len(self.accounts)
        return f"<AccountManager: {enabled}/{total} accounts enabled>"
