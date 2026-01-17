# ⚡ PM2 QUICK START - 5 Menit Setup

Panduan super cepat untuk deploy bot ke PM2.

---

## 🚀 Option 1: Auto Install (Recommended)

### Satu perintah untuk install semua:
```bash
# Install PM2 + dependencies + setup directories
bash scripts/install_pm2.sh

# Start semua services
./scripts/pm2_helper.sh start
```

**Done!** ✅ Bot sudah jalan!

---

## 🔧 Option 2: Manual Install

### 1. Install PM2
```bash
# Install Node.js (jika belum ada)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2
npm install -g pm2

# Verify
pm2 --version
```

### 2. Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Start Services
```bash
pm2 start ecosystem.config.js
```

---

## 📊 Management Commands

```bash
# Status semua services
pm2 status

# Lihat logs real-time
pm2 logs

# Monitor resource usage
pm2 monit

# Restart semua
pm2 restart all

# Stop semua
pm2 stop all
```

---

## 🎯 Helper Script Commands

Jika pakai helper script:

```bash
./scripts/pm2_helper.sh start      # Start all
./scripts/pm2_helper.sh stop       # Stop all
./scripts/pm2_helper.sh restart    # Restart all
./scripts/pm2_helper.sh status     # Status
./scripts/pm2_helper.sh logs       # View logs
./scripts/pm2_helper.sh monitor    # Monitor
```

---

## 🌐 Access Dashboards

Setelah start, buka browser:

- **Dashboard V1**: http://localhost:5000 (Multi-account manager)
- **Dashboard V2**: http://localhost:5001 (Per-account view)

---

## 🔄 Auto-Start on Boot

```bash
# Setup auto-start
pm2 startup

# Copy & run the output command (sudo env PATH=...)
sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u $USER --hp $HOME

# Save current setup
pm2 save
```

Sekarang bot akan otomatis jalan setiap kali server restart! 🎉

---

## 📱 What's Running?

Setelah `pm2 start ecosystem.config.js`:

| Process Name | Description | Port |
|--------------|-------------|------|
| `twitter-bot-dashboard` | Multi-account manager | 5000 |
| `twitter-bot-dashboard-v2` | Per-account detailed view | 5001 |
| `twitter-bot-runner` | Bot automation (all accounts) | - |

---

## 🔍 Check If Working

```bash
# Check status
pm2 status

# Should show all 3 processes as "online":
# ✅ twitter-bot-dashboard      (online)
# ✅ twitter-bot-dashboard-v2   (online)
# ✅ twitter-bot-runner         (online)

# Check logs
pm2 logs --lines 50

# Should see bot activity:
# - "Bot initialized successfully!"
# - "Morning/Afternoon/Evening slot starting"
# - "Posted tweet successfully"
```

---

## ❌ Troubleshooting

### Problem: Process keeps restarting
```bash
# Check error logs
pm2 logs twitter-bot-runner --err --lines 50

# Common fixes:
# 1. Check cookies.json valid
# 2. Check config/settings.yaml correct
# 3. Check Python dependencies installed
```

### Problem: Dashboard tidak bisa diakses
```bash
# Check if port in use
sudo netstat -tuln | grep 5000

# Restart dashboard
pm2 restart twitter-bot-dashboard
```

### Problem: Bot tidak posting
```bash
# Check bot logs
pm2 logs twitter-bot-runner --lines 100

# Check schedule di config/settings.yaml
# Check cookies valid
# Check rate limits
```

---

## 📁 Important Files

```
ecosystem.config.js          # PM2 configuration
scripts/pm2_helper.sh        # Helper commands
scripts/install_pm2.sh       # Auto installer
PM2_DEPLOYMENT_GUIDE.md     # Full documentation
```

---

## 🎓 Next Steps

1. ✅ Bot jalan → Monitor 1 hari via `pm2 logs`
2. ✅ Setup auto-start → `pm2 startup` + `pm2 save`
3. ✅ Configure templates → Edit `config/templates.yaml`
4. ✅ Add more accounts → Via dashboard http://localhost:5000
5. ✅ Monitor metrics → Via dashboard atau `pm2 monit`

---

## 📞 Need Help?

- **Full docs**: `PM2_DEPLOYMENT_GUIDE.md`
- **Bot usage**: `QUICK_START.md`
- **Troubleshooting**: Check logs `pm2 logs --err`

---

**Status**: Ready to deploy! 🚀
