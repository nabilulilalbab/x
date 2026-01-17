# 🚀 DEPLOYMENT GUIDE - Twitter Bot

Panduan deployment lengkap untuk production environment menggunakan PM2.

---

## 📚 Table of Contents

1. [Quick Start](#-quick-start-5-menit)
2. [Prerequisites](#-prerequisites)
3. [Installation](#-installation)
4. [Configuration](#-configuration)
5. [Deployment](#-deployment)
6. [Management](#-management)
7. [Monitoring](#-monitoring)
8. [Troubleshooting](#-troubleshooting)
9. [Production Best Practices](#-production-best-practices)

---

## ⚡ Quick Start (5 Menit)

```bash
# 1. Install PM2
npm install -g pm2

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Configure bot
cp config/settings.yaml.example config/settings.yaml
nano config/settings.yaml  # Edit sesuai kebutuhan

# 4. Add Twitter cookies
# Buat file: accounts/account1_*/cookies.json

# 5. Start dengan PM2
pm2 start ecosystem.config.js

# 6. Check status
pm2 status

# 7. View logs
pm2 logs
```

**Done!** ✅ Bot jalan di background dengan auto-restart!

---

## 📋 Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+, CentOS 8+) atau macOS
- **Python**: 3.8 atau lebih baru
- **Node.js**: 16.x atau lebih baru (untuk PM2)
- **RAM**: Minimal 512MB (recommended 1GB+)
- **Disk**: Minimal 500MB free space

### Software Requirements
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check pip
pip3 --version

# Install Node.js (if not installed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version  # Should be 16+
npm --version
```

---

## 🔧 Installation

### Step 1: Install PM2

```bash
# Install PM2 globally
sudo npm install -g pm2

# Verify installation
pm2 --version
```

### Step 2: Install Python Dependencies

```bash
# Install all dependencies
pip3 install -r requirements.txt

# Or use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Step 3: Setup Directories

```bash
# Create necessary directories
mkdir -p data/logs
mkdir -p accounts/account1_GrnStore4347/{config,data/logs,media/promo}
mkdir -p accounts/account2_KorteksL43042/{config,data/logs,media/promo}

# Set permissions
chmod 755 data/logs
chmod 700 accounts/
```

---

## ⚙️ Configuration

### 1. Bot Settings

Edit `config/settings.yaml`:
```yaml
account:
  username: '@YourUsername'

business:
  wa_number: '081234567890'
  wa_link: 'https://wa.me/6281234567890?text=...'

schedule:
  enabled: true
  morning:
    enabled: true
    time: '08:00'
  afternoon:
    enabled: true
    time: '13:00'
  evening:
    enabled: true
    time: '20:00'

ai:
  enabled: true
  api_url: 'https://api.elrayyxml.web.id/api/ai/copilot'
```

### 2. Templates

Edit `config/templates.yaml`:
```yaml
promo_templates:
  - text: "🔥 KUOTA XL 10GB cuma Rp25.000!"
    media: "media/promo/image1.jpg"  # Optional
  - text: "📱 Stok ready! Kuota XL 25GB = Rp50.000!"
    media: null
```

### 3. Keywords

Edit `config/keywords.yaml`:
```yaml
high_intent:
  - "butuh kuota xl"
  - "jual kuota xl"
  - "kuota xl murah"
```

### 4. Multi-Account Setup

Edit `config/accounts.yaml`:
```yaml
accounts:
  - id: account1
    name: "Main Account"
    username: "@GrnStore4347"
    folder: "accounts/account1_GrnStore4347"
    enabled: true
  
  - id: account2
    name: "Secondary Account"
    username: "@KorteksL43042"
    folder: "accounts/account2_KorteksL43042"
    enabled: true

settings:
  max_concurrent_accounts: 2
```

### 5. Twitter Cookies

**Per Account:**
1. Login ke Twitter di browser
2. Export cookies (gunakan extension "EditThisCookie" atau "Cookie Editor")
3. Save sebagai `accounts/account1_*/cookies.json`

Format:
```json
{
  "ct0": "...",
  "auth_token": "..."
}
```

**Panduan lengkap**: `docs/guides/PANDUAN_TAMBAH_COOKIES.md`

---

## 🚀 Deployment

### PM2 Configuration

File `ecosystem.config.js` sudah ter-configure untuk:

1. **Dashboard V1** (Port 5000) - Multi-account manager
2. **Dashboard V2** (Port 5001) - Per-account view
3. **Bot Runner** - Automation engine untuk semua account

### Start Services

```bash
# Start semua services
pm2 start ecosystem.config.js

# Expected output:
# ┌─────┬────────────────────────────┬─────────┬─────────┐
# │ id  │ name                       │ status  │ restart │
# ├─────┼────────────────────────────┼─────────┼─────────┤
# │ 0   │ twitter-bot-dashboard      │ online  │ 0       │
# │ 1   │ twitter-bot-dashboard-v2   │ online  │ 0       │
# │ 2   │ twitter-bot-runner         │ online  │ 0       │
# └─────┴────────────────────────────┴─────────┴─────────┘
```

### Verify Deployment

```bash
# 1. Check PM2 status
pm2 status

# 2. Check logs
pm2 logs --lines 50

# 3. Test dashboards
curl http://localhost:5000  # Should return HTML
curl http://localhost:5001  # Should return HTML

# 4. Check if bot is posting
pm2 logs twitter-bot-runner | grep "Posted tweet"
```

---

## 📊 Management

### Basic Commands

```bash
# View status
pm2 status
pm2 list

# View logs (real-time)
pm2 logs                              # All processes
pm2 logs twitter-bot-runner           # Specific process
pm2 logs --lines 100                  # Last 100 lines
pm2 logs --err                        # Errors only

# Monitor resources
pm2 monit

# Process info
pm2 info twitter-bot-runner
```

### Start/Stop/Restart

```bash
# Stop
pm2 stop all                          # Stop all
pm2 stop twitter-bot-runner           # Stop specific
pm2 stop 0                            # Stop by ID

# Start
pm2 start ecosystem.config.js         # Start all
pm2 start twitter-bot-runner          # Start specific

# Restart
pm2 restart all                       # Restart all
pm2 restart twitter-bot-runner        # Restart specific

# Reload (zero-downtime)
pm2 reload all
```

### Delete Processes

```bash
# Delete from PM2
pm2 delete all                        # Delete all
pm2 delete twitter-bot-runner         # Delete specific

# Then start fresh
pm2 start ecosystem.config.js
```

---

## 🔍 Monitoring

### Real-time Monitoring

```bash
# CPU & Memory monitoring
pm2 monit

# Dashboard (web interface)
pm2 web
# Access: http://localhost:9615
```

### Logs Management

```bash
# View logs
pm2 logs --lines 200
pm2 logs --json                       # JSON format

# Flush logs (clear all)
pm2 flush

# Log files location:
data/logs/
├── pm2-dashboard-error.log
├── pm2-dashboard-out.log
├── pm2-dashboard-v2-error.log
├── pm2-dashboard-v2-out.log
├── pm2-bot-runner-error.log
└── pm2-bot-runner-out.log
```

### Setup Log Rotation

```bash
# Install PM2 log rotate
pm2 install pm2-logrotate

# Configure
pm2 set pm2-logrotate:max_size 10M        # Max 10MB per file
pm2 set pm2-logrotate:retain 7            # Keep 7 rotated files
pm2 set pm2-logrotate:compress true       # Compress old logs
pm2 set pm2-logrotate:rotateInterval '0 0 * * *'  # Daily at midnight
```

---

## ❌ Troubleshooting

### Issue 1: Process Keeps Restarting

**Symptoms:**
```bash
pm2 status
# Shows: restart count keeps increasing
```

**Solutions:**
```bash
# 1. Check error logs
pm2 logs twitter-bot-runner --err --lines 100

# 2. Common causes & fixes:
# - Cookies expired → Update cookies.json
# - Missing dependencies → pip3 install -r requirements.txt
# - Port in use → Change port in config or kill process
# - Config error → Check syntax in YAML files

# 3. Test manual run
python3 main.py --test

# 4. Restart with clean state
pm2 delete twitter-bot-runner
pm2 start ecosystem.config.js
```

### Issue 2: Dashboard Not Accessible

**Symptoms:**
```bash
curl http://localhost:5000
# Connection refused
```

**Solutions:**
```bash
# 1. Check if port is in use
sudo netstat -tuln | grep 5000
sudo lsof -i :5000

# 2. Check dashboard logs
pm2 logs twitter-bot-dashboard --lines 50

# 3. Test manual run
python3 dashboard.py

# 4. Check firewall
sudo ufw status
sudo ufw allow 5000/tcp
```

### Issue 3: Bot Not Posting Tweets

**Symptoms:**
- Bot is running but no tweets posted

**Solutions:**
```bash
# 1. Check logs for errors
pm2 logs twitter-bot-runner --lines 200 | grep -i error

# 2. Verify configuration
# - Schedule enabled? Check config/settings.yaml
# - Cookies valid? Check accounts/*/cookies.json
# - Rate limits reached? Check database

# 3. Check database
sqlite3 accounts/account1_*/data/metrics.db
> SELECT * FROM rate_limits ORDER BY timestamp DESC LIMIT 10;
> SELECT * FROM activities ORDER BY timestamp DESC LIMIT 10;

# 4. Test manual posting
python3 main.py --run-once morning --account account1
```

### Issue 4: High Memory Usage

**Symptoms:**
```bash
pm2 monit
# Shows high memory usage (>500MB per process)
```

**Solutions:**
```bash
# 1. Restart process
pm2 restart twitter-bot-runner

# 2. Lower memory limit in ecosystem.config.js
max_memory_restart: '300M'  # Restart if exceed 300MB

# 3. Check for memory leaks
pm2 logs twitter-bot-runner | grep -i memory

# 4. Optimize database
sqlite3 data/metrics.db "VACUUM;"
```

---

## 🎯 Production Best Practices

### 1. Auto-Start on Boot

```bash
# Generate startup script
pm2 startup

# Output will show command like:
# sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u youruser --hp /home/youruser

# Run that command, then:
pm2 save

# Test
sudo reboot
# After reboot, check:
pm2 status  # Should show all processes running
```

### 2. Security

```bash
# File permissions
chmod 600 config/settings.yaml
chmod 600 accounts/*/cookies.json
chmod 700 accounts/
chmod 755 data/

# Firewall (production server)
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 5000/tcp  # Dashboard (restrict to specific IP)
sudo ufw allow 5001/tcp  # Dashboard V2 (restrict to specific IP)

# Or better: Use reverse proxy with auth
# See: docs/deployment/NGINX_SETUP.md (to be created)
```

### 3. Backup Strategy

```bash
# Backup critical files daily
#!/bin/bash
BACKUP_DIR="/backup/twitter-bot"
DATE=$(date +%Y%m%d)

tar -czf "$BACKUP_DIR/config-$DATE.tar.gz" config/
tar -czf "$BACKUP_DIR/accounts-$DATE.tar.gz" accounts/
tar -czf "$BACKUP_DIR/data-$DATE.tar.gz" data/

# Keep last 7 days only
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete
```

Add to crontab:
```bash
crontab -e
# Add:
0 2 * * * /path/to/backup_script.sh
```

### 4. Monitoring & Alerts

**Option 1: PM2 Plus (Cloud)**
```bash
# Sign up at pm2.io
pm2 link <secret_key> <public_key>

# Features:
# - Real-time monitoring
# - Email alerts on errors
# - Custom metrics
# - Transaction tracing
```

**Option 2: Custom Health Check**
```bash
#!/bin/bash
# health_check.sh

if ! pm2 list | grep -q "twitter-bot-runner.*online"; then
    echo "Bot is down! Restarting..."
    pm2 restart twitter-bot-runner
    
    # Send alert (example: via Telegram)
    curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
         -d "chat_id=<CHAT_ID>&text=Twitter Bot restarted!"
fi
```

Add to crontab (check every 5 minutes):
```bash
*/5 * * * * /path/to/health_check.sh
```

### 5. Update Workflow

```bash
# Safe update procedure
cd /path/to/twitter-bot

# 1. Backup current state
pm2 save
tar -czf backup-$(date +%Y%m%d).tar.gz config/ accounts/

# 2. Pull latest code
git pull origin main

# 3. Update dependencies
pip3 install -r requirements.txt --upgrade

# 4. Test configuration
python3 main.py --test

# 5. Reload without downtime
pm2 reload all

# 6. Monitor
pm2 logs --lines 100
```

---

## 📁 Directory Structure After Deployment

```
twitter-bot/
├── 📄 Main Files
│   ├── README.md
│   ├── DEPLOYMENT.md           ← You are here
│   ├── main.py
│   ├── dashboard.py
│   ├── dashboard_v2.py
│   ├── requirements.txt
│   └── ecosystem.config.js
│
├── 🤖 Bot Modules
│   └── bot/
│       ├── automation.py
│       ├── twitter_client.py
│       ├── content_generator.py
│       └── ...
│
├── ⚙️ Configuration
│   └── config/
│       ├── settings.yaml
│       ├── templates.yaml
│       ├── keywords.yaml
│       └── accounts.yaml
│
├── 👤 Accounts
│   └── accounts/
│       ├── account1_GrnStore4347/
│       │   ├── config/
│       │   ├── cookies.json
│       │   ├── data/metrics.db
│       │   └── media/promo/
│       └── account2_KorteksL43042/
│           └── ...
│
├── 📊 Data & Logs
│   └── data/
│       └── logs/
│           ├── pm2-dashboard-error.log
│           ├── pm2-dashboard-out.log
│           └── ...
│
└── 📚 Documentation
    └── docs/
        ├── QUICK_START.md
        ├── deployment/
        │   └── PM2_DEPLOYMENT_GUIDE.md
        └── guides/
            └── ...
```

---

## 🆘 Quick Reference

```bash
# ESSENTIAL COMMANDS
pm2 start ecosystem.config.js    # Start all
pm2 stop all                      # Stop all
pm2 restart all                   # Restart all
pm2 logs                          # View logs
pm2 monit                         # Monitor
pm2 status                        # Check status

# TROUBLESHOOTING
pm2 logs --err --lines 100        # Error logs
pm2 describe <name>               # Process details
pm2 flush                         # Clear logs
pm2 delete all                    # Remove all processes

# MAINTENANCE
pm2 update                        # Update PM2
pm2 save                          # Save process list
pm2 startup                       # Auto-start setup
```

---

## 📞 Support & Documentation

- **Quick Start**: `docs/QUICK_START.md`
- **Full User Guide**: `docs/guides/USAGE.md`
- **Configuration**: `docs/guides/` folder
- **Troubleshooting**: This file (Troubleshooting section)
- **API Reference**: `docs/technical/` folder

---

## ✅ Deployment Checklist

Before going to production:

- [ ] PM2 installed and working (`pm2 --version`)
- [ ] Python dependencies installed (`pip3 list`)
- [ ] Configuration files edited (`config/*.yaml`)
- [ ] Twitter cookies added (`accounts/*/cookies.json`)
- [ ] Test run successful (`python3 main.py --test`)
- [ ] PM2 services started (`pm2 status` shows "online")
- [ ] Dashboards accessible (`curl localhost:5000`)
- [ ] Bot posting tweets (check logs)
- [ ] Auto-start configured (`pm2 startup` + `pm2 save`)
- [ ] Log rotation setup (`pm2 install pm2-logrotate`)
- [ ] Backups configured (cron job)
- [ ] Monitoring enabled (PM2 Plus or custom)
- [ ] Security hardened (firewall, permissions)

---

**Version**: 2.0  
**Last Updated**: 2026-01-17  
**Status**: Production Ready ✅
