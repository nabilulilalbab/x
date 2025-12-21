# 🚀 DEVELOPMENT PLAN: Twitter Bot Jualan Kuota XL

**Project:** Safe Twitter Promotion Bot for Kuota XL
**Approach:** Hybrid (80% Manual + 20% Automation)
**Target:** 300-500 followers dalam 30 hari (Realistic)
**Schedule:** 3x/hari (08:00, 13:00, 20:00)

---

## 📋 PROJECT OVERVIEW

### Goals:
1. ✅ Bot promosi yang AMAN (tidak kena ban)
2. ✅ Template DINAMIS (bisa diubah sesuka hati)
3. ✅ AI-powered content improvement (no overclaim)
4. ✅ Metrics tracking AKURAT
5. ✅ Easy to use & maintain

### Tech Stack:
- **Language:** Python 3.14
- **Twitter Library:** Twikit v2.3.3
- **HTTP Client:** httpx (with timeout config)
- **AI API:** ElrayyXml Copilot API
- **Config Format:** YAML (easy to edit)
- **Metrics:** SQLite database (simple & portable)

---

## 🏗️ ARCHITECTURE

```
twitter-kuota-bot/
├── config/
│   ├── settings.yaml          # Main configuration (EDITABLE!)
│   ├── templates.yaml          # Tweet templates (EDITABLE!)
│   ├── keywords.yaml           # Search keywords (EDITABLE!)
│   └── schedule.yaml           # Posting schedule (EDITABLE!)
├── bot/
│   ├── __init__.py
│   ├── client.py              # Twitter client wrapper
│   ├── automation.py          # Bot automation logic
│   ├── content_generator.py   # AI-powered content
│   ├── metrics.py             # Metrics tracking
│   └── safety.py              # Rate limiter & safety
├── data/
│   ├── cookies.json           # Twitter auth
│   ├── metrics.db             # SQLite metrics
│   └── logs/                  # Activity logs
├── media/
│   └── promo/                 # Images/videos for tweets
├── main.py                    # Main entry point
├── run_scheduled.py           # Cron job runner
└── dashboard.py               # Simple web dashboard (optional)
```

---

## ⚙️ CORE FEATURES

### 1. DYNAMIC TEMPLATE SYSTEM

**File:** `config/templates.yaml`

```yaml
# USER EDITABLE - Ubah sesuka hati!

promo_templates:
  - "🔥 KUOTA XL MURAH! {paket} cuma {harga}! Hemat {diskon}%! 📲 WA: {wa_number}"
  - "📱 Stok ready! {paket} = {harga} aja! Order sekarang: {wa_link}"
  - "⚡ Flash Sale! {paket} diskon jadi {harga}! Limited! 🔥 {wa_number}"
  
value_templates:
  - "Tips hemat kuota #{number}: {tip_content}"
  - "Review sinyal XL di {location}: {review_content}"
  - "Tutorial: {tutorial_title} - {tutorial_content}"

engagement_templates:
  - "{reaction} banget!"
  - "Setuju! {additional_comment}"
  - "Menarik perspektifnya 🤔"

# Variables akan di-fill otomatis dari config
variables:
  paket: ["10GB", "25GB", "Unlimited"]
  harga: ["Rp25.000", "Rp50.000", "Rp75.000"]
  diskon: ["30", "40", "50"]
  wa_number: "08xxx-xxxx-xxxx"
  wa_link: "wa.me/628xxxxxxxxx"
```

### 2. AI CONTENT IMPROVEMENT

**API Integration:** ElrayyXml Copilot
**Endpoint:** `https://api.elrayyxml.web.id/api/ai/copilot?text={text}`

**Flow:**
```
1. Load template dari templates.yaml
2. Fill variables → Raw tweet
3. Send ke AI API → "Improve tweet ini: [raw_tweet]. 
   Requirements: casual, menarik, tidak overclaim, max 280 char"
4. Get improved tweet
5. Post to Twitter
```

**Features:**
- ✅ Auto-improve grammar & tone
- ✅ Make it more engaging
- ✅ Remove overclaim language
- ✅ Keep under 280 characters
- ✅ Maintain brand voice

### 3. ACCURATE METRICS TRACKING

**Database:** SQLite (`data/metrics.db`)

**Tables:**

```sql
-- Daily activity
CREATE TABLE daily_activity (
    id INTEGER PRIMARY KEY,
    date DATE,
    tweets_posted INTEGER DEFAULT 0,
    likes_given INTEGER DEFAULT 0,
    replies_made INTEGER DEFAULT 0,
    follows_made INTEGER DEFAULT 0,
    retweets_made INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tweet performance
CREATE TABLE tweet_performance (
    id INTEGER PRIMARY KEY,
    tweet_id TEXT UNIQUE,
    tweet_text TEXT,
    posted_at TIMESTAMP,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    retweets INTEGER DEFAULT 0,
    replies INTEGER DEFAULT 0,
    engagement_rate FLOAT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Follower growth
CREATE TABLE follower_growth (
    id INTEGER PRIMARY KEY,
    date DATE,
    followers_count INTEGER,
    following_count INTEGER,
    ratio FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- WA conversions (manual input)
CREATE TABLE conversions (
    id INTEGER PRIMARY KEY,
    date DATE,
    wa_messages INTEGER DEFAULT 0,
    orders INTEGER DEFAULT 0,
    revenue FLOAT DEFAULT 0,
    source TEXT DEFAULT 'twitter',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Search keywords performance
CREATE TABLE keyword_performance (
    id INTEGER PRIMARY KEY,
    keyword TEXT,
    date DATE,
    tweets_found INTEGER DEFAULT 0,
    engaged INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Metrics to Track:**
- Daily: Tweets, likes, replies, follows, retweets
- Tweet: Views, likes, RTs, replies, engagement rate
- Growth: Followers, following, ratio
- Business: WA messages, orders, revenue
- Keywords: Performance per keyword

### 4. SAFETY & RATE LIMITING

**Config:** `config/settings.yaml`

```yaml
safety:
  rate_limits:
    tweets_per_hour: 5
    tweets_per_day: 10
    follows_per_hour: 5
    follows_per_day: 15
    likes_per_hour: 10
    likes_per_day: 30
    replies_per_hour: 5
    replies_per_day: 10
    
  delays:
    min_delay: 10  # seconds
    max_delay: 30  # seconds
    after_tweet: [30, 60]  # longer delay after posting
    after_follow: [20, 45]
    after_error: [60, 180]
    
  warnings:
    follower_ratio_min: 0.1  # following/followers min ratio
    engagement_rate_min: 0.01  # min engagement to continue
```

### 5. SCHEDULING SYSTEM

**Config:** `config/schedule.yaml`

```yaml
schedule:
  timezone: "Asia/Jakarta"
  
  slots:
    morning:
      time: "08:00"
      enabled: true
      actions:
        - type: "post_tweet"
          template_type: "promo"
          use_ai: true
        - type: "search_engage"
          keywords: ["butuh kuota xl", "kuota xl murah"]
          max_engage: 5
        - type: "follow_users"
          max_follow: 5
          
    afternoon:
      time: "13:00"
      enabled: true
      actions:
        - type: "post_tweet"
          template_type: "value"
          use_ai: true
        - type: "search_engage"
          keywords: ["kuota habis", "paket internet murah"]
          max_engage: 5
          
    evening:
      time: "20:00"
      enabled: true
      actions:
        - type: "post_tweet"
          template_type: "promo"
          use_ai: true
        - type: "engage_followers"
          max_engage: 3
        - type: "check_mentions"
```

---

## 🎨 USER CONFIGURATION FILES

### `config/settings.yaml` (Main Config)

```yaml
# ============================================
# MAIN SETTINGS - EDIT SESUKA HATI!
# ============================================

account:
  cookies_file: "data/cookies.json"
  
business:
  product: "Kuota XL"
  niche: "pulsa_kuota"
  wa_number: "08xxx-xxxx-xxxx"
  wa_link: "wa.me/628xxxxxxxxx?text=Halo%20mau%20order%20kuota"
  
  prices:
    - paket: "10GB"
      harga: "Rp25.000"
      harga_normal: "Rp45.000"
      diskon: 44
    - paket: "25GB"
      harga: "Rp50.000"
      harga_normal: "Rp90.000"
      diskon: 44
    - paket: "Unlimited"
      harga: "Rp75.000"
      harga_normal: "Rp120.000"
      diskon: 37

targets:
  followers_30days: 500
  engagement_rate_target: 0.02  # 2%
  daily_orders_target: 2

ai:
  enabled: true
  api_url: "https://api.elrayyxml.web.id/api/ai/copilot"
  improve_prompt: |
    Improve tweet ini menjadi lebih menarik dan casual untuk target audience mahasiswa/pekerja Indonesia.
    Requirements:
    - Bahasa Indonesia casual tapi sopan
    - Tidak overclaim atau berlebihan
    - Maksimal 280 karakter
    - Gunakan emoji yang tepat (max 3)
    - Fokus pada value proposition
    
    Original tweet: {tweet}
    
    Berikan HANYA improved tweet tanpa penjelasan.

safety:
  # Copy from section 4 above
  
# Continue with other settings...
```

---

## 📊 METRICS DASHBOARD

### Real-time Metrics Display

**Command:** `python dashboard.py`

**Output:**
```
╔════════════════════════════════════════════════════════════╗
║        TWITTER BOT METRICS - Kuota XL                      ║
╚════════════════════════════════════════════════════════════╝

📅 DATE: 2025-12-21

┌─────────────────────────────────────────────────────────────┐
│  📊 TODAY'S ACTIVITY                                        │
└─────────────────────────────────────────────────────────────┘
  Tweets Posted:    3/10   ███████░░░  30%
  Likes Given:     15/30   ██████████  50%
  Replies Made:     5/10   ███████░░░  50%
  Follows Made:     8/15   █████████░  53%
  
┌─────────────────────────────────────────────────────────────┐
│  📈 GROWTH METRICS                                          │
└─────────────────────────────────────────────────────────────┘
  Current Followers:    245
  New Today:            +12
  Following:            380
  Ratio:                0.64 ✅
  
  30-Day Target:        500 followers
  Progress:             49% ████████░░
  Days Remaining:       15
  Avg Growth/Day:       16.3 followers
  
┌─────────────────────────────────────────────────────────────┐
│  🎯 ENGAGEMENT METRICS (Last 7 Days)                        │
└─────────────────────────────────────────────────────────────┘
  Total Tweets:         21
  Avg Views/Tweet:      850
  Avg Likes/Tweet:      18
  Avg Engagement Rate:  2.1% ✅
  
  Best Tweet (12/19):
  "🔥 PROMO: 25GB cuma 50rb..."
  └─ Views: 1,450 | Likes: 45 | RTs: 12 | Engagement: 3.9%
  
┌─────────────────────────────────────────────────────────────┐
│  💰 BUSINESS METRICS                                        │
└─────────────────────────────────────────────────────────────┘
  WA Messages (Today):     5
  Orders (Today):          2
  Conversion Rate:        40% ✅
  
  This Week:
  └─ Messages: 28 | Orders: 11 | Revenue: Rp550.000
  
  This Month:
  └─ Messages: 95 | Orders: 38 | Revenue: Rp1.900.000
  
┌─────────────────────────────────────────────────────────────┐
│  🔍 KEYWORD PERFORMANCE (Last 7 Days)                       │
└─────────────────────────────────────────────────────────────┘
  1. "butuh kuota xl"      - 23 found, 15 engaged (65%)
  2. "kuota xl murah"      - 18 found, 12 engaged (67%)
  3. "kuota habis"         - 45 found, 20 engaged (44%)
  4. "beli kuota xl"       - 12 found, 10 engaged (83%) ⭐
  5. "paket internet"      -  8 found,  5 engaged (62%)
  
┌─────────────────────────────────────────────────────────────┐
│  ⚠️  ALERTS                                                 │
└─────────────────────────────────────────────────────────────┘
  ✅ All systems normal
  ✅ Rate limits: Safe
  ✅ Engagement rate: Above target
  ✅ Growth on track
  
┌─────────────────────────────────────────────────────────────┐
│  🎯 RECOMMENDATIONS                                         │
└─────────────────────────────────────────────────────────────┘
  1. Keyword "beli kuota xl" has highest engagement (83%)
     → Increase search frequency for this keyword
     
  2. Evening tweets perform 25% better than morning
     → Consider adding 4th slot at 22:00
     
  3. Tweets with price comparison get 2x engagement
     → Use more comparison templates
     
╚════════════════════════════════════════════════════════════╝

Last updated: 2025-12-21 20:35:42
Auto-refresh in 60s... (Ctrl+C to exit)
```

---

## 🔄 WORKFLOW

### Daily Automated Flow:

```
08:00 - MORNING SLOT
├─ 1. Load morning schedule
├─ 2. Generate promo tweet from template
├─ 3. Improve with AI API
├─ 4. Post tweet
├─ 5. Wait 30-60s
├─ 6. Search "butuh kuota xl" (max 5 engage)
│     ├─ Like relevant tweets
│     └─ Soft reply if appropriate
├─ 7. Wait 20-45s between actions
├─ 8. Follow 5 target users
├─ 9. Log all activity to metrics.db
└─ 10. Update dashboard

13:00 - AFTERNOON SLOT
├─ 1. Load afternoon schedule
├─ 2. Generate value content tweet
├─ 3. Improve with AI API
├─ 4. Post tweet
├─ 5. Wait 30-60s
├─ 6. Search "kuota habis" (max 5 engage)
├─ 7. Engage with results
└─ 8. Log activity

20:00 - EVENING SLOT
├─ 1. Load evening schedule
├─ 2. Generate promo tweet
├─ 3. Improve with AI API
├─ 4. Post tweet
├─ 5. Wait 30-60s
├─ 6. Engage with own followers (like their tweets)
├─ 7. Check & reply mentions (MANUAL RECOMMENDED!)
├─ 8. Daily metrics summary
└─ 9. Generate recommendations
```

---

## 🛠️ IMPLEMENTATION PLAN

### Phase 1: Core Infrastructure (Day 1-2)
- [ ] Setup project structure
- [ ] Create config system (YAML loader)
- [ ] Setup SQLite database & tables
- [ ] Twitter client wrapper (Twikit + httpx)
- [ ] Rate limiter & safety module

### Phase 2: Template & AI System (Day 2-3)
- [ ] Dynamic template loader
- [ ] Variable substitution system
- [ ] AI API integration (ElrayyXml)
- [ ] Content generator with AI improvement
- [ ] Testing with sample tweets

### Phase 3: Automation Logic (Day 3-4)
- [ ] Search & engage module
- [ ] Follow/like/retweet logic
- [ ] Schedule system (cron-like)
- [ ] Error handling & retry
- [ ] Activity logger

### Phase 4: Metrics System (Day 4-5)
- [ ] Metrics collector
- [ ] Database operations
- [ ] Dashboard display (terminal UI)
- [ ] Analytics & recommendations
- [ ] Export reports (CSV/JSON)

### Phase 5: Testing & Refinement (Day 5-7)
- [ ] Test with real Twitter account
- [ ] Monitor for issues
- [ ] Fine-tune rate limits
- [ ] Optimize AI prompts
- [ ] Documentation

---

## 📝 USAGE INSTRUCTIONS

### Setup:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup cookies
# Login ke Twitter via browser, export cookies.json

# 3. Edit config
nano config/settings.yaml
# - Set wa_number
# - Set prices
# - Adjust targets

nano config/templates.yaml
# - Customize tweet templates

# 4. Test connection
python main.py --test

# 5. Run once manually
python main.py --run-once

# 6. View metrics
python dashboard.py
```

### Running:
```bash
# Manual run (test)
python main.py --run-once

# Schedule with cron (Linux)
crontab -e
# Add:
# 0 8,13,20 * * * cd /path/to/bot && python run_scheduled.py

# Or run as daemon (background)
python main.py --daemon

# View logs
tail -f data/logs/bot.log
```

### Editing Templates:
```bash
# Edit templates anytime
nano config/templates.yaml

# Bot will reload automatically on next run
# No need to restart!
```

### Manual Metrics Input:
```bash
# Add conversion data (orders dari WA)
python main.py --add-conversion --orders 3 --revenue 150000

# Update tweet stats manually
python main.py --update-tweet TWEET_ID --views 1500 --likes 45
```

---

## 🔒 SAFETY FEATURES

1. **Rate Limiting:** Strict limits per hour/day
2. **Random Delays:** 10-30s between actions
3. **Error Recovery:** Auto-retry with exponential backoff
4. **Activity Logging:** All actions logged for audit
5. **Health Checks:** Monitor account status
6. **Safe Mode:** Auto-pause if suspicious activity detected
7. **Backup System:** Auto-backup config & metrics daily

---

## 📈 SUCCESS CRITERIA

### Week 1-2:
- [ ] 50-150 followers
- [ ] Avg engagement rate >1%
- [ ] 0 warnings from Twitter
- [ ] 1-3 WA messages from Twitter

### Week 3-4:
- [ ] 150-300 followers
- [ ] Avg engagement rate >1.5%
- [ ] 3-5 WA messages/week
- [ ] 1-2 orders/week from Twitter

### Month 2:
- [ ] 300-500 followers
- [ ] Avg engagement rate >2%
- [ ] 10-15 WA messages/week
- [ ] 3-5 orders/week from Twitter
- [ ] Sustainable growth without manual intervention

---

## 🎯 NEXT STEPS

1. ✅ Review this development plan
2. ❓ Get approval & clarifications
3. 🛠️ Start implementation (Phase 1)
4. 🧪 Testing
5. 🚀 Launch!

---

**Ready to proceed with implementation?**
