"""
Twitter Bot Dashboard V2
Clean, modern dashboard with native multi-account support
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
from pathlib import Path
import logging
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Import bot modules
from bot.account_manager import AccountManager
from bot.database import Database
from bot.config_loader import ConfigLoader
from bot.multi_account_runner import MultiAccountRunner

# Initialize account manager
account_manager = AccountManager()

# Initialize multi-account runner
multi_runner = None
runner_threads = {}  # Store thread references to keep them alive

def get_multi_runner():
    """Get or create multi-account runner instance"""
    global multi_runner
    if multi_runner is None:
        multi_runner = MultiAccountRunner()
    return multi_runner

# ============= UTILITY FUNCTIONS =============

def get_account_database(account_id):
    """Get database for specific account"""
    account = account_manager.get_account(account_id)
    if not account:
        return None
    
    db_path = f"{account['folder']}/data/metrics.db"
    return Database(db_path=db_path)

def get_account_config(account_id):
    """Get config loader for specific account"""
    account = account_manager.get_account(account_id)
    if not account:
        return None
    
    config_dir = f"{account['folder']}/config"
    return ConfigLoader(config_dir=config_dir)

# ============= MAIN ROUTES =============

@app.route('/')
def index():
    """Serve dashboard V2"""
    return render_template('dashboard_v2.html')

@app.route('/api/v2/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'version': '2.0',
        'accounts': len(account_manager.get_all_accounts())
    })

# ============= ACCOUNT MANAGEMENT =============

@app.route('/api/v2/accounts')
def list_accounts():
    """List all accounts"""
    try:
        import yaml
        import os
        
        accounts = account_manager.get_all_accounts()
        
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
                'total': len(accounts),
                'enabled': len(account_manager.get_enabled_accounts())
            }
        })
    except Exception as e:
        logger.error(f"Error listing accounts: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/accounts/<account_id>')
def get_account(account_id):
    """Get specific account details"""
    try:
        import yaml
        import os
        
        account = account_manager.get_account(account_id)
        
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        # Check if folder exists
        folder_exists = Path(account['folder']).exists()
        
        # Check if cookies exist
        cookies_exist = Path(f"{account['folder']}/cookies.json").exists()
        
        # Get WA number from settings
        folder = account.get('folder')
        wa_number = ''
        wa_link = ''
        if folder and os.path.exists(f"{folder}/config/settings.yaml"):
            try:
                with open(f"{folder}/config/settings.yaml", 'r') as f:
                    account_settings = yaml.safe_load(f)
                    business = account_settings.get('business', {})
                    wa_number = business.get('wa_number', '')
                    wa_link = business.get('wa_link', '')
            except:
                pass
        
        return jsonify({
            'success': True,
            'data': {
                **account,
                'folder_exists': folder_exists,
                'cookies_exist': cookies_exist,
                'wa_number': wa_number,
                'wa_link': wa_link
            }
        })
    except Exception as e:
        logger.error(f"Error getting account {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============= STATISTICS =============

@app.route('/api/v2/stats/<account_id>')
def get_stats(account_id):
    """Get statistics for specific account"""
    try:
        # Validate account
        account = account_manager.get_account(account_id)
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        # Get database
        db = get_account_database(account_id)
        if not db:
            return jsonify({'success': False, 'error': 'Database not found'}), 404
        
        # Get stats
        stats = db.get_dashboard_stats()
        
        return jsonify({
            'success': True,
            'account_id': account_id,
            'account_name': account['name'],
            'data': stats
        })
    except Exception as e:
        logger.error(f"Error getting stats for {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/tweets/<account_id>')
def get_tweets(account_id):
    """Get recent tweets for specific account"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Validate account
        account = account_manager.get_account(account_id)
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        # Get database
        db = get_account_database(account_id)
        if not db:
            return jsonify({'success': False, 'error': 'Database not found'}), 404
        
        # Get tweets
        tweets = db.get_recent_tweets(limit)
        
        return jsonify({
            'success': True,
            'account_id': account_id,
            'data': tweets
        })
    except Exception as e:
        logger.error(f"Error getting tweets for {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/logs/<account_id>')
def get_logs(account_id):
    """Get activity logs for specific account"""
    try:
        limit = request.args.get('limit', 20, type=int)
        
        # Validate account
        account = account_manager.get_account(account_id)
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        # Get database
        db = get_account_database(account_id)
        if not db:
            return jsonify({'success': False, 'error': 'Database not found'}), 404
        
        # Get logs
        logs = db.get_recent_logs(limit)
        
        return jsonify({
            'success': True,
            'account_id': account_id,
            'data': logs
        })
    except Exception as e:
        logger.error(f"Error getting logs for {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/keywords/<account_id>')
def get_keywords(account_id):
    """Get keyword performance for specific account"""
    try:
        days = request.args.get('days', 7, type=int)
        
        # Validate account
        account = account_manager.get_account(account_id)
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        # Get database
        db = get_account_database(account_id)
        if not db:
            return jsonify({'success': False, 'error': 'Database not found'}), 404
        
        # Get keywords
        keywords = db.get_keyword_performance(days)
        
        return jsonify({
            'success': True,
            'account_id': account_id,
            'data': keywords
        })
    except Exception as e:
        logger.error(f"Error getting keywords for {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============= CONFIGURATION =============

@app.route('/api/v2/config/<account_id>')
def get_config(account_id):
    """Get configuration for specific account"""
    try:
        # Validate account
        account = account_manager.get_account(account_id)
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        # Get config loader
        config = get_account_config(account_id)
        if not config:
            return jsonify({'success': False, 'error': 'Config not found'}), 404
        
        # Get all config
        return jsonify({
            'success': True,
            'account_id': account_id,
            'data': {
                'settings': config.get_settings(),
                'templates': config.get_templates(),
                'keywords': config.get_keywords()
            }
        })
    except Exception as e:
        logger.error(f"Error getting config for {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/config/<account_id>/settings', methods=['POST'])
def update_settings(account_id):
    """Update settings for specific account"""
    try:
        import yaml
        
        # Validate account
        account = account_manager.get_account(account_id)
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        # Get new settings
        new_settings = request.json
        
        # Save to file
        settings_file = f"{account['folder']}/config/settings.yaml"
        with open(settings_file, 'w') as f:
            yaml.dump(new_settings, f, default_flow_style=False, allow_unicode=True)
        
        return jsonify({
            'success': True,
            'message': f'Settings updated for {account["name"]}'
        })
    except Exception as e:
        logger.error(f"Error updating settings for {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/config/<account_id>/templates', methods=['POST'])
def update_templates(account_id):
    """Update templates for specific account"""
    try:
        import yaml
        
        # Validate account
        account = account_manager.get_account(account_id)
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        # Get new templates
        new_templates = request.json
        
        # Save to file
        templates_file = f"{account['folder']}/config/templates.yaml"
        with open(templates_file, 'w') as f:
            yaml.dump(new_templates, f, default_flow_style=False, allow_unicode=True)
        
        return jsonify({
            'success': True,
            'message': f'Templates updated for {account["name"]}'
        })
    except Exception as e:
        logger.error(f"Error updating templates for {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/config/<account_id>/keywords', methods=['POST'])
def update_keywords(account_id):
    """Update keywords for specific account"""
    try:
        import yaml
        
        # Validate account
        account = account_manager.get_account(account_id)
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        # Get new keywords
        new_keywords = request.json
        
        # Save to file
        keywords_file = f"{account['folder']}/config/keywords.yaml"
        with open(keywords_file, 'w') as f:
            yaml.dump(new_keywords, f, default_flow_style=False, allow_unicode=True)
        
        return jsonify({
            'success': True,
            'message': f'Keywords updated for {account["name"]}'
        })
    except Exception as e:
        logger.error(f"Error updating keywords for {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============= MANUAL ACTIONS =============

@app.route('/api/v2/conversions/<account_id>', methods=['GET'])
def get_conversions(account_id):
    """Get conversions for specific account"""
    try:
        days = request.args.get('days', 7, type=int)
        
        # Validate account
        account = account_manager.get_account(account_id)
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        # Get database
        db = get_account_database(account_id)
        if not db:
            return jsonify({'success': False, 'error': 'Database not found'}), 404
        
        # Get conversions
        conversions = db.get_conversions(days)
        
        return jsonify({
            'success': True,
            'account_id': account_id,
            'data': conversions
        })
    except Exception as e:
        logger.error(f"Error getting conversions for {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/conversions/<account_id>/add', methods=['POST'])
def add_conversion(account_id):
    """Add conversion for specific account"""
    try:
        # Validate account
        account = account_manager.get_account(account_id)
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        # Get database
        db = get_account_database(account_id)
        if not db:
            return jsonify({'success': False, 'error': 'Database not found'}), 404
        
        # Get conversion data
        data = request.json
        
        # Add conversion
        db.log_conversion(
            source=data.get('source', 'twitter'),
            wa_messages=data.get('wa_messages', 1),
            confirmed_orders=data.get('confirmed_orders', 1),
            revenue=data.get('revenue', 0)
        )
        
        return jsonify({
            'success': True,
            'message': f'Conversion added for {account["name"]}'
        })
    except Exception as e:
        logger.error(f"Error adding conversion for {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============= MULTI-ACCOUNT CONTROL =============

@app.route('/api/v2/multi/status')
def get_multi_status():
    """Get multi-account runner status"""
    try:
        runner = get_multi_runner()
        summary = runner.get_summary()
        
        return jsonify({
            'success': True,
            'data': summary
        })
    except Exception as e:
        logger.error(f"Error getting multi status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/multi/start-all', methods=['POST'])
def start_all_accounts():
    """Start all enabled accounts"""
    try:
        import asyncio
        import threading
        
        global runner_threads
        runner = get_multi_runner()
        
        def run_start_all():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(runner.start_all())
            loop.close()
        
        thread = threading.Thread(target=run_start_all, daemon=False)
        thread.start()
        runner_threads['start_all'] = thread  # Keep reference
        
        return jsonify({
            'success': True,
            'message': 'Starting all enabled accounts...'
        })
    except Exception as e:
        logger.error(f"Error starting all accounts: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/multi/stop-all', methods=['POST'])
def stop_all_accounts():
    """Stop all running accounts"""
    try:
        import asyncio
        import threading
        
        global runner_threads
        runner = get_multi_runner()
        
        def run_stop_all():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(runner.stop_all())
            loop.close()
        
        thread = threading.Thread(target=run_stop_all, daemon=False)
        thread.start()
        runner_threads['stop_all'] = thread  # Keep reference
        
        return jsonify({
            'success': True,
            'message': 'Stopping all accounts...'
        })
    except Exception as e:
        logger.error(f"Error stopping all accounts: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/multi/accounts/<account_id>/start', methods=['POST'])
def start_account(account_id):
    """Start specific account"""
    try:
        import asyncio
        import threading
        
        global runner_threads
        runner = get_multi_runner()
        
        def run_start():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(runner.start_account(account_id))
            loop.close()
        
        thread = threading.Thread(target=run_start, daemon=False)
        thread.start()
        runner_threads[f'start_{account_id}'] = thread  # Keep reference
        
        return jsonify({
            'success': True,
            'message': f'Starting account {account_id}...'
        })
    except Exception as e:
        logger.error(f"Error starting account {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/multi/accounts/<account_id>/stop', methods=['POST'])
def stop_account(account_id):
    """Stop specific account"""
    try:
        import asyncio
        import threading
        
        global runner_threads
        runner = get_multi_runner()
        
        def run_stop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(runner.stop_account(account_id))
            loop.close()
        
        thread = threading.Thread(target=run_stop, daemon=False)
        thread.start()
        runner_threads[f'stop_{account_id}'] = thread  # Keep reference
        
        return jsonify({
            'success': True,
            'message': f'Stopping account {account_id}...'
        })
    except Exception as e:
        logger.error(f"Error stopping account {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/multi/accounts/<account_id>/restart', methods=['POST'])
def restart_account(account_id):
    """Restart specific account"""
    try:
        import asyncio
        import threading
        
        global runner_threads
        runner = get_multi_runner()
        
        def run_restart():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(runner.restart_account(account_id))
            loop.close()
        
        thread = threading.Thread(target=run_restart, daemon=False)
        thread.start()
        runner_threads[f'restart_{account_id}'] = thread  # Keep reference
        
        return jsonify({
            'success': True,
            'message': f'Restarting account {account_id}...'
        })
    except Exception as e:
        logger.error(f"Error restarting account {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============= MEDIA MANAGEMENT =============

@app.route('/accounts/<account_id>/media/promo/<filename>')
def serve_account_media(account_id, filename):
    """Serve media file for preview"""
    try:
        account = account_manager.get_account(account_id)
        if not account:
            return "Account not found", 404
        
        from pathlib import Path
        media_path = Path(account['folder']) / 'media' / 'promo' / filename
        
        if not media_path.exists():
            return "File not found", 404
        
        from flask import send_file
        return send_file(str(media_path))
    except Exception as e:
        logger.error(f"Error serving media: {e}")
        return str(e), 500

@app.route('/api/v2/accounts/<account_id>/media')
def get_account_media(account_id):
    """Get media files for specific account"""
    try:
        account = account_manager.get_account(account_id)
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        import os
        from pathlib import Path
        
        media_folder = Path(account['folder']) / 'media' / 'promo'
        media_folder.mkdir(parents=True, exist_ok=True)
        
        media_files = []
        for file in media_folder.iterdir():
            if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.mp4']:
                media_files.append({
                    'name': file.name,
                    'path': f'media/promo/{file.name}',
                    'url': f'/accounts/{account_id}/media/promo/{file.name}',
                    'size': file.stat().st_size,
                    'type': 'video' if file.suffix.lower() == '.mp4' else 'image'
                })
        
        return jsonify({
            'success': True,
            'data': {
                'media_files': media_files,
                'count': len(media_files)
            }
        })
    except Exception as e:
        logger.error(f"Error getting account media: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/accounts/<account_id>/media/upload', methods=['POST'])
def upload_account_media(account_id):
    """Upload media file for specific account"""
    try:
        account = account_manager.get_account(account_id)
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Validate extension
        import os
        from pathlib import Path
        allowed = {'.jpg', '.jpeg', '.png', '.gif', '.mp4'}
        ext = os.path.splitext(file.filename)[1].lower()
        
        if ext not in allowed:
            return jsonify({'success': False, 'error': f'Invalid file type. Allowed: {", ".join(allowed)}'}), 400
        
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
                'path': f'media/promo/{file.filename}'
            }
        })
    except Exception as e:
        logger.error(f"Error uploading media: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v2/accounts/<account_id>/templates/assign-media', methods=['POST'])
def assign_media_to_template(account_id):
    """Assign media to promo template for specific account"""
    try:
        account = account_manager.get_account(account_id)
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        import yaml
        from pathlib import Path
        
        data = request.json
        template_index = data.get('template_index')
        media_file = data.get('media_file')  # filename or null
        
        # Load account templates
        templates_file = Path(account['folder']) / 'config' / 'templates.yaml'
        with open(templates_file, 'r') as f:
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
            with open(templates_file, 'w') as f:
                yaml.dump(templates, f, default_flow_style=False, allow_unicode=True)
            
            return jsonify({'success': True, 'message': 'Media assigned to template'})
        else:
            return jsonify({'success': False, 'error': 'Invalid template index'}), 400
    except Exception as e:
        logger.error(f"Error assigning media: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============= ACTIONS =============

@app.route('/api/v2/actions/<account_id>/run-slot', methods=['POST'])
def run_slot(account_id):
    """Run manual slot for specific account"""
    try:
        import asyncio
        import threading
        from bot.automation import BotAutomation
        
        # Validate account
        account = account_manager.get_account(account_id)
        if not account:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        # Get slot name
        data = request.json
        slot = data.get('slot', 'morning')
        
        # Create bot instance for this account
        bot = BotAutomation(account_folder=account['folder'])
        
        # Run in background
        def run():
            asyncio.run(bot.run_once(slot))
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'Running {slot} slot for {account["name"]}'
        })
    except Exception as e:
        logger.error(f"Error running slot for {account_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============= STATIC FILES =============

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'success': False, 'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {error}")
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# ============= MAIN =============

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Twitter Bot Dashboard V2 Starting...")
    print("=" * 60)
    print("📊 Dashboard URL: http://0.0.0.0:5001")
    print("⚙️  Debug mode: False")
    print("=" * 60)
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5001, debug=False)
