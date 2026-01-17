# 🚀 Twitter Bot - Jualan Kuota XL

Bot promosi Twitter yang **AMAN**, **DINAMIS**, dan **AI-POWERED** untuk jualan kuota XL dan Kuota XL Akrab.

> **📖 Dokumentasi lengkap**: [`docs/INDEX.md`](docs/INDEX.md) | **🚀 Deployment**: [`DEPLOYMENT.md`](DEPLOYMENT.md)**

## ✨ Features

- ✅ **Template Dinamis** - Edit templates kapan saja tanpa restart
- ✅ **AI-Powered Content** - Auto-improve tweets dengan AI sebelum posting
- ✅ **Accurate Metrics** - Real-time tracking dengan SQLite database
- ✅ **Safe Automation** - Rate limiting & random delays
- ✅ **Easy Configuration** - Semua setting di YAML files (user-friendly)
- ✅ **Web Dashboard** - Monitor bot activity via browser
- ✅ **Media Support** - Upload gambar/video untuk promo

## 📊 Target & Strategy

- **Target:** 300-500 followers dalam 30 hari
- **Schedule:** 3x/hari (08:00, 13:00, 20:00)
- **Approach:** 70% value content, 30% promo
- **CTA:** WhatsApp link (NO DM spam!)

## 🛠️ Tech Stack

- **Python 3.14**
- **Twikit** - Twitter automation
- **httpx** - HTTP client with timeout
- **SQLite** - Metrics database
- **Flask** - Web dashboard
- **PyYAML** - Configuration management
- **ElrayyXml AI API** - Content improvement

## 📁 Project Structure

```
twitter-bot/
├── bot/                    # Core bot modules
│   ├── automation.py      # Main automation logic
│   ├── twitter_client.py  # Twitter API wrapper
│   ├── ai_client.py       # AI integration
│   ├── content_generator.py # Content generation
│   ├── database.py        # Metrics tracking
│   └── config_loader.py   # Config management
├── config/                # Configuration files
│   ├── settings.yaml      # Main settings
│   ├── templates.yaml     # Tweet templates
│   ├── keywords.yaml      # Search keywords
│   ├── settings_akrab.yaml    # Akrab variant
│   └── templates_akrab.yaml   # Akrab templates
├── data/                  # Database & logs
│   ├── metrics.db         # SQLite database
│   └── logs/              # Log files
├── docs/                  # Documentation
│   ├── DEVELOPMENT_PLAN.md
│   ├── USAGE.md
│   ├── CARA_PAKAI_AKRAB.md
│   └── ...
├── media/promo/           # Media files for tweets
├── static/                # Dashboard assets
├── templates/             # Dashboard HTML
├── main.py               # CLI entry point
├── dashboard.py          # Web dashboard
└── requirements.txt      # Dependencies
```

## 🚀 Quick Start

> **📖 Panduan lengkap**: [`docs/QUICK_START.md`](docs/QUICK_START.md)

### 1. Installation

```bash
# Clone repository
git clone <repo-url>
cd twitter-bot

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# atau: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Edit settings
nano config/settings.yaml

# Minimal required config:
# - wa_number: Your WhatsApp number
# - prices: Your product prices
# - cookies_file: Twitter cookies (cookies.json)
```

### 3. Setup Twitter Cookies

```bash
# Login ke Twitter di browser
# Export cookies menggunakan extension
# Save ke cookies.json
```

### 4. Test Connection

```bash
# Test bot connection
python main.py --test

# Expected output:
# ✅ Connection test passed!
# Logged in as: @YourUsername
```

### 5. Run Bot

```bash
# Run once (manual)
python main.py --run-once morning

# Run scheduled mode (daemon)
python main.py --daemon

# Start web dashboard
python dashboard.py
# Open: http://localhost:5000
```

## 📖 Documentation

### 🎯 Essential Guides
- **📚 [Documentation Index](docs/INDEX.md)** - Central hub untuk semua dokumentasi
- **⚡ [Quick Start](docs/QUICK_START.md)** - Setup bot dalam 10 menit
- **🚀 [Deployment Guide](DEPLOYMENT.md)** - Deploy ke production dengan PM2
- **📖 [User Guide](docs/guides/USAGE.md)** - Panduan penggunaan lengkap

### 📁 Documentation Categories
```
docs/
├── INDEX.md                    # 📚 Central documentation index
├── QUICK_START.md              # ⚡ Quick setup guide
├── deployment/                 # 🚀 Production deployment guides
│   ├── PM2_DEPLOYMENT_GUIDE.md
│   └── PM2_QUICK_START.md
├── guides/                     # 📖 User guides & tutorials
│   ├── USAGE.md
│   ├── CARA_PAKAI_AKRAB.md
│   ├── PANDUAN_TAMBAH_COOKIES.md
│   └── PANDUAN_MEDIA_PROMO.md
├── migration/                  # 🔄 Migration & multi-account
│   └── MULTI_ACCOUNT_RUNNING_GUIDE.md
├── technical/                  # 🔧 Technical documentation
│   ├── NEW_TEMPLATE_SYSTEM.md
│   └── DEVELOPMENT_PLAN.md
└── reports/                    # 📊 Test results & reports
    └── SAFETY_REPORT.md
```

**👉 Lihat semua dokumentasi**: [`docs/INDEX.md`](docs/INDEX.md)

## 🎯 Usage Examples

### Manual Posting

```bash
# Morning slot (8:00)
python main.py --run-once morning

# Afternoon slot (13:00)
python main.py --run-once afternoon

# Evening slot (20:00)
python main.py --run-once evening
```

### Scheduled Mode

```bash
# Run as daemon (auto post 3x/day)
python main.py --daemon

# Or use PM2 for production (recommended)
pm2 start ecosystem.config.js

# Bot akan otomatis post di:
# - 08:00 WIB (Pagi)
# - 13:00 WIB (Siang)
# - 20:00 WIB (Malam)
```

### Web Dashboard

```bash
# Start dashboard
python dashboard.py

# Features:
# - Real-time metrics
# - Manual tweet posting
# - Configuration editor
# - Activity logs
# - Performance charts
```

## 📊 Metrics Tracking

Bot otomatis track:
- Daily tweets count
- Follower growth
- Engagement rate
- Tweet performance
- Keyword effectiveness
- Business metrics (WA messages, orders)

Lihat metrics via:
- Web dashboard: `http://localhost:5000`
- Database: `data/metrics.db`

## ⚠️ Safety Features

1. **Rate Limiting** - Max 10 tweets/day, 15 follows/day
2. **Random Delays** - 10-30 seconds antar aksi
3. **Error Recovery** - Auto-retry dengan exponential backoff
4. **Activity Logging** - Full audit trail
5. **Health Checks** - Monitor account status
6. **Safe Mode** - Auto-pause jika detect masalah

## 🔧 Advanced Configuration

### Switch ke Config Akrab

```bash
# Backup config lama
cp config/settings.yaml config/settings_backup.yaml

# Copy config Akrab
cp config/settings_akrab.yaml config/settings.yaml
cp config/templates_akrab.yaml config/templates.yaml

# Restart bot
```

### Custom Templates

Edit `config/templates.yaml`:

```yaml
promo_templates:
  - "🔥 KUOTA XL MURAH! {paket} cuma {harga}!"
  - "📱 Your custom template here..."
```

Variables available:
- `{paket}` - Paket name
- `{harga}` - Price
- `{harga_normal}` - Normal price
- `{diskon}` - Discount percentage
- `{wa_number}` - WhatsApp number
- `{wa_link}` - WhatsApp link

## 🐛 Troubleshooting

### Bot tidak bisa login
- Check cookies.json masih valid
- Re-export cookies dari browser
- Lihat [SOLUSI_ERROR_226.md](docs/SOLUSI_ERROR_226.md)

### Tweet tidak muncul
- Check rate limits (max 10/day)
- Check logs di `data/logs/bot.log`
- Pastikan Twitter tidak shadowban

### Dashboard tidak buka
- Check port 5000 tidak dipakai app lain
- Run: `python dashboard.py`
- Check firewall settings

## 📈 Expected Results

**Week 1-2:**
- 50-150 followers
- 1-3 WA inquiries

**Week 3-4:**
- 150-300 followers
- 3-5 WA inquiries/week
- 1-2 orders/week

**Month 2+:**
- 300-500 followers
- 10-15 WA inquiries/week
- 3-5 orders/week

## 🤝 Contributing

Project ini masih dalam development aktif. Contributions welcome!

## 📄 License

Private project - All rights reserved

---

**Status:** ✅ Production Ready  
**Last Updated:** 2025-12-21  
**Version:** 1.0.0

---

## 🔀 MULTI-ACCOUNT SUPPORT

Bot sekarang mendukung **multiple Twitter accounts** secara bersamaan!

### Quick Setup

```bash
# 1. Start dashboard
python dashboard.py

# 2. Add account (browser: http://localhost:5000/accounts)
Click "➕ Add Account"

# 3. Add cookies
python add_account_cookies.py

# 4. Enable & Start via dashboard
Toggle "Enabled" → Click "▶️ Start"
```

### Documentation
- **Quick Guide**: `QUICK_GUIDE_MULTI_ACCOUNT.md`
- **Cookies Guide**: `docs/PANDUAN_TAMBAH_COOKIES.md`
- **Full Implementation**: `MULTI_ACCOUNT_IMPLEMENTATION_COMPLETE.md`

### Features
- ✅ Unlimited accounts support
- ✅ Concurrent execution
- ✅ Per-account configuration
- ✅ Web-based management
- ✅ Real-time monitoring
- ✅ Error isolation
- ✅ CLI & API support

