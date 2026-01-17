# 🚀 QUICK START - Twitter Bot

Panduan cepat untuk mulai menggunakan bot dalam 5 menit!

## 📋 Prerequisites

- Python 3.14+
- Twitter account
- WhatsApp number untuk order

## ⚡ 5 Langkah Quick Start

### 1. Install Dependencies (1 menit)

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# atau: venv\Scripts\activate  # Windows

# Install dependencies (sudah include di venv)
# Jika perlu install ulang:
pip install -r requirements.txt
```

### 2. Setup Twitter Cookies (2 menit)

```bash
# Login ke Twitter di browser
# Install extension: EditThisCookie atau Cookie Editor
# Export cookies sebagai JSON
# Save ke file: cookies.json
```

### 3. Edit Config (1 menit)

Edit `config/settings.yaml`:

```yaml
business:
  wa_number: "085117557905"  # Ganti dengan nomor WA Anda
  wa_link: "https://wa.me/6285117557905?text=..."  # Ganti dengan link WA Anda
```

Edit `config/templates.yaml`:

```yaml
promo_templates:
  - text: "🔥 KUOTA XL 10GB cuma Rp25.000! Order: {wa_number}"
    media: null
  
  # Tambah template lain sesuai kebutuhan
```

### 4. Test Bot (30 detik)

```bash
# Test connection
python main.py --test

# Expected output:
# ✅ Connection test passed!
# Logged in as: @YourUsername
```

### 5. Run Bot (30 detik)

```bash
# Manual run (morning slot)
python main.py --run-once morning

# Atau auto mode (3x/day: 08:00, 13:00, 20:00)
python main.py --daemon
```

## 🎉 Done!

Bot sekarang sudah jalan! Cek Twitter untuk melihat hasil post.

---

## 📊 Monitoring

### Via Web Dashboard

```bash
# Start dashboard
python dashboard.py

# Open browser: http://localhost:5000
```

Dashboard features:
- Real-time metrics
- Tweet performance
- Follower growth chart
- Manual posting
- Config editor

### Via Logs

```bash
# Lihat logs
tail -f data/logs/bot.log
```

---

## 🎯 Tips Awal

### 1. Mulai dengan Manual Mode

Jangan langsung daemon mode. Test dulu manual:

```bash
python main.py --run-once morning
python main.py --run-once afternoon
python main.py --run-once evening
```

### 2. Monitor Rate Limits

Check rate limits via dashboard atau:

```bash
# Lihat daily stats
python3 -c "from bot.database import Database; db = Database(); print(db.get_daily_activity())"
```

### 3. Edit Templates On-the-Fly

Bot reload config otomatis setiap run. Edit `templates.yaml` kapan aja!

### 4. Use Media for Better Engagement

Add images to increase engagement:

```yaml
promo_templates:
  - text: "🔥 Promo!"
    media: "media/promo/promo1.jpg"  # Put your images here
```

---

## 🔧 Konfigurasi Lanjutan

### Switch ke XL Akrab

```bash
# Backup config
cp config/settings.yaml config/settings.yaml.backup

# Copy Akrab config
cp config/settings_akrab.yaml config/settings.yaml
cp config/templates_akrab.yaml config/templates.yaml

# Update WA number di settings.yaml
# Restart bot
```

### Schedule dengan Cron (Linux)

```bash
# Edit crontab
crontab -e

# Add:
0 8 * * * cd /path/to/twitter-bot && python main.py --run-once morning
0 13 * * * cd /path/to/twitter-bot && python main.py --run-once afternoon
0 20 * * * cd /path/to/twitter-bot && python main.py --run-once evening
```

### AI Configuration

Edit `config/settings.yaml`:

```yaml
ai:
  enabled: true  # Set false untuk disable AI
  api_url: "https://api.elrayyxml.web.id/api/ai/copilot"
  timeout: 10
```

---

## ❓ Troubleshooting Quick

### Bot tidak login?
- Cek cookies.json masih valid (max 30 hari)
- Re-export cookies dari browser
- Lihat: `docs/SOLUSI_ERROR_226.md`

### Tweet tidak muncul?
- Cek rate limits (max 10/day)
- Lihat logs: `data/logs/bot.log`
- Test manual: `python main.py --run-once morning`

### Dashboard error?
- Cek port 5000 tidak dipakai app lain
- Restart: `python dashboard.py`

---

## 📚 Dokumentasi Lengkap

Untuk panduan lengkap, lihat:

- **`docs/NEW_TEMPLATE_SYSTEM.md`** - Panduan template system
- **`docs/USAGE.md`** - Panduan penggunaan lengkap
- **`docs/CARA_PAKAI_AKRAB.md`** - Setup untuk XL Akrab
- **`README.md`** - Overview project

---

## 🎯 Next Steps

Setelah bot running:

1. ✅ Monitor metrics di dashboard
2. ✅ A/B test berbagai template
3. ✅ Track conversion (WA messages & orders)
4. ✅ Optimize template berdasarkan performance
5. ✅ Scale gradually (jangan spam!)

---

**Happy tweeting! 🚀**

Need help? Check `docs/` folder or create issue.
