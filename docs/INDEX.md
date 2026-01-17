# 📚 Documentation Index - Twitter Bot

Panduan lengkap untuk semua dokumentasi Twitter Bot.

---

## 🚀 Quick Navigation

### For First-Time Users
1. 📖 [Quick Start Guide](QUICK_START.md) - Setup bot dalam 10 menit
2. 🚀 [Deployment Guide](../DEPLOYMENT.md) - Deploy ke production dengan PM2
3. 📋 [Project Structure](PROJECT_STRUCTURE.md) - Struktur folder project

### For Existing Users
- 🎯 [User Guide](guides/USAGE.md) - Panduan lengkap penggunaan
- ⚙️ [Configuration](guides/) - Setup & konfigurasi
- 🔄 [Multi-Account Guide](migration/MULTI_ACCOUNT_RUNNING_GUIDE.md)

---

## 📁 Documentation Structure

```
docs/
├── 📄 Core Documentation
│   ├── QUICK_START.md              # Panduan setup awal
│   ├── PROJECT_STRUCTURE.md        # Struktur project
│   ├── CHANGELOG.md                # Version history
│   └── NAVIGATION.md               # Navigation helper
│
├── 🚀 Deployment
│   └── deployment/
│       ├── PM2_DEPLOYMENT_GUIDE.md # Full PM2 guide
│       ├── PM2_QUICK_START.md      # Quick PM2 setup
│       └── PM2_SUMMARY.txt         # Summary
│
├── 📚 User Guides
│   └── guides/
│       ├── USAGE.md                # Main user guide
│       ├── CARA_PAKAI_AKRAB.md     # Config Akrab guide
│       ├── PANDUAN_TAMBAH_COOKIES.md
│       ├── PANDUAN_MEDIA_PROMO.md
│       ├── PANDUAN_UPLOAD_GAMBAR.md
│       ├── MEDIA_OPTIONAL_GUIDE.md
│       └── QUICK_MEDIA_START.md
│
├── 🔄 Migration & Upgrade
│   └── migration/
│       ├── MULTI_ACCOUNT_RUNNING_GUIDE.md
│       ├── DASHBOARD_V2_UPGRADE.md
│       └── DASHBOARD_V2_FULL_MIGRATION.md
│
├── 🔧 Technical Documentation
│   └── technical/
│       ├── NEW_TEMPLATE_SYSTEM.md  # Template v2.0
│       ├── DEVELOPMENT_PLAN.md     # Roadmap
│       └── SOLUSI_ERROR_226.md     # Error solutions
│
└── 📊 Reports & Analytics
    └── reports/
        ├── FINAL_SUMMARY.md        # Project summary
        ├── FINAL_TEST_RESULTS.md   # Test results
        └── SAFETY_REPORT.md        # Safety features
```

---

## 🎯 Quick Links by Topic

### 🚀 Getting Started
| Topic | Document | Description |
|-------|----------|-------------|
| Setup Bot | [QUICK_START.md](QUICK_START.md) | Install & setup dalam 10 menit |
| Deploy Production | [DEPLOYMENT.md](../DEPLOYMENT.md) | Deploy dengan PM2 |
| Test Connection | [USAGE.md](guides/USAGE.md) | Test bot connection |

### ⚙️ Configuration
| Topic | Document | Description |
|-------|----------|-------------|
| Settings | [USAGE.md](guides/USAGE.md) | Configure settings.yaml |
| Templates | [NEW_TEMPLATE_SYSTEM.md](technical/NEW_TEMPLATE_SYSTEM.md) | Template system v2.0 |
| Keywords | [USAGE.md](guides/USAGE.md) | Setup target keywords |
| Cookies | [PANDUAN_TAMBAH_COOKIES.md](guides/PANDUAN_TAMBAH_COOKIES.md) | Add Twitter cookies |

### 📱 Multi-Account
| Topic | Document | Description |
|-------|----------|-------------|
| Setup Multi-Account | [MULTI_ACCOUNT_RUNNING_GUIDE.md](migration/MULTI_ACCOUNT_RUNNING_GUIDE.md) | Run multiple accounts |
| Account Management | [USAGE.md](guides/USAGE.md) | Manage accounts via dashboard |

### 🖼️ Media & Content
| Topic | Document | Description |
|-------|----------|-------------|
| Upload Media | [PANDUAN_MEDIA_PROMO.md](guides/PANDUAN_MEDIA_PROMO.md) | Upload promo images/videos |
| Media Guide | [MEDIA_OPTIONAL_GUIDE.md](guides/MEDIA_OPTIONAL_GUIDE.md) | Optional media guide |
| Quick Media | [QUICK_MEDIA_START.md](guides/QUICK_MEDIA_START.md) | Quick media setup |

### 🔧 Advanced
| Topic | Document | Description |
|-------|----------|-------------|
| Template System | [NEW_TEMPLATE_SYSTEM.md](technical/NEW_TEMPLATE_SYSTEM.md) | New template format |
| Development | [DEVELOPMENT_PLAN.md](technical/DEVELOPMENT_PLAN.md) | Roadmap & plans |
| Error Solutions | [SOLUSI_ERROR_226.md](technical/SOLUSI_ERROR_226.md) | Common error fixes |

### 📊 Monitoring & Reports
| Topic | Document | Description |
|-------|----------|-------------|
| Safety Features | [SAFETY_REPORT.md](reports/SAFETY_REPORT.md) | Rate limits & safety |
| Test Results | [FINAL_TEST_RESULTS.md](reports/FINAL_TEST_RESULTS.md) | Testing results |
| Project Summary | [FINAL_SUMMARY.md](reports/FINAL_SUMMARY.md) | Overall summary |

---

## 🆘 Troubleshooting by Issue

### Bot Issues
- **Bot tidak posting** → [DEPLOYMENT.md - Troubleshooting](../DEPLOYMENT.md#troubleshooting)
- **Cookies expired** → [PANDUAN_TAMBAH_COOKIES.md](guides/PANDUAN_TAMBAH_COOKIES.md)
- **Rate limit exceeded** → [SAFETY_REPORT.md](reports/SAFETY_REPORT.md)
- **Error 226** → [SOLUSI_ERROR_226.md](technical/SOLUSI_ERROR_226.md)

### Dashboard Issues
- **Dashboard tidak bisa diakses** → [DEPLOYMENT.md - Issue 2](../DEPLOYMENT.md#issue-2-dashboard-not-accessible)
- **Multi-account error** → [MULTI_ACCOUNT_RUNNING_GUIDE.md](migration/MULTI_ACCOUNT_RUNNING_GUIDE.md)

### Configuration Issues
- **Template error** → [NEW_TEMPLATE_SYSTEM.md](technical/NEW_TEMPLATE_SYSTEM.md)
- **Media not found** → [PANDUAN_MEDIA_PROMO.md](guides/PANDUAN_MEDIA_PROMO.md)

---

## 📖 Reading Path

### Path 1: Beginner (First Time Setup)
1. Read: [QUICK_START.md](QUICK_START.md)
2. Read: [PANDUAN_TAMBAH_COOKIES.md](guides/PANDUAN_TAMBAH_COOKIES.md)
3. Optional: [PANDUAN_MEDIA_PROMO.md](guides/PANDUAN_MEDIA_PROMO.md)
4. Run: `python main.py --test`
5. Run: `python main.py --run-once morning`

### Path 2: Deploy to Production
1. Read: [DEPLOYMENT.md](../DEPLOYMENT.md)
2. Read: [PM2_QUICK_START.md](deployment/PM2_QUICK_START.md)
3. Run: `pm2 start ecosystem.config.js`
4. Monitor: `pm2 logs` dan `pm2 monit`

### Path 3: Multi-Account Setup
1. Read: [MULTI_ACCOUNT_RUNNING_GUIDE.md](migration/MULTI_ACCOUNT_RUNNING_GUIDE.md)
2. Setup: `config/accounts.yaml`
3. Create: Account folders structure
4. Add: Cookies per account
5. Run: Multi-account runner

### Path 4: Advanced Customization
1. Read: [NEW_TEMPLATE_SYSTEM.md](technical/NEW_TEMPLATE_SYSTEM.md)
2. Read: [USAGE.md](guides/USAGE.md)
3. Customize: Templates, keywords, settings
4. Test: Via dashboard preview
5. Deploy: Apply changes

---

## 🔄 Version History

See [CHANGELOG.md](CHANGELOG.md) for full version history.

**Current Version**: 2.0  
**Major Changes**:
- ✅ Simplified template system
- ✅ Multi-account support
- ✅ PM2 deployment ready
- ✅ Dashboard V2
- ✅ Media per template

---

## 📞 Support

### Need Help?
1. **Check docs first** - Search in docs/ folder
2. **Check troubleshooting** - [DEPLOYMENT.md](../DEPLOYMENT.md)
3. **Check logs** - `pm2 logs` atau `data/logs/`
4. **Test manually** - `python main.py --test`

### Report Issues
- Check: [FINAL_TEST_RESULTS.md](reports/FINAL_TEST_RESULTS.md)
- Review: [SAFETY_REPORT.md](reports/SAFETY_REPORT.md)

---

## 🎓 Contributing

Want to improve documentation?
1. Fork repository
2. Edit documentation in `docs/`
3. Submit pull request
4. Follow markdown style guide

---

**Last Updated**: 2026-01-17  
**Documentation Version**: 2.0  
**Maintainer**: Twitter Bot Team
