#!/usr/bin/env python3
"""
Twitter Cookie Extractor
Extract ct0 and auth_token from Cookie-Editor JSON export

Usage:
    python3 extract_twitter_cookies.py
    # Then paste JSON from Cookie-Editor and press Ctrl+D
"""

import json
import sys
import os
from pathlib import Path

def main():
    print("=" * 70)
    print("🍪 TWITTER COOKIE EXTRACTOR")
    print("=" * 70)
    print()
    print("📋 Instructions:")
    print("   1. Install Cookie-Editor extension in your browser")
    print("   2. Login to Twitter (x.com)")
    print("   3. Click Cookie-Editor icon → Export → JSON")
    print("   4. Copy the JSON output")
    print("   5. Paste here and press Ctrl+D (Linux/Mac) or Ctrl+Z Enter (Windows)")
    print()
    print("-" * 70)
    print("Paste JSON here:")
    print()
    
    try:
        # Read JSON from stdin
        input_data = sys.stdin.read().strip()
        
        if not input_data:
            print("❌ Error: No input received")
            sys.exit(1)
        
        # Parse JSON
        all_cookies = json.loads(input_data)
        
        # Extract needed cookies
        needed = {}
        for cookie in all_cookies:
            name = cookie.get('name', '')
            value = cookie.get('value', '')
            
            if name == 'ct0':
                needed['ct0'] = value
            elif name == 'auth_token':
                needed['auth_token'] = value
        
        # Validate
        if not needed.get('ct0'):
            print("❌ Error: 'ct0' cookie not found!")
            print("   Make sure you're logged in to Twitter.")
            sys.exit(1)
        
        if not needed.get('auth_token'):
            print("❌ Error: 'auth_token' cookie not found!")
            print("   Make sure you're logged in to Twitter.")
            sys.exit(1)
        
        print()
        print("=" * 70)
        print("✅ COOKIES EXTRACTED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print(f"   ct0:        {needed['ct0'][:30]}...")
        print(f"   auth_token: {needed['auth_token'][:30]}...")
        print()
        
        # Ask for account folder
        print("-" * 70)
        print("📁 Account folder:")
        print()
        
        # List existing accounts
        accounts_dir = Path('accounts')
        if accounts_dir.exists():
            existing = [d.name for d in accounts_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
            if existing:
                print("   Existing accounts:")
                for acc in existing:
                    print(f"   - {acc}")
                print()
        
        while True:
            account_folder = input("Enter account folder name (e.g., account1_GrnStore4347): ").strip()
            
            if not account_folder:
                print("❌ Account folder cannot be empty!")
                continue
            
            # Check if folder exists
            target_dir = accounts_dir / account_folder
            if not target_dir.exists():
                print(f"⚠️  Warning: Folder '{account_folder}' does not exist.")
                create = input("Create folder? (y/n): ").strip().lower()
                if create == 'y':
                    target_dir.mkdir(parents=True, exist_ok=True)
                    (target_dir / 'config').mkdir(exist_ok=True)
                    (target_dir / 'data').mkdir(exist_ok=True)
                    (target_dir / 'media' / 'promo').mkdir(parents=True, exist_ok=True)
                    print(f"✅ Created: {target_dir}")
                else:
                    continue
            
            break
        
        # Save cookies
        output_file = target_dir / 'cookies.json'
        
        with open(output_file, 'w') as f:
            json.dump(needed, f, indent=2)
        
        # Set permissions (Unix only)
        if os.name != 'nt':
            os.chmod(output_file, 0o600)
        
        print()
        print("=" * 70)
        print("🎉 SUCCESS!")
        print("=" * 70)
        print()
        print(f"📄 Cookies saved to: {output_file}")
        print()
        print("💡 Next steps:")
        print(f"   1. Test connection:")
        account_id = account_folder.split('_')[0]
        print(f"      python3 main.py --account {account_id} --test")
        print()
        print(f"   2. Start bot:")
        print(f"      python3 main.py --account {account_id} --daemon")
        print()
        print(f"   3. Or via PM2:")
        print(f"      pm2 start ecosystem.config.js")
        print()
        
    except json.JSONDecodeError as e:
        print()
        print("❌ Error: Invalid JSON format!")
        print(f"   {e}")
        print()
        print("💡 Make sure you copied the entire JSON from Cookie-Editor")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print()
        print("❌ Cancelled by user")
        sys.exit(1)
        
    except Exception as e:
        print()
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
