"""
Multi-Account Runner
Run multiple Twitter accounts concurrently
"""

import asyncio
import logging
from typing import Dict, List, Optional, Set
from datetime import datetime

from .account_manager import AccountManager
from .automation import BotAutomation

logger = logging.getLogger(__name__)


class MultiAccountRunner:
    """
    Run multiple Twitter bot accounts concurrently.
    
    Features:
    - Start/stop individual accounts
    - Start/stop all enabled accounts
    - Monitor account health
    - Isolate errors per account
    - Resource management
    """
    
    def __init__(self):
        """Initialize MultiAccountRunner."""
        self.account_manager = AccountManager()
        
        # Active bots and tasks
        self.bots: Dict[str, BotAutomation] = {}
        self.tasks: Dict[str, asyncio.Task] = {}
        
        # Account status tracking
        self.statuses: Dict[str, Dict] = {}
        self.errors: Dict[str, List[str]] = {}
        
        # Running flag
        self.is_running = False
        
        logger.info("✅ MultiAccountRunner initialized")
    
    async def start_account(self, account_id: str) -> bool:
        """
        Start a single account.
        
        Args:
            account_id: Account ID to start
        
        Returns:
            True if started successfully, False otherwise
        """
        try:
            # Check if account exists and is enabled
            account = self.account_manager.get_account(account_id)
            
            if not account:
                logger.error(f"❌ Account {account_id} not found")
                return False
            
            if not account.get('enabled'):
                logger.warning(f"⚠️  Account {account_id} is disabled")
                return False
            
            # Check if already running
            if account_id in self.bots and self.bots[account_id].is_running:
                logger.warning(f"⚠️  Account {account_id} is already running")
                return False
            
            logger.info(f"🚀 Starting account: {account['name']} ({account['username']})")
            
            # Create bot instance
            bot = BotAutomation(account_folder=account['folder'])
            
            # Initialize bot
            success = await bot.initialize()
            
            if not success:
                logger.error(f"❌ Failed to initialize account {account_id}")
                return False
            
            # Store bot
            self.bots[account_id] = bot
            
            # Create and store task
            task = asyncio.create_task(
                self._run_account_with_error_handling(account_id, bot)
            )
            self.tasks[account_id] = task
            
            # Update status
            self.statuses[account_id] = {
                'account_id': account_id,
                'name': account['name'],
                'username': account['username'],
                'status': 'running',
                'started_at': datetime.now().isoformat(),
                'error': None
            }
            
            logger.info(f"✅ Account {account_id} started successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error starting account {account_id}: {e}")
            self._record_error(account_id, str(e))
            return False
    
    async def _run_account_with_error_handling(self, account_id: str, bot: BotAutomation):
        """
        Run account with error handling and isolation.
        
        Args:
            account_id: Account ID
            bot: BotAutomation instance
        """
        try:
            logger.info(f"🏃 Running scheduled mode for account {account_id}")
            await bot.run_scheduled()
            
        except asyncio.CancelledError:
            logger.info(f"⚠️  Account {account_id} task cancelled")
            raise
            
        except Exception as e:
            logger.error(f"❌ Account {account_id} error: {e}")
            self._record_error(account_id, str(e))
            
            # Update status
            if account_id in self.statuses:
                self.statuses[account_id]['status'] = 'error'
                self.statuses[account_id]['error'] = str(e)
        
        finally:
            # Cleanup
            try:
                await bot.cleanup()
            except Exception as e:
                logger.error(f"❌ Cleanup error for {account_id}: {e}")
            
            # Update status
            if account_id in self.statuses:
                self.statuses[account_id]['status'] = 'stopped'
                self.statuses[account_id]['stopped_at'] = datetime.now().isoformat()
    
    async def stop_account(self, account_id: str) -> bool:
        """
        Stop a single account.
        
        Args:
            account_id: Account ID to stop
        
        Returns:
            True if stopped successfully, False otherwise
        """
        try:
            if account_id not in self.bots:
                logger.warning(f"⚠️  Account {account_id} is not running")
                return False
            
            logger.info(f"🛑 Stopping account: {account_id}")
            
            # Stop bot
            bot = self.bots[account_id]
            bot.stop()
            
            # Cancel task
            if account_id in self.tasks:
                task = self.tasks[account_id]
                task.cancel()
                
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            
            # Cleanup
            await bot.cleanup()
            
            # Remove from active
            del self.bots[account_id]
            if account_id in self.tasks:
                del self.tasks[account_id]
            
            # Update status
            if account_id in self.statuses:
                self.statuses[account_id]['status'] = 'stopped'
                self.statuses[account_id]['stopped_at'] = datetime.now().isoformat()
            
            logger.info(f"✅ Account {account_id} stopped successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error stopping account {account_id}: {e}")
            return False
    
    async def start_all(self) -> Dict[str, bool]:
        """
        Start all enabled accounts.
        
        Returns:
            Dict mapping account_id to success status
        """
        logger.info("🚀 Starting all enabled accounts...")
        
        accounts = self.account_manager.get_enabled_accounts()
        results = {}
        
        for account in accounts:
            account_id = account['id']
            success = await self.start_account(account_id)
            results[account_id] = success
        
        self.is_running = True
        
        logger.info(f"✅ Started {sum(results.values())}/{len(results)} accounts")
        return results
    
    async def stop_all(self) -> Dict[str, bool]:
        """
        Stop all running accounts.
        
        Returns:
            Dict mapping account_id to success status
        """
        logger.info("🛑 Stopping all accounts...")
        
        account_ids = list(self.bots.keys())
        results = {}
        
        for account_id in account_ids:
            success = await self.stop_account(account_id)
            results[account_id] = success
        
        self.is_running = False
        
        logger.info(f"✅ Stopped {sum(results.values())}/{len(results)} accounts")
        return results
    
    def get_account_status(self, account_id: str) -> Optional[Dict]:
        """
        Get status of a specific account.
        
        Args:
            account_id: Account ID
        
        Returns:
            Status dict or None if not found
        """
        if account_id in self.statuses:
            status = self.statuses[account_id].copy()
            
            # Add live bot status if running
            if account_id in self.bots:
                bot = self.bots[account_id]
                status['bot_status'] = bot.get_status()
            
            return status
        
        return None
    
    def get_all_statuses(self) -> Dict[str, Dict]:
        """
        Get status of all accounts.
        
        Returns:
            Dict mapping account_id to status
        """
        all_statuses = {}
        
        # Get all accounts from manager
        all_accounts = self.account_manager.get_all_accounts()
        
        for account in all_accounts:
            account_id = account['id']
            
            if account_id in self.statuses:
                # Running or recently stopped
                all_statuses[account_id] = self.get_account_status(account_id)
            else:
                # Never started
                all_statuses[account_id] = {
                    'account_id': account_id,
                    'name': account['name'],
                    'username': account['username'],
                    'status': 'idle',
                    'enabled': account.get('enabled', False)
                }
        
        return all_statuses
    
    def get_running_count(self) -> int:
        """Get number of running accounts."""
        return len(self.bots)
    
    def get_summary(self) -> Dict:
        """
        Get summary statistics.
        
        Returns:
            Summary dict
        """
        all_accounts = self.account_manager.get_all_accounts()
        enabled_accounts = self.account_manager.get_enabled_accounts()
        
        return {
            'total_accounts': len(all_accounts),
            'enabled_accounts': len(enabled_accounts),
            'running_accounts': self.get_running_count(),
            'is_running': self.is_running,
            'statuses': self.get_all_statuses()
        }
    
    def _record_error(self, account_id: str, error: str):
        """Record error for an account."""
        if account_id not in self.errors:
            self.errors[account_id] = []
        
        self.errors[account_id].append({
            'timestamp': datetime.now().isoformat(),
            'error': error
        })
        
        # Keep only last 10 errors
        self.errors[account_id] = self.errors[account_id][-10:]
    
    def get_errors(self, account_id: str) -> List[Dict]:
        """Get recent errors for an account."""
        return self.errors.get(account_id, [])
    
    async def restart_account(self, account_id: str) -> bool:
        """
        Restart an account (stop then start).
        
        Args:
            account_id: Account ID
        
        Returns:
            True if restarted successfully
        """
        logger.info(f"🔄 Restarting account: {account_id}")
        
        # Stop if running
        if account_id in self.bots:
            await self.stop_account(account_id)
            await asyncio.sleep(2)  # Wait a bit
        
        # Start
        return await self.start_account(account_id)
    
    def __repr__(self):
        """String representation."""
        return f"<MultiAccountRunner: {self.get_running_count()} running, {self.account_manager.get_all_accounts().__len__()} total>"
