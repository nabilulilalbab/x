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

from bot.database import Database
from bot.config_loader import ConfigLoader
from bot.automation import BotAutomation

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

# Load config
settings = config.get_settings()
app.config['SECRET_KEY'] = settings['dashboard']['secret_key']


# ============= ROUTES =============

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


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
                'bot_running': bot is not None and bot.is_running
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/activity/today')
def get_today_activity():
    """Get today's activity"""
    try:
        activity = db.get_daily_activity()
        return jsonify({'success': True, 'data': activity})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/tweets/recent')
def get_recent_tweets():
    """Get recent tweets with stats"""
    try:
        limit = request.args.get('limit', 10, type=int)
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
        days = request.args.get('days', 30, type=int)
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
        days = request.args.get('days', 7, type=int)
        keywords = db.get_keyword_performance(days)
        return jsonify({'success': True, 'data': keywords})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/logs')
def get_logs():
    """Get recent activity logs"""
    try:
        limit = request.args.get('limit', 50, type=int)
        logs = db.get_recent_logs(limit)
        return jsonify({'success': True, 'data': logs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/config')
def get_config():
    """Get current configuration"""
    try:
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
        
        new_settings = request.json
        
        # Save to file
        with open('config/settings.yaml', 'w') as f:
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
        
        new_templates = request.json
        
        # Save to file
        with open('config/templates.yaml', 'w') as f:
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
        
        temp_bot = BotAutomation()
        
        def run():
            asyncio.run(temp_bot.run_once(slot))
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        
        return jsonify({'success': True, 'message': f'Running {slot} slot'})
    except Exception as e:
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
