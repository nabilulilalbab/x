# 🤖 Multi-Account Bot - Running Guide

## ✅ Current Status

**System:** Multi-account bot AKTIF dan BERJALAN  
**Date:** 2025-12-21  
**Accounts:** 2 accounts configured, 1 running

### 📊 Account Status

| Account | Username | Status | Schedule | WA Number |
|---------|----------|--------|----------|-----------|
| **Account2** | @KorteksL43042 | 🟢 **RUNNING** | Auto (08:00, 13:00, 20:00) | 085117557905 |
| **Account1** | @GrnStore4347 | ⚪ IDLE | Auto (08:00, 13:00, 20:00) | 085117557905 |

> **Note:** Account1 perlu cookies baru untuk running. Account2 sudah aktif dan akan post otomatis!

---

## 🕐 Schedule Otomatis

Bot akan jalan otomatis pada waktu-waktu ini (WIB):

### 🌅 Morning Slot (08:00)
- ✅ Post **promo tweet** + media
- ✅ Search & like 5 tweets
- ✅ Follow 5 target users
- ⏱️ Duration: ~5-10 menit

### 🌤️ Afternoon Slot (13:00)
- ✅ Post **value tweet** (tips/tutorial)
- ✅ Search & like 5 tweets
- ⏱️ Duration: ~3-5 menit

### 🌙 Evening Slot (20:00)
- ✅ Post **promo tweet** + media
- ✅ Search & like 3 tweets
- ✅ Follow 5 target users
- ✅ Daily summary report
- ⏱️ Duration: ~5-10 menit

---

## 🎯 What Bot Does Automatically

### Content Posting
- **Promo Tweets:** 2x per day (morning & evening) dengan gambar promo
- **Value Tweets:** 1x per day (afternoon) berupa tips/tutorial
- **AI Enhancement:** Semua tweet di-improve dengan AI
- **WA Number:** Otomatis ditambahkan di promo tweets

### Engagement
- **Likes:** 13 likes per day (5+5+3)
- **Follows:** 10 follows per day (5+5)
- **Search:** Target keywords dari `keywords.yaml`
- **Safe Limits:** Rate limiting untuk avoid ban

### Tracking
- **Metrics:** Tweets, likes, follows, engagement rate
- **Orders:** Track orders & revenue via dashboard
- **Logs:** Activity logs tersimpan di database
- **Analytics:** Daily, weekly, monthly reports

---

## 🎛️ Control Panel

### Dashboard V1 (Multi-Account Management)
**URL:** http://localhost:5000/accounts

**Features:**
- Start/Stop all accounts
- Start/Stop per account
- Upload cookies per account
- View metrics table
- WA Number display per account

### Dashboard V2 (Detailed View)
**URL:** http://localhost:5001

**Features:**
- Select account dari dropdown
- WA Number clickable (direct WhatsApp)
- Detailed metrics (8 stat cards)
- Real-time updates (30s refresh)
- Orders & Revenue tracking

---

## 🔧 Control Commands

### Via Dashboard (Recommended)
```
Open: http://localhost:5000/accounts
Click: Start/Stop buttons
```

### Via Command Line

**Check Status:**
```bash
curl http://localhost:5000/api/multi/status | python3 -m json.tool
```

**Start All Accounts:**
```bash
curl -X POST http://localhost:5000/api/multi/start-all
```

**Stop All Accounts:**
```bash
curl -X POST http://localhost:5000/api/multi/stop-all
```

**Start Specific Account:**
```bash
curl -X POST http://localhost:5000/api/multi/accounts/account1/start
curl -X POST http://localhost:5000/api/multi/accounts/account2/start
```

**Stop Specific Account:**
```bash
curl -X POST http://localhost:5000/api/multi/accounts/account1/stop
curl -X POST http://localhost:5000/api/multi/accounts/account2/stop
```

**Restart Account:**
```bash
curl -X POST http://localhost:5000/api/multi/accounts/account1/restart
```

---

## 🔴 Troubleshooting Account1

### Problem
Account1 menampilkan error: `404 "Sorry, that page does not exist"`

### Cause
Cookies sudah **expired** atau **invalid**. Twitter API menolak session.

### Solution

**OPSI 1: Upload via Dashboard** (Easiest)
1. Buka http://localhost:5000/accounts
2. Klik tombol "🍪 Cookies" di row Account1
3. Upload cookies.json baru
4. Klik "▶️ Start"

**OPSI 2: Manual Copy**
1. Export cookies dari browser (extension: EditThisCookie/Cookie-Editor)
2. Login ke Twitter dengan @GrnStore4347
3. Export sebagai JSON
4. Copy ke `accounts/account1_GrnStore4347/cookies.json`
5. Restart:
```bash
curl -X POST http://localhost:5000/api/multi/accounts/account1/restart
```

**OPSI 3: Use Same Cookies as Account2** (Temporary)
```bash
cp accounts/account2_KorteksL43042/cookies.json accounts/account1_GrnStore4347/cookies.json
curl -X POST http://localhost:5000/api/multi/accounts/account1/restart
```

---

## 📝 Monitoring & Logs

### Check Bot Logs
```bash
tail -f /tmp/dashboard_v1.log
```

### Check Specific Account Logs
```bash
tail -f /tmp/dashboard_v1.log | grep account1
tail -f /tmp/dashboard_v1.log | grep account2
```

### Watch for Errors
```bash
tail -f /tmp/dashboard_v1.log | grep -i error
```

### View Metrics in Dashboard
- Dashboard V1: http://localhost:5000/accounts
- Dashboard V2: http://localhost:5001

---

## ⚙️ Configuration Files

### Per-Account Settings
```
accounts/account1_GrnStore4347/config/settings.yaml
accounts/account2_KorteksL43042/config/settings.yaml
```

### Multi-Account Config
```
config/accounts.yaml  # Account list & global settings
```

### Templates & Keywords
```
accounts/{account_id}/config/templates.yaml   # Per-account templates
accounts/{account_id}/config/keywords.yaml    # Per-account keywords
```

---

## 🚀 Starting Everything on Server Boot

### Create systemd service (Linux)
```bash
sudo nano /etc/systemd/system/twitter-bot-dashboard.service
```

```ini
[Unit]
Description=Twitter Bot Dashboard
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/twitter-bot
ExecStart=/usr/bin/python3 /path/to/twitter-bot/dashboard.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable & Start:**
```bash
sudo systemctl enable twitter-bot-dashboard
sudo systemctl start twitter-bot-dashboard
sudo systemctl status twitter-bot-dashboard
```

### Or use tmux/screen (Simple)
```bash
# Start dashboard in tmux
tmux new -s twitter-bot
python3 dashboard.py

# Detach: Ctrl+B then D
# Reattach: tmux attach -t twitter-bot
```

---

## 📊 Expected Results

### Daily Activity (per account)
- **Tweets:** 3 tweets (2 promo + 1 value)
- **Likes:** 13 likes
- **Follows:** 10 follows
- **Engagement:** Search & interact with 20+ tweets

### Weekly Results (2 accounts)
- **Tweets:** 42 tweets total
- **Likes:** 182 likes total
- **Follows:** 140 follows total
- **Reach:** Thousands of impressions

### Growth Target (per account)
- **Followers:** +500 in 30 days
- **Engagement Rate:** 2%+
- **Orders:** 1+ per day (tracked via WA messages)

---

## ✅ Current Setup Summary

**What's Working:**
- ✅ Multi-account system configured
- ✅ Auto-scheduling enabled (08:00, 13:00, 20:00)
- ✅ Account2 running and active
- ✅ WA Number (085117557905) visible in dashboard
- ✅ Metrics tracking active
- ✅ Dashboard V1 running (port 5000)
- ✅ Dashboard V2 running (port 5001)

**What Needs Attention:**
- ⚠️ Account1 needs valid cookies to run
- 💡 Upload fresh cookies via dashboard

**Next Steps:**
1. Fix Account1 cookies (see Troubleshooting section)
2. Monitor first scheduled run (next: 08:00/13:00/20:00)
3. Check metrics in dashboard after each run
4. Track orders via Dashboard V2

---

## 📞 Support

**Dashboard URLs:**
- Multi-Account Control: http://localhost:5000/accounts
- Detailed Metrics: http://localhost:5001

**Documentation:**
- Quick Start: `QUICK_START.md`
- Navigation: `NAVIGATION.md`
- Project Structure: `PROJECT_STRUCTURE.md`

**Logs:**
- Dashboard: `/tmp/dashboard_v1.log`
- Account Metrics: `accounts/{account_id}/data/metrics.db`

---

*Last Updated: 2025-12-21*
*System Status: ✅ OPERATIONAL (1/2 accounts running)*
