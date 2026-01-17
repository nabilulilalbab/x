"""
Web Dashboard for Twitter Bot
Flask web interface for monitoring and management
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
from datetime import datetime, timedelta
import asyncio
import threading
import logging
from pathlib import Path

from bot.database import Database
from bot.config_loader import ConfigLoader
from bot.automation import BotAutomation
from bot.multi_account_runner import MultiAccountRunner

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
CORS(app)

# Initialize components
db = Database()
config = ConfigLoader()
bot = None
bot_thread = None

# Multi-account runner (singleton)
multi_runner = None

# Load config
settings = config.get_settings()
app.config['SECRET_KEY'] = settings['dashboard']['secret_key']


# ============= ROUTES =============

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/accounts')
def accounts_page():
    """Accounts management page"""
    return render_template('accounts.html')


@app.route('/media')
def media_manager():
    """Media manager page"""
    return render_template('media_manager.html')


@app.route('/media/promo/<path:filename>')
def serve_media(filename):
    """Serve media files"""
    from flask import send_from_directory
    import os
    
    media_folder = os.path.join(os.getcwd(), 'media', 'promo')
    return send_from_directory(media_folder, filename)


@app.route('/api/stats')
def get_stats():
    """Get dashboard statistics"""
    try:
        account_id = request.args.get('account_id')
        
        # Load per-account or global database
        if account_id:
            from bot.account_manager import AccountManager
            manager = AccountManager()
            account = manager.get_account(account_id)
            
            if not account:
                return jsonify({'success': False, 'error': 'Account not found'}), 404
            
            account_db = Database(db_path=f"{account['folder']}/data/metrics.db")
            stats = account_db.get_dashboard_stats()
        else:
            # Global stats
            stats = db.get_dashboard_stats()
        
        # Add rate limits if bot is running
        rate_limits = {}
        if bot and bot.twitter.client:
            try:
                rate_limits = asyncio.run(bot.twitter.get_rate_limit_status())
            except:
                pass
        
        return jsonify({
            'success': True,
            'data': {
                **stats,
                'rate_limits': rate_limits,
                'bot_running': bot is not None and bot.is_running,
                'account_id': account_id
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/activity/today')
def get_today_activity():
    """Get today's activity"""
    try:
        account_id = request.args.get('account_id')
        
        if account_id:
            from bot.account_manager import AccountManager
            manager = AccountManager()
            account = manager.get_account(account_id)
            
            if not account:
                return jsonify({'success': False, 'error': 'Account not found'}), 404
            
            account_db = Database(db_path=f"{account['folder']}/data/metrics.db")
            activity = account_db.get_daily_activity()
        else:
            activity = db.get_daily_activity()
        
        return jsonify({'success': True, 'data': activity})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/tweets/recent')
def get_recent_tweets():
    """Get recent tweets with stats"""
    try:
        account_id = request.args.get('account_id')
        limit = request.args.get('limit', 10, type=int)
        
        if account_id:
            from bot.account_manager import AccountManager
            manager = AccountManager()
            account = manager.get_account(account_id)
            
            if not account:
                return jsonify({'success': False, 'error': 'Account not found'}), 404
            
            account_db = Database(db_path=f"{account['folder']}/data/metrics.db")
            tweets = account_db.get_recent_tweets(limit)
        else:
            tweets = db.get_recent_tweets(limit)
        
        return jsonify({'success': True, 'data': tweets})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/tweets/best')
def get_best_tweet():
    """Get best performing tweet"""
    try:
        days = request.args.get('days', 7, type=int)
        tweet = db.get_best_tweet(days)
        return jsonify({'success': True, 'data': tweet})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/growth')
def get_growth():
    """Get follower growth data"""
    try:
        account_id = request.args.get('account_id')
        days = request.args.get('days', 30, type=int)
        
        if account_id:
            from bot.account_manager import AccountManager
            manager = AccountManager()
            account = manager.get_account(account_id)
            
            if not account:
                return jsonify({'success': False, 'error': 'Account not found'}), 404
            
            account_db = Database(db_path=f"{account['folder']}/data/metrics.db")
            growth = account_db.get_follower_growth(days)
        else:
            growth = db.get_follower_growth(days)
        
        return jsonify({'success': True, 'data': growth})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/conversions')
def get_conversions():
    """Get conversion data"""
    try:
        days = request.args.get('days', 7, type=int)
        conversions = db.get_conversions(days)
        summary = db.get_conversion_summary(days)
        
        return jsonify({
            'success': True,
            'data': {
                'conversions': conversions,
                'summary': summary
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/keywords')
def get_keywords():
    """Get keyword performance"""
    try:
        account_id = request.args.get('account_id')
        days = request.args.get('days', 7, type=int)
        
        if account_id:
            from bot.account_manager import AccountManager
            manager = AccountManager()
            account = manager.get_account(account_id)
            
            if not account:
                return jsonify({'success': False, 'error': 'Account not found'}), 404
            
            account_db = Database(db_path=f"{account['folder']}/data/metrics.db")
            keywords = account_db.get_keyword_performance(days)
        else:
            keywords = db.get_keyword_performance(days)
        
        return jsonify({'success': True, 'data': keywords})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/logs')
def get_logs():
    """Get recent activity logs"""
    try:
        account_id = request.args.get('account_id')
        limit = request.args.get('limit', 50, type=int)
        
        if account_id:
            from bot.account_manager import AccountManager
            manager = AccountManager()
            account = manager.get_account(account_id)
            
            if not account:
                return jsonify({'success': False, 'error': 'Account not found'}), 404
            
            account_db = Database(db_path=f"{account['folder']}/data/metrics.db")
            logs = account_db.get_recent_logs(limit)
        else:
            logs = db.get_recent_logs(limit)
        
        return jsonify({'success': True, 'data': logs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/config')
def get_config():
    """Get current configuration"""
    try:
        account_id = request.args.get('account_id')
        
        if account_id:
            from bot.account_manager import AccountManager
            manager = AccountManager()
            account = manager.get_account(account_id)
            
            if not account:
                return jsonify({'success': False, 'error': 'Account not found'}), 404
            
            account_config = ConfigLoader(config_dir=f"{account['folder']}/config")
            
            return jsonify({
                'success': True,
                'data': {
                    'settings': account_config.get_settings(),
                    'templates': account_config.get_templates(),
                    'keywords': account_config.get_keywords(),
                    'account_id': account_id
                }
            })
        else:
            config.reload_all()
            
            return jsonify({
                'success': True,
                'data': {
                    'settings': config.get_settings(),
                    'templates': config.get_templates(),
                    'keywords': config.get_keywords()
                }
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/config/settings', methods=['POST'])
def update_settings():
    """Update settings configuration"""
    try:
        import yaml
        
        account_id = request.args.get('account_id')
        new_settings = request.json
        
        if account_id:
            from bot.account_manager import AccountManager
            manager = AccountManager()
            account = manager.get_account(account_id)
            
            if not account:
                return jsonify({'success': False, 'error': 'Account not found'}), 404
            
            settings_file = f"{account['folder']}/config/settings.yaml"
        else:
            settings_file = 'config/settings.yaml'
        
        # Save to file
        with open(settings_file, 'w') as f:
            yaml.dump(new_settings, f, default_flow_style=False, allow_unicode=True)
        
        config.reload_all()
        
        return jsonify({'success': True, 'message': 'Settings updated'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/config/templates', methods=['POST'])
def update_templates():
    """Update templates configuration"""
    try:
        import yaml
        
        account_id = request.args.get('account_id')
        new_templates = request.json
        
        if account_id:
            from bot.account_manager import AccountManager
            manager = AccountManager()
            account = manager.get_account(account_id)
            
            if not account:
                return jsonify({'success': False, 'error': 'Account not found'}), 404
            
            templates_file = f"{account['folder']}/config/templates.yaml"
        else:
            templates_file = 'config/templates.yaml'
        
        # Save to file
        with open(templates_file, 'w') as f:
            yaml.dump(new_templates, f, default_flow_style=False, allow_unicode=True)
        
        config.reload_all()
        
        return jsonify({'success': True, 'message': 'Templates updated'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/templates/assign-media', methods=['POST'])
def assign_media_to_template():
    """Assign media file to a specific promo template"""
    try:
        import yaml
        
        data = request.json
        template_index = data.get('template_index')
        media_file = data.get('media_file')  # filename or null
        
        # Load current templates
        with open('config/templates.yaml', 'r') as f:
            templates = yaml.safe_load(f)
        
        # Update media path
        if 0 <= template_index < len(templates['promo_templates']):
            template = templates['promo_templates'][template_index]
            
            # Ensure template is object format
            if isinstance(template, str):
                templates['promo_templates'][template_index] = {
                    'text': template,
                    'media': f"media/promo/{media_file}" if media_file else None
                }
            else:
                template['media'] = f"media/promo/{media_file}" if media_file else None
            
            # Save
            with open('config/templates.yaml', 'w') as f:
                yaml.dump(templates, f, default_flow_style=False, allow_unicode=True)
            
            config.reload_all()
            
            return jsonify({'success': True, 'message': 'Media assigned to template'})
        else:
            return jsonify({'success': False, 'error': 'Invalid template index'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/config/keywords', methods=['POST'])
def update_keywords():
    """Update keywords configuration"""
    try:
        import yaml
        
        new_keywords = request.json
        
        # Save to file
        with open('config/keywords.yaml', 'w') as f:
            yaml.dump(new_keywords, f, default_flow_style=False, allow_unicode=True)
        
        config.reload_all()
        
        return jsonify({'success': True, 'message': 'Keywords updated'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/preview-tweet', methods=['POST'])
def preview_tweet():
    """Preview generated tweet (simple version without AI in dashboard)"""
    try:
        data = request.json
        template = data.get('template', '')
        use_ai = data.get('use_ai', False)  # Disable AI in dashboard for stability
        
        if not template:
            return jsonify({'success': False, 'error': 'Template is required'}), 400
        
        # Simple preview: just fill WA variables
        from bot.config_loader import ConfigLoader
        
        config_loader = ConfigLoader()
        settings = config_loader.get_settings()
        business = settings['business']
        
        # Only WA variables (no more price variables)
        variables = {
            'wa_number': business.get('wa_number', ''),
            'wa_link': business.get('wa_link', '')
        }
        
        # Fill template
        try:
            generated = template.format(**variables)
        except KeyError as e:
            return jsonify({
                'success': False, 
                'error': f'Missing variable in template: {e}'
            }), 400
        
        note = "Note: This is a simple preview. AI improvement will happen when bot actually posts the tweet."
        
        return jsonify({
            'success': True,
            'data': {
                'original': template,
                'generated': generated,
                'length': len(generated),
                'note': note,
                'variables_available': '{wa_number}, {wa_link}'
            }
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/conversion/add', methods=['POST'])
def add_conversion():
    """Manually add conversion data"""
    try:
        data = request.json
        
        db.add_conversion(
            wa_messages=data.get('wa_messages', 0),
            orders=data.get('orders', 0),
            revenue=data.get('revenue', 0),
            notes=data.get('notes')
        )
        
        return jsonify({'success': True, 'message': 'Conversion added'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/media/upload', methods=['POST'])
def upload_media():
    """Upload media file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Check file extension
        allowed_extensions = ['jpg', 'jpeg', 'png', 'mp4']
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if ext not in allowed_extensions:
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        # Save file
        import os
        from werkzeug.utils import secure_filename
        
        filename = secure_filename(file.filename)
        upload_folder = 'media/promo'
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        return jsonify({'success': True, 'filename': filename, 'path': filepath})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/media/list')
def list_media():
    """List all media files"""
    try:
        import os
        
        upload_folder = 'media/promo'
        if not os.path.exists(upload_folder):
            return jsonify({'success': True, 'files': []})
        
        files = [f for f in os.listdir(upload_folder) 
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4'))]
        
        return jsonify({'success': True, 'files': files})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/media/delete', methods=['POST'])
def delete_media():
    """Delete media file"""
    try:
        data = request.json
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'success': False, 'error': 'No filename provided'}), 400
        
        import os
        from werkzeug.utils import secure_filename
        
        filename = secure_filename(filename)
        filepath = os.path.join('media/promo', filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True, 'message': 'File deleted'})
        else:
            return jsonify({'success': False, 'error': 'File not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bot/start', methods=['POST'])
def start_bot():
    """Start bot (scheduled mode)"""
    global bot, bot_thread
    
    try:
        if bot and bot.is_running:
            return jsonify({'success': False, 'error': 'Bot already running'})
        
        bot = BotAutomation()
        
        def run_bot():
            asyncio.run(bot.run_scheduled())
        
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        
        return jsonify({'success': True, 'message': 'Bot started'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bot/stop', methods=['POST'])
def stop_bot():
    """Stop bot"""
    global bot
    
    try:
        if not bot or not bot.is_running:
            return jsonify({'success': False, 'error': 'Bot not running'})
        
        bot.stop()
        
        return jsonify({'success': True, 'message': 'Bot stopped'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bot/status')
def get_bot_status():
    """Get bot status"""
    try:
        if bot:
            status = bot.get_status()
            return jsonify({'success': True, 'data': status})
        else:
            return jsonify({
                'success': True,
                'data': {'is_running': False}
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bot/run-once', methods=['POST'])
def run_once():
    """Run bot once (manual trigger)"""
    try:
        data = request.json
        slot = data.get('slot', 'morning')
        account_id = data.get('account_id')
        
        if account_id:
            from bot.account_manager import AccountManager
            manager = AccountManager()
            account = manager.get_account(account_id)
            
            if not account:
                return jsonify({'success': False, 'error': 'Account not found'}), 404
            
            temp_bot = BotAutomation(account_folder=account['folder'])
        else:
            temp_bot = BotAutomation()
        
        def run():
            asyncio.run(temp_bot.run_once(slot))
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        
        return jsonify({'success': True, 'message': f'Running {slot} slot for {account_id or "default"}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= MULTI-ACCOUNT API ENDPOINTS =============

@app.route('/api/accounts')
def list_accounts():
    """List all accounts"""
    try:
        from bot.account_manager import AccountManager
        import yaml
        import os
        
        manager = AccountManager()
        accounts = manager.get_all_accounts()
        settings = manager.get_settings()
        
        # Enrich accounts with wa_number from their settings.yaml
        for account in accounts:
            folder = account.get('folder')
            if folder and os.path.exists(f"{folder}/config/settings.yaml"):
                try:
                    with open(f"{folder}/config/settings.yaml", 'r') as f:
                        account_settings = yaml.safe_load(f)
                        business = account_settings.get('business', {})
                        account['wa_number'] = business.get('wa_number', '')
                        account['wa_link'] = business.get('wa_link', '')
                except:
                    pass
        
        return jsonify({
            'success': True,
            'data': {
                'accounts': accounts,
                'settings': settings,
                'total': len(accounts),
                'enabled': len([a for a in accounts if a.get('enabled')])
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>')
def get_account(account_id):
    """Get specific account details"""
    try:
        from bot.account_manager import AccountManager
        
        manager = AccountManager()
        account = manager.get_account(account_id)
        
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        # Get additional info
        import os
        folder = account.get('folder')
        
        # Check if folder exists
        folder_exists = os.path.exists(folder) if folder else False
        
        # Check if configs exist
        config_exists = False
        cookies_exists = False
        if folder_exists:
            config_exists = os.path.exists(f"{folder}/config")
            cookies_exists = os.path.exists(f"{folder}/cookies.json")
        
        return jsonify({
            'success': True,
            'data': {
                **account,
                'folder_exists': folder_exists,
                'config_exists': config_exists,
                'cookies_exists': cookies_exists
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>/delete', methods=['DELETE'])
def delete_account(account_id):
    """Delete account (with safety checks)"""
    try:
        import os
        import shutil
        from datetime import datetime
        from bot.account_manager import AccountManager
        import yaml
        
        manager = AccountManager()
        account = manager.get_account(account_id)
        
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        folder = account.get('folder')
        
        # Safety check: Don't delete if it's the only account
        all_accounts = manager.get_all_accounts()
        if len(all_accounts) <= 1:
            return jsonify({
                'success': False,
                'error': 'Cannot delete the only account. Create another account first.'
            }), 400
        
        # Safety check: Don't delete if account is enabled (to prevent accidents)
        if account.get('enabled'):
            return jsonify({
                'success': False,
                'error': 'Cannot delete enabled account. Disable it first for safety.'
            }), 400
        
        # Create backup before deletion
        backup_folder = None
        if folder and os.path.exists(folder):
            backup_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_folder = f"{folder}.backup_{backup_suffix}"
            
            try:
                shutil.copytree(folder, backup_folder)
                print(f"   ✅ Backup created: {backup_folder}")
            except Exception as e:
                print(f"   ⚠️  Backup failed: {e}")
                # Continue anyway - user requested deletion
        
        # Remove from accounts.yaml
        with open('config/accounts.yaml', 'r') as f:
            accounts_config = yaml.safe_load(f)
        
        accounts_config['accounts'] = [
            acc for acc in accounts_config['accounts'] 
            if acc['id'] != account_id
        ]
        
        with open('config/accounts.yaml', 'w') as f:
            yaml.dump(accounts_config, f, default_flow_style=False, allow_unicode=True)
        
        # Delete folder
        if folder and os.path.exists(folder):
            shutil.rmtree(folder)
        
        # Reload account manager
        manager.reload()
        
        return jsonify({
            'success': True,
            'message': f'Account {account_id} deleted successfully',
            'backup': backup_folder if backup_folder else None
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>/update', methods=['PUT'])
def update_account(account_id):
    """Update account configuration"""
    try:
        from bot.account_manager import AccountManager
        import yaml
        
        manager = AccountManager()
        account = manager.get_account(account_id)
        
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        data = request.json
        
        # Fields that can be updated
        updatable_fields = ['name', 'username', 'enabled', 'description']
        updated = False
        
        # Load accounts.yaml
        with open('config/accounts.yaml', 'r') as f:
            accounts_config = yaml.safe_load(f)
        
        # Find and update the account
        for acc in accounts_config['accounts']:
            if acc['id'] == account_id:
                for field in updatable_fields:
                    if field in data:
                        acc[field] = data[field]
                        updated = True
                
                if updated:
                    # Update last_modified timestamp
                    from datetime import datetime
                    acc['last_modified'] = datetime.now().isoformat()
                
                break
        
        if not updated:
            return jsonify({
                'success': False,
                'error': 'No valid fields to update'
            }), 400
        
        # Save accounts.yaml
        with open('config/accounts.yaml', 'w') as f:
            yaml.dump(accounts_config, f, default_flow_style=False, allow_unicode=True)
        
        # Reload account manager
        manager.reload()
        
        # Get updated account
        updated_account = manager.get_account(account_id)
        
        return jsonify({
            'success': True,
            'message': f'Account {account_id} updated successfully',
            'data': updated_account
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/create', methods=['POST'])
def create_account():
    """Create new account"""
    try:
        import os
        import shutil
        from datetime import datetime
        
        data = request.json
        
        # Validate required fields
        account_id = data.get('id')
        name = data.get('name')
        username = data.get('username')
        
        if not account_id or not name or not username:
            return jsonify({
                'success': False, 
                'error': 'Missing required fields: id, name, username'
            }), 400
        
        # Validate account_id format (alphanumeric + underscore only)
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', account_id):
            return jsonify({
                'success': False,
                'error': 'Account ID must be alphanumeric (letters, numbers, underscore only)'
            }), 400
        
        # Check if account already exists
        from bot.account_manager import AccountManager
        manager = AccountManager()
        
        if manager.account_exists(account_id):
            return jsonify({
                'success': False,
                'error': f'Account {account_id} already exists'
            }), 400
        
        # Create folder name: account_id + username (sanitized)
        username_clean = username.replace('@', '').replace(' ', '')
        folder_name = f"{account_id}_{username_clean}"
        folder_path = f"accounts/{folder_name}"
        
        # Check if folder already exists
        if os.path.exists(folder_path):
            return jsonify({
                'success': False,
                'error': f'Folder {folder_path} already exists'
            }), 400
        
        # Create folder structure
        os.makedirs(f"{folder_path}/config", exist_ok=True)
        os.makedirs(f"{folder_path}/data/logs", exist_ok=True)
        os.makedirs(f"{folder_path}/media/promo", exist_ok=True)
        
        # Create .gitkeep in media/promo
        with open(f"{folder_path}/media/promo/.gitkeep", 'w') as f:
            f.write('')
        
        # Copy template configs from account1 or default
        template_source = None
        if os.path.exists("accounts/account1_GrnStore4347/config"):
            template_source = "accounts/account1_GrnStore4347/config"
        elif os.path.exists("config"):
            template_source = "config"
        
        if template_source:
            for config_file in ['settings.yaml', 'templates.yaml', 'keywords.yaml']:
                src = f"{template_source}/{config_file}"
                dst = f"{folder_path}/config/{config_file}"
                if os.path.exists(src):
                    shutil.copy2(src, dst)
        
        # Update settings.yaml with wa_number if provided
        wa_number = data.get('wa_number', '')
        if wa_number:
            import yaml
            settings_path = f"{folder_path}/config/settings.yaml"
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    account_settings = yaml.safe_load(f)
                
                # Update business section
                if 'business' not in account_settings:
                    account_settings['business'] = {}
                
                account_settings['business']['wa_number'] = wa_number
                
                # Generate wa_link if it looks like a phone number
                if wa_number.replace('+', '').replace('-', '').replace(' ', '').isdigit():
                    clean_number = wa_number.replace('+', '').replace('-', '').replace(' ', '')
                    if not clean_number.startswith('62'):
                        if clean_number.startswith('0'):
                            clean_number = '62' + clean_number[1:]
                        else:
                            clean_number = '62' + clean_number
                    account_settings['business']['wa_link'] = f"https://wa.me/{clean_number}?text=Halo%20min%20mau%20order%20kuota%20XL"
                
                # Update account username
                account_settings['account']['username'] = username
                
                with open(settings_path, 'w') as f:
                    yaml.dump(account_settings, f, default_flow_style=False, allow_unicode=True)
        
        # Create placeholder cookies.json
        import json
        placeholder_cookies = {
            "_note": "Add your Twitter session cookies here",
            "cookies": []
        }
        with open(f"{folder_path}/cookies.json", 'w') as f:
            json.dump(placeholder_cookies, f, indent=2)
        
        # Add to accounts.yaml
        new_account = {
            'id': account_id,
            'name': name,
            'username': username,
            'enabled': data.get('enabled', False),  # Default: disabled until cookies added
            'folder': folder_path,
            'description': data.get('description', ''),
            'created_at': datetime.now().isoformat()
        }
        
        # Load and update accounts.yaml
        import yaml
        with open('config/accounts.yaml', 'r') as f:
            accounts_config = yaml.safe_load(f)
        
        accounts_config['accounts'].append(new_account)
        
        with open('config/accounts.yaml', 'w') as f:
            yaml.dump(accounts_config, f, default_flow_style=False, allow_unicode=True)
        
        # Reload account manager
        manager.reload()
        
        return jsonify({
            'success': True,
            'message': f'Account {account_id} created successfully',
            'data': new_account
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= MULTI-ACCOUNT CONCURRENT EXECUTION API =============

@app.route('/api/multi/init', methods=['POST'])
def init_multi_runner():
    """Initialize multi-account runner"""
    global multi_runner
    
    try:
        if multi_runner is None:
            multi_runner = MultiAccountRunner()
            return jsonify({
                'success': True,
                'message': 'Multi-account runner initialized'
            })
        else:
            return jsonify({
                'success': True,
                'message': 'Multi-account runner already initialized'
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/multi/accounts/<account_id>/start', methods=['POST'])
def start_single_account(account_id):
    """Start a single account"""
    global multi_runner
    
    try:
        # Initialize runner if not exists
        if multi_runner is None:
            multi_runner = MultiAccountRunner()
        
        # Run start in background
        def run_start():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(multi_runner.start_account(account_id))
            loop.close()
            return success
        
        thread = threading.Thread(target=run_start, daemon=True)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'Starting account {account_id}...'
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/multi/accounts/<account_id>/stop', methods=['POST'])
def stop_single_account(account_id):
    """Stop a single account"""
    global multi_runner
    
    try:
        if multi_runner is None:
            return jsonify({
                'success': False,
                'error': 'Multi-runner not initialized'
            }), 400
        
        # Run stop in background
        def run_stop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(multi_runner.stop_account(account_id))
            loop.close()
            return success
        
        thread = threading.Thread(target=run_stop, daemon=True)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'Stopping account {account_id}...'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/multi/accounts/<account_id>/restart', methods=['POST'])
def restart_single_account(account_id):
    """Restart a single account"""
    global multi_runner
    
    try:
        if multi_runner is None:
            multi_runner = MultiAccountRunner()
        
        # Run restart in background
        def run_restart():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(multi_runner.restart_account(account_id))
            loop.close()
            return success
        
        thread = threading.Thread(target=run_restart, daemon=True)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'Restarting account {account_id}...'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/multi/start-all', methods=['POST'])
def start_all_accounts():
    """Start all enabled accounts"""
    global multi_runner
    
    try:
        if multi_runner is None:
            multi_runner = MultiAccountRunner()
        
        # Run start-all in background
        def run_start_all():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(multi_runner.start_all())
            loop.close()
            return results
        
        thread = threading.Thread(target=run_start_all, daemon=True)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Starting all enabled accounts...'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/multi/stop-all', methods=['POST'])
def stop_all_accounts():
    """Stop all running accounts"""
    global multi_runner
    
    try:
        if multi_runner is None:
            return jsonify({
                'success': False,
                'error': 'Multi-runner not initialized'
            }), 400
        
        # Run stop-all in background
        def run_stop_all():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(multi_runner.stop_all())
            loop.close()
            return results
        
        thread = threading.Thread(target=run_stop_all, daemon=True)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Stopping all accounts...'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/multi/status')
def get_multi_status():
    """Get status of all accounts"""
    global multi_runner
    
    try:
        if multi_runner is None:
            # Return idle status for all accounts
            from bot.account_manager import AccountManager
            manager = AccountManager()
            accounts = manager.get_all_accounts()
            
            statuses = {}
            for account in accounts:
                statuses[account['id']] = {
                    'account_id': account['id'],
                    'name': account['name'],
                    'username': account['username'],
                    'status': 'idle',
                    'enabled': account.get('enabled', False)
                }
            
            return jsonify({
                'success': True,
                'data': {
                    'initialized': False,
                    'total_accounts': len(accounts),
                    'running_accounts': 0,
                    'statuses': statuses
                }
            })
        
        summary = multi_runner.get_summary()
        
        return jsonify({
            'success': True,
            'data': {
                'initialized': True,
                **summary
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/multi/accounts/<account_id>/status')
def get_account_run_status(account_id):
    """Get detailed status of a specific account"""
    global multi_runner
    
    try:
        if multi_runner is None:
            return jsonify({
                'success': False,
                'error': 'Multi-runner not initialized'
            }), 400
        
        status = multi_runner.get_account_status(account_id)
        
        if status is None:
            return jsonify({
                'success': False,
                'error': 'Account not found or never started'
            }), 404
        
        # Add recent errors
        errors = multi_runner.get_errors(account_id)
        status['recent_errors'] = errors
        
        return jsonify({
            'success': True,
            'data': status
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>/cookies/upload', methods=['POST'])
def upload_cookies(account_id):
    """Upload and validate cookies for an account"""
    try:
        from bot.account_manager import AccountManager
        from twikit import Client
        import json
        
        # Get account
        manager = AccountManager()
        account = manager.get_account(account_id)
        
        if not account:
            return jsonify({
                'success': False,
                'error': f'Account {account_id} not found'
            }), 404
        
        # Get cookies from request
        data = request.get_json()
        
        if not data or 'cookies' not in data:
            return jsonify({
                'success': False,
                'error': 'No cookies data provided'
            }), 400
        
        cookies_data = data['cookies']
        
        # Parse cookies if it's a string
        if isinstance(cookies_data, str):
            try:
                cookies_data = json.loads(cookies_data)
            except json.JSONDecodeError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid JSON format for cookies'
                }), 400
        
        # Convert browser cookies format to twikit format if needed
        # Browser format: [{name, value, ...}, ...] or {name: {value, ...}, ...}
        # Twikit format: {name: value, ...}
        if isinstance(cookies_data, list):
            # Array format from browser extension
            converted = {}
            for cookie in cookies_data:
                if isinstance(cookie, dict) and 'name' in cookie and 'value' in cookie:
                    converted[cookie['name']] = cookie['value']
            cookies_data = converted
        elif isinstance(cookies_data, dict):
            # Check if it's already simple dict format
            if not all(isinstance(v, str) for v in cookies_data.values()):
                # Complex dict format, convert
                converted = {}
                for key, val in cookies_data.items():
                    if isinstance(val, dict) and 'value' in val:
                        converted[key] = val['value']
                    elif isinstance(val, str):
                        converted[key] = val
                cookies_data = converted
        
        # Validate cookies has required fields
        required_fields = ['ct0', 'auth_token']
        missing_fields = [f for f in required_fields if f not in cookies_data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required cookie fields: {", ".join(missing_fields)}'
            }), 400
        
        # Save cookies to temporary file for validation
        import tempfile
        temp_cookies = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(cookies_data, temp_cookies)
        temp_cookies.close()
        
        # Validate cookies by trying to authenticate
        try:
            client = Client('en-US')
            client.load_cookies(temp_cookies.name)
            
            # Try to get user info to validate
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def validate():
                try:
                    user = await client.user()
                    return {
                        'valid': True,
                        'username': user.screen_name,
                        'name': user.name,
                        'followers': user.followers_count,
                        'following': user.following_count
                    }
                except Exception as e:
                    return {
                        'valid': False,
                        'error': str(e)
                    }
            
            result = loop.run_until_complete(validate())
            loop.close()
            
            # Clean up temp file
            import os
            os.unlink(temp_cookies.name)
            
            if not result['valid']:
                return jsonify({
                    'success': False,
                    'error': f'Invalid cookies: {result.get("error", "Authentication failed")}'
                }), 400
            
            # Cookies are valid, save to account folder
            cookies_file = Path(account['folder']) / 'cookies.json'
            
            with open(cookies_file, 'w') as f:
                json.dump(cookies_data, f, indent=2)
            
            return jsonify({
                'success': True,
                'message': 'Cookies uploaded and validated successfully',
                'account_info': {
                    'username': result['username'],
                    'name': result['name'],
                    'followers': result['followers'],
                    'following': result['following']
                }
            })
            
        except Exception as e:
            # Clean up temp file
            import os
            try:
                os.unlink(temp_cookies.name)
            except:
                pass
            
            return jsonify({
                'success': False,
                'error': f'Validation failed: {str(e)}'
            }), 400
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>/config/templates', methods=['GET'])
def get_account_templates(account_id):
    """Get templates for a specific account"""
    try:
        from bot.account_manager import AccountManager
        import yaml
        
        # Get account
        manager = AccountManager()
        account = manager.get_account(account_id)
        
        if not account:
            return jsonify({
                'success': False,
                'error': f'Account {account_id} not found'
            }), 404
        
        # Load templates
        templates_file = Path(account['folder']) / 'config' / 'templates.yaml'
        
        if not templates_file.exists():
            return jsonify({
                'success': False,
                'error': 'Templates file not found'
            }), 404
        
        with open(templates_file, 'r', encoding='utf-8') as f:
            templates = yaml.safe_load(f)
        
        return jsonify({
            'success': True,
            'data': templates
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>/config/templates', methods=['PUT'])
def update_account_templates(account_id):
    """Update templates for a specific account"""
    try:
        from bot.account_manager import AccountManager
        import yaml
        from datetime import datetime
        
        # Get account
        manager = AccountManager()
        account = manager.get_account(account_id)
        
        if not account:
            return jsonify({
                'success': False,
                'error': f'Account {account_id} not found'
            }), 404
        
        # Get new templates data
        data = request.get_json()
        
        if not data or 'templates' not in data:
            return jsonify({
                'success': False,
                'error': 'No templates data provided'
            }), 400
        
        templates = data['templates']
        
        # Backup existing templates
        templates_file = Path(account['folder']) / 'config' / 'templates.yaml'
        backup_file = Path(account['folder']) / 'config' / f'templates.yaml.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        
        if templates_file.exists():
            import shutil
            shutil.copy2(templates_file, backup_file)
        
        # Save new templates
        with open(templates_file, 'w', encoding='utf-8') as f:
            yaml.dump(templates, f, allow_unicode=True, default_flow_style=False)
        
        return jsonify({
            'success': True,
            'message': 'Templates updated successfully',
            'backup': str(backup_file)
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>/media', methods=['GET'])
def get_account_media(account_id):
    """Get media files for a specific account"""
    try:
        from bot.account_manager import AccountManager
        import os
        
        # Get account
        manager = AccountManager()
        account = manager.get_account(account_id)
        
        if not account:
            return jsonify({
                'success': False,
                'error': f'Account {account_id} not found'
            }), 404
        
        # Get media files
        media_folder = Path(account['folder']) / 'media' / 'promo'
        
        if not media_folder.exists():
            media_folder.mkdir(parents=True, exist_ok=True)
        
        media_files = []
        for file in media_folder.iterdir():
            if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.mp4']:
                media_files.append({
                    'name': file.name,
                    'path': f'media/promo/{file.name}',
                    'size': file.stat().st_size,
                    'modified': datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                })
        
        return jsonify({
            'success': True,
            'data': {
                'media_files': media_files,
                'count': len(media_files),
                'folder': str(media_folder)
            }
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>/media/upload', methods=['POST'])
def upload_account_media(account_id):
    """Upload media file for a specific account"""
    try:
        from bot.account_manager import AccountManager
        import os
        
        # Get account
        manager = AccountManager()
        account = manager.get_account(account_id)
        
        if not account:
            return jsonify({
                'success': False,
                'error': f'Account {account_id} not found'
            }), 404
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Validate file extension
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.mp4'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Allowed: {", ".join(allowed_extensions)}'
            }), 400
        
        # Save file
        media_folder = Path(account['folder']) / 'media' / 'promo'
        media_folder.mkdir(parents=True, exist_ok=True)
        
        file_path = media_folder / file.filename
        file.save(str(file_path))
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully',
            'file': {
                'name': file.filename,
                'path': f'media/promo/{file.filename}',
                'size': file_path.stat().st_size
            }
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>/media/<filename>', methods=['DELETE'])
def delete_account_media(account_id, filename):
    """Delete media file from a specific account"""
    try:
        from bot.account_manager import AccountManager
        
        # Get account
        manager = AccountManager()
        account = manager.get_account(account_id)
        
        if not account:
            return jsonify({
                'success': False,
                'error': f'Account {account_id} not found'
            }), 404
        
        # Delete file
        media_folder = Path(account['folder']) / 'media' / 'promo'
        file_path = media_folder / filename
        
        if not file_path.exists():
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        # Backup before delete
        backup_folder = Path(account['folder']) / 'media' / 'backup'
        backup_folder.mkdir(parents=True, exist_ok=True)
        
        import shutil
        backup_path = backup_folder / f'{filename}.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        shutil.copy2(file_path, backup_path)
        
        # Delete original
        file_path.unlink()
        
        return jsonify({
            'success': True,
            'message': 'File deleted successfully',
            'backup': str(backup_path)
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>/cookies/test', methods=['POST'])
def test_cookies(account_id):
    """Test if account cookies are valid"""
    try:
        from bot.account_manager import AccountManager
        from bot.automation import BotAutomation
        
        # Get account
        manager = AccountManager()
        account = manager.get_account(account_id)
        
        if not account:
            return jsonify({
                'success': False,
                'error': f'Account {account_id} not found'
            }), 404
        
        # Check cookies file exists
        cookies_file = Path(account['folder']) / 'cookies.json'
        
        if not cookies_file.exists():
            return jsonify({
                'success': False,
                'error': 'Cookies file not found. Please upload cookies first.'
            }), 404
        
        # Test connection
        def test():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def run_test():
                bot = BotAutomation(account_folder=account['folder'])
                success = await bot.initialize()
                
                if success:
                    user_info = {
                        'username': bot.twitter.me.screen_name,
                        'name': bot.twitter.me.name,
                        'followers': bot.twitter.me.followers_count,
                        'following': bot.twitter.me.following_count
                    }
                    await bot.cleanup()
                    return {'valid': True, 'user_info': user_info}
                else:
                    await bot.cleanup()
                    return {'valid': False, 'error': 'Authentication failed'}
            
            result = loop.run_until_complete(run_test())
            loop.close()
            return result
        
        result = test()
        
        if result['valid']:
            return jsonify({
                'success': True,
                'message': 'Cookies are valid',
                'account_info': result['user_info']
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Authentication failed')
            }), 400
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    dashboard_config = settings['dashboard']
    
    print("="*60)
    print("🚀 Twitter Bot Dashboard Starting...")
    print("="*60)
    print(f"📊 Dashboard URL: http://{dashboard_config['host']}:{dashboard_config['port']}")
    print(f"⚙️  Debug mode: {dashboard_config['debug']}")
    print("="*60)
    print("\nPress Ctrl+C to stop\n")
    
    app.run(
        host=dashboard_config['host'],
        port=dashboard_config['port'],
        debug=dashboard_config['debug']
    )
