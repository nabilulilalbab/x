#!/usr/bin/env python3
"""
Twitter Bot - Main Entry Point
Kuota XL Sales Automation Bot
"""

import asyncio
import argparse
import logging
import sys
from pathlib import Path

from bot.automation import BotAutomation

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def print_banner():
    """Print bot banner"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║           🚀 TWITTER BOT - KUOTA XL AUTOMATION 🚀              ║
║                                                                ║
║  Safe, Dynamic, AI-Powered Twitter Marketing Bot              ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)


async def run_once(slot: str, account_folder: str = None):
    """Run bot once (manual trigger)"""
    print_banner()
    print(f"\n🔧 Running {slot} slot...\n")
    
    bot = BotAutomation(account_folder=account_folder)
    
    try:
        await bot.run_once(slot)
        print(f"\n✅ {slot.capitalize()} slot completed!")
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.exception("Fatal error")
    finally:
        await bot.cleanup()


async def run_scheduled(account_folder: str = None):
    """Run bot with schedule (daemon mode)"""
    print_banner()
    print("\n🕐 Starting bot in scheduled mode...")
    print("Press Ctrl+C to stop\n")
    
    bot = BotAutomation(account_folder=account_folder)
    
    try:
        await bot.run_scheduled()
    except KeyboardInterrupt:
        print("\n⚠️  Stopping bot...")
        bot.stop()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        logger.exception("Fatal error")
    finally:
        await bot.cleanup()
        print("\n👋 Bot stopped!")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Twitter Bot for Kuota XL Sales',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --run-once morning     Run morning slot once
  python main.py --daemon               Run in scheduled mode
  python main.py --test                 Test connection only
  
Multi-Account Examples:
  python main.py --account account1 --run-once morning
  python main.py --account account2 --daemon
  python main.py --list-accounts        List all accounts
        """
    )
    
    parser.add_argument(
        '--run-once',
        choices=['morning', 'afternoon', 'evening'],
        help='Run one slot manually'
    )
    
    parser.add_argument(
        '--daemon',
        action='store_true',
        help='Run in scheduled mode (background)'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test connection and exit'
    )
    
    parser.add_argument(
        '--account',
        type=str,
        help='Account ID for multi-account mode (e.g., account1)'
    )
    
    parser.add_argument(
        '--list-accounts',
        action='store_true',
        help='List all available accounts'
    )
    
    args = parser.parse_args()
    
    # Handle list-accounts command
    if args.list_accounts:
        from bot.account_manager import AccountManager
        
        print_banner()
        print("\n📋 Available Accounts:\n")
        
        manager = AccountManager()
        accounts = manager.get_all_accounts()
        
        if not accounts:
            print("   No accounts configured yet.")
            print("   Create accounts.yaml to add accounts.")
            return
        
        for account in accounts:
            status = "🟢 ENABLED" if account.get('enabled') else "⭕ DISABLED"
            print(f"   {status} {account['id']}")
            print(f"      Name: {account['name']}")
            print(f"      Username: {account['username']}")
            print(f"      Folder: {account['folder']}")
            print()
        
        print(f"Total: {len(accounts)} account(s)\n")
        return
    
    # Determine account folder based on --account parameter
    account_folder = None
    if args.account:
        from bot.account_manager import AccountManager
        
        manager = AccountManager()
        account = manager.get_account(args.account)
        
        if not account:
            print(f"\n❌ Error: Account '{args.account}' not found!")
            print(f"   Run: python main.py --list-accounts")
            return
        
        if not account.get('enabled'):
            print(f"\n⚠️  Warning: Account '{args.account}' is disabled!")
            response = input(f"   Run anyway? (yes/no): ").lower()
            if response != 'yes':
                print("   Cancelled.")
                return
        
        account_folder = account['folder']
        print(f"\n🔀 Multi-Account Mode: {account['name']} ({account['username']})")
    
    # Create data/logs directory if not exists
    if account_folder:
        Path(f'{account_folder}/data/logs').mkdir(parents=True, exist_ok=True)
    else:
        Path('data/logs').mkdir(parents=True, exist_ok=True)
    
    if args.test:
        print_banner()
        print("\n🔍 Testing connection...\n")
        
        bot = BotAutomation(account_folder=account_folder)
        
        async def test():
            success = await bot.initialize()
            if success:
                print("\n✅ Connection test passed!")
                print(f"   Logged in as: @{bot.twitter.me.screen_name}")
                print(f"   Followers: {bot.twitter.me.followers_count}")
                print(f"   Following: {bot.twitter.me.following_count}")
            else:
                print("\n❌ Connection test failed!")
            await bot.cleanup()
        
        asyncio.run(test())
    
    elif args.run_once:
        asyncio.run(run_once(args.run_once, account_folder))
    
    elif args.daemon:
        asyncio.run(run_scheduled(account_folder))
    
    else:
        print_banner()
        print("\n📖 Usage:")
        print("  python main.py --run-once morning    # Run morning slot")
        print("  python main.py --daemon              # Run scheduled mode")
        print("  python main.py --test                # Test connection")
        print("  python dashboard.py                  # Start web dashboard")
        print("\n💡 For web dashboard, run: python dashboard.py")
        print("   Then open http://localhost:5000 in browser\n")


if __name__ == '__main__':
    main()
