# 🚀 PM2 DEPLOYMENT GUIDE - Twitter Bot

Panduan lengkap deploy Twitter Bot ke PM2 untuk production environment.

---

## 📋 Prerequisites

### 1. Install PM2
```bash
# Install PM2 globally
npm install -g pm2

# Verify installation
pm2 --version
```

### 2. Install Python Dependencies
```bash
# Pastikan Python 3.x sudah terinstall
python3 --version

# Install dependencies
pip3 install -r requirements.txt

# Atau pakai virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 3. Setup Directories
```bash
# Buat log directories
mkdir -p data/logs
mkdir -p accounts/account1_GrnStore4347/data/logs
mkdir -p accounts/account2_KorteksL43042/data/logs

# Set permissions (optional, for production server)
chmod 755 data/logs
```

---

## 🎯 Deployment Modes

### **Mode 1: Multi-Account Runner (Recommended)**
Run semua accounts dalam 1 process dengan concurrent execution.

### **Mode 2: Individual Account Runners**
Run tiap account sebagai process terpisah (lebih isolated).

---

## 🚀 Quick Start

### 1. Start All Services
```bash
# Start semua services (dashboard + bot runner)
pm2 start ecosystem.config.js

# Check status
pm2 status
```

Expected output:
```
┌─────┬───────────────────────────────┬─────────┬─────────┬─────────┐
│ id  │ name                          │ status  │ restart │ uptime  │
├─────┼───────────────────────────────┼─────────┼─────────┼─────────┤
│ 0   │ twitter-bot-dashboard         │ online  │ 0       │ 10s     │
│ 1   │ twitter-bot-dashboard-v2      │ online  │ 0       │ 10s     │
│ 2   │ twitter-bot-runner            │ online  │ 0       │ 10s     │
└─────┴───────────────────────────────┴─────────┴─────────┴─────────┘
```

### 2. Access Dashboards
```bash
# Dashboard V1 (Multi-Account Manager)
http://localhost:5000

# Dashboard V2 (Per-Account View)
http://localhost:5001
```

---

## 📊 PM2 Management Commands

### Basic Commands
```bash
# List all processes
pm2 list
pm2 ls

# View logs (real-time)
pm2 logs                              # All processes
pm2 logs twitter-bot-runner           # Specific process
pm2 logs --lines 100                  # Last 100 lines

# Monitor resources
pm2 monit                             # Real-time monitoring

# Process info
pm2 info twitter-bot-runner           # Detailed info
pm2 describe twitter-bot-runner       # Same as info
```

### Start/Stop/Restart
```bash
# Start
pm2 start ecosystem.config.js         # Start all
pm2 start twitter-bot-runner          # Start specific

# Stop
pm2 stop all                          # Stop all
pm2 stop twitter-bot-runner           # Stop specific
pm2 stop 0                            # Stop by ID

# Restart
pm2 restart all                       # Restart all
pm2 restart twitter-bot-runner        # Restart specific

# Reload (zero-downtime restart)
pm2 reload all

# Delete (remove from PM2)
pm2 delete all                        # Delete all
pm2 delete twitter-bot-runner         # Delete specific
```

### Logs Management
```bash
# View logs
pm2 logs --lines 200                  # Last 200 lines
pm2 logs --err                        # Error logs only
pm2 logs --out                        # Output logs only

# Flush logs (clear)
pm2 flush

# Rotate logs (archive old logs)
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7
```

---

## 🔧 Configuration Options

### Modify `ecosystem.config.js`

#### 1. Change Memory Limit
```javascript
max_memory_restart: '1G'  // Restart if exceed 1GB
```

#### 2. Enable Watch Mode (auto-restart on file change)
```javascript
watch: true,
watch_delay: 1000,
ignore_watch: ['node_modules', 'logs', '*.log']
```

#### 3. Schedule Restart (Cron)
```javascript
cron_restart: '0 3 * * *'  // Restart at 3 AM daily
```

#### 4. Environment Variables
```javascript
env: {
  NODE_ENV: 'production',
  PORT: 5000,
  PYTHONUNBUFFERED: '1'
}
```

#### 5. Error Handling
```javascript
max_restarts: 10,          // Max restart attempts
min_uptime: '10s',         // Min uptime before restart
restart_delay: 5000        // Delay between restarts (ms)
```

---

## 🎯 Production Best Practices

### 1. Auto-Start on Boot
```bash
# Save PM2 process list
pm2 save

# Generate startup script
pm2 startup

# Output will be something like:
# sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u youruser --hp /home/youruser

# Run the output command
sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u $USER --hp $HOME

# Test reboot
sudo reboot
```

### 2. Monitor with PM2 Plus (Optional)
```bash
# Create account at pm2.io
pm2 link <secret_key> <public_key>

# Now you can monitor via web: https://app.pm2.io
```

### 3. Setup Log Rotation
```bash
# Install pm2-logrotate
pm2 install pm2-logrotate

# Configure
pm2 set pm2-logrotate:max_size 10M        # Max size per log file
pm2 set pm2-logrotate:retain 7            # Keep 7 rotated files
pm2 set pm2-logrotate:compress true       # Compress rotated files
pm2 set pm2-logrotate:rotateInterval '0 0 * * *'  # Daily at midnight
```

### 4. Setup Process File Watcher
```bash
# Watch for crashes and auto-restart
pm2 startup
pm2 save
```

---

## 🔍 Troubleshooting

### Issue 1: Process Keeps Restarting
```bash
# Check error logs
pm2 logs twitter-bot-runner --err --lines 100

# Check why it's restarting
pm2 describe twitter-bot-runner

# Common causes:
# - Missing dependencies (check requirements.txt)
# - Missing config files (settings.yaml, cookies.json)
# - Python version mismatch
# - Port already in use
```

### Issue 2: Dashboard Not Accessible
```bash
# Check if port is in use
netstat -tuln | grep 5000
lsof -i :5000

# Check dashboard logs
pm2 logs twitter-bot-dashboard --lines 50

# Test manually
python3 dashboard.py
```

### Issue 3: Bot Not Posting Tweets
```bash
# Check bot runner logs
pm2 logs twitter-bot-runner --lines 200

# Check cookies validity
# - Cookies might be expired
# - Re-login via browser and update cookies.json

# Check rate limits in database
sqlite3 accounts/account1_GrnStore4347/data/metrics.db
> SELECT * FROM rate_limits ORDER BY timestamp DESC LIMIT 10;
```

### Issue 4: High Memory Usage
```bash
# Check memory usage
pm2 monit

# Restart specific process
pm2 restart twitter-bot-runner

# Lower max_memory_restart if needed
pm2 delete twitter-bot-runner
# Edit ecosystem.config.js: max_memory_restart: '500M'
pm2 start ecosystem.config.js
```

---

## 📁 Log Files Location

```
data/logs/
├── pm2-dashboard-error.log        # Dashboard V1 errors
├── pm2-dashboard-out.log          # Dashboard V1 output
├── pm2-dashboard-v2-error.log     # Dashboard V2 errors
├── pm2-dashboard-v2-out.log       # Dashboard V2 output
├── pm2-bot-runner-error.log       # Bot runner errors
├── pm2-bot-runner-out.log         # Bot runner output
└── bot.log                        # Application logs (from Python)

accounts/account1_GrnStore4347/data/logs/
├── pm2-error.log                  # Account1 errors (if individual mode)
└── pm2-out.log                    # Account1 output (if individual mode)
```

---

## 🔄 Update & Redeploy

### Update Code
```bash
# Pull latest code
git pull origin main

# Install new dependencies (if any)
pip3 install -r requirements.txt

# Restart services
pm2 restart all

# Or reload with zero downtime
pm2 reload all
```

### Update Configuration
```bash
# Edit config files
nano config/settings.yaml
nano config/templates.yaml

# No restart needed! ConfigLoader has hot reload
# But you can restart to be sure:
pm2 restart twitter-bot-runner
```

---

## 🛡️ Security Considerations

### 1. File Permissions
```bash
# Protect sensitive files
chmod 600 config/settings.yaml
chmod 600 accounts/*/cookies.json
chmod 600 .env

# Protect directories
chmod 700 accounts/
chmod 700 data/
```

### 2. Environment Variables (Optional)
Create `.env` file:
```bash
# .env
FLASK_SECRET_KEY=your-secret-key-here
AI_API_URL=https://api.elrayyxml.web.id/api/ai/copilot
```

Load in `ecosystem.config.js`:
```javascript
env: {
  ...require('dotenv').config().parsed
}
```

### 3. Firewall Rules (Production Server)
```bash
# Only allow specific IPs to access dashboard
sudo ufw allow from YOUR_IP to any port 5000
sudo ufw allow from YOUR_IP to any port 5001

# Or use nginx reverse proxy with authentication
```

---

## 📊 Monitoring & Alerts

### 1. PM2 Plus (Cloud Monitoring)
```bash
pm2 link <secret> <public>

# Features:
# - Real-time monitoring
# - Email alerts on errors
# - Custom metrics
# - Transaction tracing
```

### 2. Custom Health Check Script
Create `health_check.sh`:
```bash
#!/bin/bash
# Check if bot is running
if ! pm2 list | grep -q "twitter-bot-runner.*online"; then
    echo "Bot is down! Restarting..."
    pm2 restart twitter-bot-runner
    # Send alert (email, Telegram, etc)
fi
```

Add to crontab:
```bash
# Check every 5 minutes
*/5 * * * * /path/to/health_check.sh
```

---

## 🎯 Performance Optimization

### 1. Use Cluster Mode (for dashboards)
```javascript
// In ecosystem.config.js
instances: 'max',  // Use all CPU cores
exec_mode: 'cluster'
```

### 2. Enable Compression
```javascript
// Add to dashboard Flask app
from flask_compress import Compress
compress = Compress(app)
```

### 3. Database Optimization
```bash
# Vacuum database regularly
sqlite3 data/metrics.db "VACUUM;"

# Add to crontab (weekly)
0 2 * * 0 sqlite3 /path/to/data/metrics.db "VACUUM;"
```

---

## 📱 Remote Management

### SSH Port Forwarding
```bash
# Access dashboard remotely via SSH tunnel
ssh -L 5000:localhost:5000 user@your-server.com
ssh -L 5001:localhost:5001 user@your-server.com

# Now access via:
# http://localhost:5000
# http://localhost:5001
```

### PM2 Web Interface
```bash
# Start PM2 web interface
pm2 web

# Access via browser:
# http://your-server-ip:9615
```

---

## 🆘 Quick Reference Card

```bash
# ESSENTIAL COMMANDS
pm2 start ecosystem.config.js    # Start all
pm2 stop all                      # Stop all
pm2 restart all                   # Restart all
pm2 logs                          # View logs
pm2 monit                         # Monitor
pm2 save                          # Save process list
pm2 status                        # Check status

# TROUBLESHOOTING
pm2 logs --err --lines 100        # Error logs
pm2 describe <name>               # Process details
pm2 flush                         # Clear logs
pm2 delete all && pm2 start ecosystem.config.js  # Fresh start

# MAINTENANCE
pm2 update                        # Update PM2
pm2 install pm2-logrotate         # Setup log rotation
pm2 startup                       # Auto-start on boot
pm2 save                          # Save current setup
```

---

## ✅ Post-Deployment Checklist

- [ ] PM2 installed and running
- [ ] All dependencies installed
- [ ] Config files configured (settings.yaml, templates.yaml, keywords.yaml)
- [ ] Cookies.json valid for each account
- [ ] Log directories created
- [ ] All services started (pm2 status shows "online")
- [ ] Dashboards accessible (localhost:5000, localhost:5001)
- [ ] Bot posting tweets successfully
- [ ] PM2 startup script configured
- [ ] PM2 process list saved
- [ ] Log rotation setup
- [ ] Monitoring enabled
- [ ] Backup strategy in place

---

## 🎓 Next Steps

1. **Monitor for 24 hours** - Check logs regularly
2. **Configure alerts** - Setup PM2 Plus or custom alerts
3. **Optimize templates** - Test different content styles
4. **Scale up** - Add more accounts as needed
5. **Backup regularly** - Backup config & database files

---

## 📞 Support

Jika ada masalah saat deployment:
1. Check logs: `pm2 logs --lines 200`
2. Check process details: `pm2 describe <name>`
3. Test manual run: `python3 main.py --test`
4. Check documentation: `README.md`, `QUICK_START.md`

---

**Last Updated**: 2026-01-17
**Version**: 2.0
**Status**: Production Ready ✅
