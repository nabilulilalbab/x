# 📁 Project Structure

```
twitter-bot/
├── 📄 Core Files
│   ├── main.py                 # Main bot entry point
│   ├── dashboard.py            # Dashboard V1 (Port 5000)
│   ├── dashboard_v2.py         # Dashboard V2 (Port 5001)
│   ├── requirements.txt        # Python dependencies
│   └── cookies.json            # Twitter session cookies
│
├── 🤖 Bot Modules (bot/)
│   ├── ai_client.py           # AI integration
│   ├── automation.py          # Core automation logic
│   ├── config_loader.py       # Configuration loader
│   ├── content_generator.py   # Content generation
│   ├── database.py            # Database operations
│   ├── twitter_client.py      # Twitter API client
│   ├── account_manager.py     # Multi-account management
│   └── multi_account_runner.py # Multi-account runner
│
├── ⚙️ Configuration (config/)
│   ├── settings.yaml          # Main settings
│   ├── templates.yaml         # Tweet templates
│   ├── keywords.yaml          # Target keywords
│   ├── accounts.yaml          # Multi-account config
│   └── settings_akrab.yaml    # Casual language variant
│
├── 👤 Account Folders (accounts/)
│   ├── account1_Username/
│   │   ├── config/            # Account-specific config
│   │   ├── cookies.json       # Account cookies
│   │   ├── data/              # Account metrics
│   │   └── media/             # Account media
│   └── account2_Username/
│       └── ...
│
├── 🎨 Web Interface
│   ├── templates/             # HTML templates
│   │   ├── dashboard.html     # Dashboard V1 UI
│   │   ├── dashboard_v2.html  # Dashboard V2 UI
│   │   └── accounts.html      # Multi-account UI
│   └── static/                # CSS & JavaScript
│       ├── css/dashboard.css
│       └── js/
│           ├── dashboard.js
│           └── app_v2.js
│
├── 📊 Data
│   └── data/
│       └── metrics.db         # SQLite database
│
├── 🖼️ Media
│   └── media/promo/           # Promotional images/videos
│
├── 📚 Documentation (docs/)
│   ├── guides/                # User guides
│   ├── reports/               # Test results & reports
│   ├── technical/             # Technical documentation
│   └── README.md
│
├── 📦 Archive (archive/)
│   ├── docs/                  # Old documentation
│   ├── scripts/               # Utility scripts
│   └── backups/               # Backup files
│
└── 📖 Main Documentation
    ├── README.md              # Project overview
    ├── QUICK_START.md         # Quick start guide
    ├── CHANGELOG.md           # Version history
    └── PROJECT_STRUCTURE.md   # This file
```

## 🚀 Quick Access

### Dashboards
- **Dashboard V1**: `http://localhost:5000` - Multi-account management
- **Dashboard V2**: `http://localhost:5001` - Per-account detailed view

### Main Scripts
- Start bot: `python3 main.py`
- Start Dashboard V1: `python3 dashboard.py`
- Start Dashboard V2: `python3 dashboard_v2.py`

### Configuration
- Main config: `config/settings.yaml`
- Account config: `config/accounts.yaml`
- Templates: `config/templates.yaml`

### Documentation
- Quick Start: `QUICK_START.md`
- User Guides: `docs/guides/`
- Technical Docs: `docs/technical/`

## 📝 Notes

- `archive/` folder is excluded from git
- Each account has isolated config and data
- Database stores all metrics and analytics
- Media files support images and videos
