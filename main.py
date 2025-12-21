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


async def run_once(slot: str):
    """Run bot once (manual trigger)"""
    print_banner()
    print(f"\n🔧 Running {slot} slot...\n")
    
    bot = BotAutomation()
    
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


async def run_scheduled():
    """Run bot with schedule (daemon mode)"""
    print_banner()
    print("\n🕐 Starting bot in scheduled mode...")
    print("Press Ctrl+C to stop\n")
    
    bot = BotAutomation()
    
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
    
    args = parser.parse_args()
    
    # Create data/logs directory if not exists
    Path('data/logs').mkdir(parents=True, exist_ok=True)
    
    if args.test:
        print_banner()
        print("\n🔍 Testing connection...\n")
        
        bot = BotAutomation()
        
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
        asyncio.run(run_once(args.run_once))
    
    elif args.daemon:
        asyncio.run(run_scheduled())
    
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
