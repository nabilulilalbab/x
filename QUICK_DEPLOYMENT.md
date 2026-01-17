# ⚡ QUICK DEPLOYMENT - 5 Menit

Panduan super cepat deploy Twitter Bot ke production.

---

## 🚀 Option 1: Auto Install (Termudah)

```bash
# 1. Clone/download project
cd twitter-bot

# 2. Auto install PM2 + dependencies
bash scripts/install_pm2.sh

# 3. Configure bot
nano config/settings.yaml
# Edit: wa_number, wa_link, username

# 4. Add Twitter cookies
nano accounts/account1_GrnStore4347/cookies.json
# Paste cookies dari browser

# 5. Start all services
pm2 start ecosystem.config.js

# 6. Check status
pm2 status

# Done! ✅
```

---

## 🔧 Option 2: Manual Install

```bash
# 1. Install PM2
npm install -g pm2

# 2. Install Python dependencies
pip3 install -r requirements.txt

# 3. Configure (sama dengan option 1)
nano config/settings.yaml
nano accounts/*/cookies.json

# 4. Start services
pm2 start ecosystem.config.js

# 5. Verify
pm2 logs
```

---

## ✅ Verify Deployment

```bash
# Check if services running
pm2 status
# Should show 3 processes: dashboard, dashboard-v2, bot-runner

# Check logs
pm2 logs --lines 50

# Test dashboards
curl http://localhost:5000  # Should return HTML
curl http://localhost:5001  # Should return HTML

# Monitor
pm2 monit
```

---

## 🔄 Auto-Start on Boot

```bash
pm2 startup
# Run the displayed command (sudo env PATH=...)
pm2 save
```

---

## 📊 Essential Commands

```bash
pm2 status          # Check status
pm2 logs            # View logs
pm2 restart all     # Restart all
pm2 stop all        # Stop all
pm2 monit           # Monitor resources
```

---

## 🌐 Access Dashboards

- **Dashboard V1**: http://localhost:5000
- **Dashboard V2**: http://localhost:5001

---

## 🆘 Troubleshooting

**Bot tidak posting?**
```bash
pm2 logs twitter-bot-runner --lines 100
# Check cookies valid
# Check schedule enabled in config/settings.yaml
```

**Dashboard tidak bisa diakses?**
```bash
pm2 restart twitter-bot-dashboard
sudo netstat -tuln | grep 5000
```

---

## 📖 Full Documentation

- **Complete Guide**: [`DEPLOYMENT.md`](DEPLOYMENT.md)
- **User Guide**: [`docs/QUICK_START.md`](docs/QUICK_START.md)
- **All Docs**: [`docs/INDEX.md`](docs/INDEX.md)

---

**⏱️ Time**: ~5 minutes  
**✅ Status**: Production Ready
