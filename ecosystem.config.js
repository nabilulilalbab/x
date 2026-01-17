/**
 * PM2 Ecosystem Configuration
 * Twitter Bot - Kuota XL Automation
 * 
 * Usage:
 *   pm2 start ecosystem.config.js
 *   pm2 stop all
 *   pm2 restart all
 *   pm2 logs
 */

module.exports = {
  apps: [
    // ==========================================
    // 1. Dashboard V1 - Multi-Account Manager
    // ==========================================
    {
      name: 'twitter-bot-dashboard',
      script: 'dashboard.py',
      interpreter: 'python3',
      cwd: './',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        FLASK_ENV: 'production',
        PORT: 5000
      },
      error_file: 'data/logs/pm2-dashboard-error.log',
      out_file: 'data/logs/pm2-dashboard-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      time: true
    },

    // ==========================================
    // 2. Dashboard V2 - Per-Account View
    // ==========================================
    {
      name: 'twitter-bot-dashboard-v2',
      script: 'dashboard_v2.py',
      interpreter: 'python3',
      cwd: './',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        FLASK_ENV: 'production',
        PORT: 5001
      },
      error_file: 'data/logs/pm2-dashboard-v2-error.log',
      out_file: 'data/logs/pm2-dashboard-v2-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      time: true
    },

    // ==========================================
    // 3. Bot Runner - Multi-Account Mode
    // ==========================================
    {
      name: 'twitter-bot-runner',
      script: 'bot/multi_account_runner.py',
      interpreter: 'python3',
      cwd: './',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      restart_delay: 5000,
      max_restarts: 10,
      min_uptime: '10s',
      error_file: 'data/logs/pm2-bot-runner-error.log',
      out_file: 'data/logs/pm2-bot-runner-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      time: true,
      // Restart at 3 AM daily (optional - for fresh start)
      cron_restart: '0 3 * * *',
      // Environment variables
      env: {
        PYTHONUNBUFFERED: '1',
        TZ: 'Asia/Jakarta'
      }
    },

    // ==========================================
    // OPTIONAL: Individual Account Runners
    // Uncomment if you want to run accounts separately
    // ==========================================
    /*
    {
      name: 'twitter-bot-account1',
      script: 'main.py',
      interpreter: 'python3',
      args: '--daemon --account account1',
      cwd: './',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      error_file: 'accounts/account1_GrnStore4347/data/logs/pm2-error.log',
      out_file: 'accounts/account1_GrnStore4347/data/logs/pm2-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      time: true
    },
    {
      name: 'twitter-bot-account2',
      script: 'main.py',
      interpreter: 'python3',
      args: '--daemon --account account2',
      cwd: './',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      error_file: 'accounts/account2_KorteksL43042/data/logs/pm2-error.log',
      out_file: 'accounts/account2_KorteksL43042/data/logs/pm2-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      time: true
    }
    */
  ]
};
