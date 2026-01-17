# 📖 USAGE GUIDE - Twitter Bot Kuota XL

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Cookies

Export cookies dari browser setelah login ke Twitter/X, simpan sebagai `cookies.json` di root folder.

### 3. Configure Settings

Edit file konfigurasi:

```bash
# Edit settings utama
nano config/settings.yaml

# Edit template tweets
nano config/templates.yaml

# Edit keywords untuk search
nano config/keywords.yaml
```

**Minimum yang harus diubah:**
- `wa_number`: Nomor WhatsApp Anda
- `wa_link`: Link WA Anda
- `prices`: Harga kuota Anda

### 4. Test Connection

```bash
python main.py --test
```

Output jika sukses:
```
✅ Connection test passed!
   Logged in as: @YourUsername
   Followers: 123
   Following: 456
```

---

## 🎮 Running the Bot

### Option 1: Web Dashboard (RECOMMENDED)

```bash
python dashboard.py
```

Buka browser: **http://localhost:5000**

Features:
- ✅ Real-time monitoring
- ✅ Start/stop bot
- ✅ View metrics & charts
- ✅ Manual slot triggers
- ✅ Add conversion data
- ✅ Activity logs

### Option 2: Manual Run (One Slot)

```bash
# Run morning slot (08:00 content)
python main.py --run-once morning

# Run afternoon slot (13:00 content)
python main.py --run-once afternoon

# Run evening slot (20:00 content)
python main.py --run-once evening
```

### Option 3: Scheduled Mode (Daemon)

```bash
python main.py --daemon
```

Bot akan jalan otomatis sesuai schedule di `config/settings.yaml`:
- Morning: 08:00
- Afternoon: 13:00
- Evening: 20:00

---

## ⚙️ Configuration

### `config/settings.yaml`

**Business Settings:**
```yaml
business:
  wa_number: "08xxx-xxxx-xxxx"  # GANTI INI!
  wa_link: "https://wa.me/628xxx"  # GANTI INI!
  
  prices:  # Edit harga sesuai kebutuhan
    - paket: "10GB"
      harga_display: "Rp25.000"
      diskon: 44
```

**Safety Limits:**
```yaml
safety:
  rate_limits:
    tweets_per_day: 10    # Max tweets per hari
    follows_per_day: 15   # Max follows per hari
    likes_per_day: 30     # Max likes per hari
```

**AI Settings:**
```yaml
ai:
  enabled: true  # Set false untuk disable AI
  api_url: "https://api.elrayyxml.web.id/api/ai/copilot"
```

**Schedule:**
```yaml
schedule:
  morning:
    time: "08:00"
    enabled: true  # Set false untuk disable
  afternoon:
    time: "13:00"
    enabled: true
  evening:
    time: "20:00"
    enabled: true
```

### `config/templates.yaml`

**Promo Templates:**
```yaml
promo_templates:
  - "🔥 KUOTA XL MURAH! {paket} cuma {harga}!"
  - "📱 Stok ready! {paket} = {harga} aja!"
  # Tambah template sendiri!
```

Variables yang tersedia:
- `{paket}` - 10GB, 25GB, Unlimited
- `{harga}` - Rp25.000, dll
- `{harga_normal}` - Harga normal
- `{diskon}` - Persentase diskon
- `{wa_number}` - Nomor WA
- `{wa_link}` - Link WA

**Value Templates:**
```yaml
value_templates:
  - "💡 Tips hemat kuota #{number}: {tip}"
  - "📊 Review sinyal XL di {location}: {review}"
  # Tambah template sendiri!
```

**Tips, FAQs, Facts:**
```yaml
tips:
  - "Matikan auto-play video untuk hemat kuota!"
  - "Download offline maps sebelum pergi!"
  # Tambah tips sendiri!
```

### `config/keywords.yaml`

**High Intent Keywords:**
```yaml
high_intent:
  - "butuh kuota xl"
  - "jual kuota xl"
  - "kuota xl murah"
  # Tambah keyword sendiri!
```

Bot akan search keywords ini dan engage (like) dengan tweets yang relevan.

---

## 📊 Metrics & Tracking

### Database Location

Semua metrics disimpan di: `data/metrics.db` (SQLite)

### Metrics yang di-track:

1. **Daily Activity**
   - Tweets posted
   - Likes given
   - Replies made
   - Follows made
   - Retweets made

2. **Tweet Performance**
   - Views
   - Likes
   - Retweets
   - Replies
   - Engagement rate

3. **Follower Growth**
   - Daily follower count
   - Following count
   - Ratio
   - New followers

4. **Business Metrics**
   - WA messages
   - Orders
   - Revenue

5. **Keyword Performance**
   - Tweets found
   - Engaged count
   - Conversion rate

### Manual Input Conversion

Via web dashboard atau API:

```bash
curl -X POST http://localhost:5000/api/conversion/add \
  -H "Content-Type: application/json" \
  -d '{
    "wa_messages": 5,
    "orders": 2,
    "revenue": 100000,
    "notes": "From Twitter promo"
  }'
```

---

## 🔧 Maintenance

### Update Templates

Edit `config/templates.yaml` kapan saja. Bot akan reload otomatis di run berikutnya.

```bash
nano config/templates.yaml
# Edit templates
# Save & exit
# Templates akan ter-update di next run
```

### Update Prices

```bash
nano config/settings.yaml
# Edit prices section
# Save & exit
```

### View Logs

```bash
tail -f data/logs/bot.log
```

### Backup Database

```bash
cp data/metrics.db data/metrics_backup_$(date +%Y%m%d).db
```

---

## 🛡️ Safety Guidelines

### DO's ✅

- ✅ Follow rate limits (10 tweets/day, 15 follows/day)
- ✅ Use random delays (configured automatically)
- ✅ Reply mentions manually (personal touch!)
- ✅ Monitor metrics daily
- ✅ Update templates regularly for variety
- ✅ Engage genuinely with audience

### DON'Ts ❌

- ❌ Don't increase rate limits (risk of ban!)
- ❌ Don't auto-reply mentions (looks like bot!)
- ❌ Don't spam same content repeatedly
- ❌ Don't DM people (high risk!)
- ❌ Don't ignore Twitter warnings
- ❌ Don't run 24/7 without monitoring

### If Account Gets Warning:

1. **STOP BOT IMMEDIATELY**
2. Review what triggered the warning
3. Reduce rate limits
4. Take a break (24-48 hours)
5. Resume with more conservative settings

---

## 🎯 Daily Workflow

### Morning (5 minutes)
1. Check web dashboard
2. Reply to mentions manually
3. Check WA messages
4. Bot auto-posts morning content

### Afternoon (5 minutes)
1. Check metrics
2. Reply to new mentions
3. Bot auto-posts afternoon content

### Evening (10 minutes)
1. Check daily stats
2. Reply to mentions
3. Handle WA orders
4. Bot auto-posts evening content
5. Review performance

**Total time: 20 minutes/day**
**Bot handles: Posting, searching, liking, following (automated)**
**You handle: Replies, sales, strategy (manual)**

---

## 🆘 Troubleshooting

### Bot won't start

```bash
# Check cookies valid
python main.py --test

# Check config files
cat config/settings.yaml

# Check logs
tail -n 50 data/logs/bot.log
```

### Tweets not posting

- Check rate limit: Max 10 tweets/day
- Check cookies not expired
- Check AI API working (if enabled)

### Dashboard not loading

```bash
# Check Flask running
python dashboard.py

# Check port not in use
lsof -i :5000
```

### AI not improving tweets

- Check `ai.enabled: true` in settings
- Check AI API URL correct
- Test AI API manually:
  ```bash
  curl "https://api.elrayyxml.web.id/api/ai/copilot?text=hello"
  ```
- Set `ai.enabled: false` to disable temporarily

---

## 📞 Support

### Common Issues:

**"Connection test failed"**
→ Cookies expired. Export cookies baru dari browser.

**"Rate limit reached"**
→ Normal! Bot akan skip sampai limit reset.

**"AI API timeout"**
→ AI API down. Bot akan post original tweet tanpa improvement.

**"Tweet too long"**
→ Edit template, kurangi text length.

### Configuration Examples:

**Conservative (Very Safe):**
```yaml
safety:
  rate_limits:
    tweets_per_day: 5
    follows_per_day: 10
    likes_per_day: 20
```

**Moderate (Balanced):**
```yaml
safety:
  rate_limits:
    tweets_per_day: 10
    follows_per_day: 15
    likes_per_day: 30
```

**Aggressive (Risky - Not Recommended):**
```yaml
safety:
  rate_limits:
    tweets_per_day: 15
    follows_per_day: 20
    likes_per_day: 50
```

---

## 🎓 Tips for Success

1. **Week 1-2: Build Trust**
   - Focus on value content (70%)
   - Minimal promo (30%)
   - Reply all mentions personally
   - Aim for 50-150 followers

2. **Week 3-4: Increase Engagement**
   - Balance value & promo (60/40)
   - Join relevant conversations
   - Use trending hashtags (max 3)
   - Aim for 150-300 followers

3. **Month 2+: Optimize**
   - Balance value & promo (50/50)
   - Leverage social proof (testimonials)
   - Run flash sales
   - Aim for 300-500 followers

4. **Content Strategy**
   - Morning: Product promo
   - Afternoon: Value content (tips, tutorials)
   - Evening: Product promo with urgency

5. **Conversion Optimization**
   - Make WA link prominent
   - Use price anchoring (show savings)
   - Add urgency (limited stock)
   - Showcase testimonials

---

## 🔄 Updates & Maintenance

### Weekly Tasks:
- [ ] Review metrics in dashboard
- [ ] Update templates if needed
- [ ] Check keyword performance
- [ ] Adjust strategy based on data

### Monthly Tasks:
- [ ] Backup database
- [ ] Review & clean old logs
- [ ] Update prices if needed
- [ ] Analyze conversion trends

---

## 📝 Changelog

### v1.0.0 (Current)
- ✅ Dynamic template system
- ✅ AI-powered content improvement
- ✅ SQLite metrics tracking
- ✅ Web dashboard with charts
- ✅ Safety rate limiting
- ✅ Scheduled automation
- ✅ Manual triggers
- ✅ Activity logging

---

**Happy Selling! 🚀**
