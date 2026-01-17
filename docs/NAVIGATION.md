# 🧭 Quick Navigation

Panduan cepat untuk menemukan file yang Anda butuhkan.

## 🚀 Getting Started

1. **First time setup**: [`QUICK_START.md`](QUICK_START.md)
2. **Project overview**: [`README.md`](README.md)
3. **Project structure**: [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md)

## 🎯 Common Tasks

### Running the Bot
```bash
# Run main bot
python3 main.py

# Run Dashboard V1 (Multi-account management)
python3 dashboard.py  # http://localhost:5000

# Run Dashboard V2 (Detailed per-account view)
python3 dashboard_v2.py  # http://localhost:5001
```

### Configuration
| Task | File Location |
|------|---------------|
| Main settings | [`config/settings.yaml`](config/settings.yaml) |
| Multi-account config | [`config/accounts.yaml`](config/accounts.yaml) |
| Tweet templates | [`config/templates.yaml`](config/templates.yaml) |
| Target keywords | [`config/keywords.yaml`](config/keywords.yaml) |
| Account-specific config | `accounts/{account_id}/config/settings.yaml` |

### Adding/Managing Accounts
1. **Dashboard UI**: Open `http://localhost:5000/accounts`
   - Click "➕ Add Account"
   - Fill in account details + WhatsApp number
   - Upload cookies.json
   
2. **Manual**: See guide [`docs/guides/PANDUAN_TAMBAH_COOKIES.md`](docs/guides/PANDUAN_TAMBAH_COOKIES.md)

### Media & Images
| Guide | Location |
|-------|----------|
| Upload images | [`docs/guides/PANDUAN_UPLOAD_GAMBAR.md`](docs/guides/PANDUAN_UPLOAD_GAMBAR.md) |
| Media promo guide | [`docs/guides/PANDUAN_MEDIA_PROMO.md`](docs/guides/PANDUAN_MEDIA_PROMO.md) |
| Quick media start | [`docs/guides/QUICK_MEDIA_START.md`](docs/guides/QUICK_MEDIA_START.md) |

## 📚 Documentation by Category

### 👤 User Guides (`docs/guides/`)
- [`USAGE.md`](docs/guides/USAGE.md) - General usage guide
- [`CARA_PAKAI_AKRAB.md`](docs/guides/CARA_PAKAI_AKRAB.md) - Casual language mode
- [`PANDUAN_TAMBAH_COOKIES.md`](docs/guides/PANDUAN_TAMBAH_COOKIES.md) - Add cookies
- [`PANDUAN_UPLOAD_GAMBAR.md`](docs/guides/PANDUAN_UPLOAD_GAMBAR.md) - Upload images
- [`PANDUAN_MEDIA_PROMO.md`](docs/guides/PANDUAN_MEDIA_PROMO.md) - Promo media guide
- [`QUICK_MEDIA_START.md`](docs/guides/QUICK_MEDIA_START.md) - Quick media start
- [`MEDIA_OPTIONAL_GUIDE.md`](docs/guides/MEDIA_OPTIONAL_GUIDE.md) - Optional media guide

### 📊 Reports (`docs/reports/`)
- [`FINAL_SUMMARY.md`](docs/reports/FINAL_SUMMARY.md) - Implementation summary
- [`FINAL_TEST_RESULTS.md`](docs/reports/FINAL_TEST_RESULTS.md) - Test results
- [`SAFETY_REPORT.md`](docs/reports/SAFETY_REPORT.md) - Safety & rate limiting

### 🔧 Technical Docs (`docs/technical/`)
- [`DEVELOPMENT_PLAN.md`](docs/technical/DEVELOPMENT_PLAN.md) - Development roadmap
- [`NEW_TEMPLATE_SYSTEM.md`](docs/technical/NEW_TEMPLATE_SYSTEM.md) - Template system docs
- [`SOLUSI_ERROR_226.md`](docs/technical/SOLUSI_ERROR_226.md) - Error 226 solutions

## 🔍 Finding Specific Information

### I want to...
| Goal | Go to |
|------|-------|
| **Start using the bot** | [`QUICK_START.md`](QUICK_START.md) |
| **Add a new account** | Dashboard: `http://localhost:5000/accounts` |
| **See WhatsApp numbers** | Dashboard V2: `http://localhost:5001` |
| **View metrics per account** | Dashboard V2: `http://localhost:5001` |
| **Change bot settings** | [`config/settings.yaml`](config/settings.yaml) |
| **Customize tweet templates** | [`config/templates.yaml`](config/templates.yaml) |
| **Change target keywords** | [`config/keywords.yaml`](config/keywords.yaml) |
| **Upload promo images** | [`docs/guides/PANDUAN_UPLOAD_GAMBAR.md`](docs/guides/PANDUAN_UPLOAD_GAMBAR.md) |
| **Fix errors** | [`docs/technical/SOLUSI_ERROR_226.md`](docs/technical/SOLUSI_ERROR_226.md) |
| **Understand the code** | [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) |
| **See version history** | [`CHANGELOG.md`](CHANGELOG.md) |

## 📂 Important Directories

```
bot/                    # Bot source code
config/                 # Configuration files
accounts/               # Per-account data & configs
data/                   # Database (metrics.db)
media/promo/            # Promotional images/videos
templates/              # HTML templates (dashboard UI)
static/                 # CSS & JavaScript
docs/                   # All documentation
archive/                # Old files (can be ignored)
```

## 🆘 Need Help?

1. Check [`QUICK_START.md`](QUICK_START.md) for basic setup
2. Check [`docs/guides/`](docs/guides/) for user guides
3. Check [`docs/technical/`](docs/technical/) for technical issues
4. Check [`CHANGELOG.md`](CHANGELOG.md) for recent changes

## 🌐 Dashboard URLs

- **Dashboard V1** (Multi-account): http://localhost:5000
  - Account management: http://localhost:5000/accounts
- **Dashboard V2** (Per-account): http://localhost:5001
