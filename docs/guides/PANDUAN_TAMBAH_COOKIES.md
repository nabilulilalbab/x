# 🍪 PANDUAN MENAMBAHKAN COOKIES

Panduan lengkap cara menambahkan cookies untuk account baru di multi-account bot.

---

## 🎯 KENAPA PERLU COOKIES?

Cookies digunakan untuk:
- ✅ Login ke Twitter tanpa username/password setiap kali
- ✅ Menjaga session tetap aktif
- ✅ Bypass rate limiting login
- ✅ Authentikasi API calls

**Satu cookies = Satu account Twitter**

---

## 📝 LANGKAH-LANGKAH

### **Step 1: Buat Account di Dashboard**

1. Buka dashboard: `http://localhost:5000/accounts`
2. Klik "➕ Add Account"
3. Isi form:
   - **Account ID**: `account2` (contoh)
   - **Name**: `Promo Kuota 2`
   - **Username**: `@PromoKuota123`
   - **Enabled**: ❌ Jangan dicentang dulu (enable setelah cookies ditambahkan)
4. Klik "Save Account"
5. Folder otomatis dibuat: `accounts/account2_PromoKuota123/`

---

### **Step 2: Tambahkan Cookies**

Ada 3 metode untuk menambahkan cookies:

---

## 🔥 **METODE 1: Script Otomatis (TERMUDAH)** ⭐⭐⭐

Gunakan script helper yang sudah disediakan:

```bash
python add_account_cookies.py
```

**Interactive prompt akan muncul:**

```
╔════════════════════════════════════════════════════════════════╗
║           🍪 ADD ACCOUNT COOKIES - TWITTER BOT 🍪              ║
╚════════════════════════════════════════════════════════════════╝

📝 Enter account details:

Account ID (e.g., account2): account2
Twitter Username (without @): PromoKuota123
Twitter Password: ********
Email (for verification): your@email.com

📋 Summary:
   Account ID: account2
   Username: @PromoKuota123
   Email: your@email.com

✅ Proceed with login? (y/n): y

⏳ Logging in...
🔐 Logging in to Twitter as @PromoKuota123...
✅ Login successful!
✅ Cookies saved to: accounts/account2_PromoKuota123/cookies.json

📊 Account Information:
   Username: @PromoKuota123
   Name: Promo Kuota
   Followers: 150
   Following: 80

🎉 Success! Account ready to use.

💡 Next steps:
   1. Go to dashboard: http://localhost:5000/accounts
   2. Enable account 'account2'
   3. Click 'Start' button
```

**Selesai!** Cookies sudah tersimpan otomatis.

---

## 📋 **METODE 2: Copy dari Account Lain**

Jika Anda sudah punya cookies yang valid dari account lain:

```bash
# Copy cookies
cp cookies.json accounts/account2_PromoKuota123/cookies.json

# Atau dari account1
cp accounts/account1_GrnStore4347/cookies.json accounts/account2_PromoKuota123/cookies.json
```

**⚠️ PENTING:** 
- Cookies dari `@GrnStore4347` HANYA bisa digunakan untuk account `@GrnStore4347`
- Cookies dari `@PromoKuota123` HANYA bisa digunakan untuk account `@PromoKuota123`
- **JANGAN gunakan cookies yang sama untuk 2 account berbeda!**

---

## 🔧 **METODE 3: Login Manual via Python**

Buat script temporary untuk login:

```python
# tmp_login.py
import asyncio
from twikit import Client

async def login():
    client = Client('en-US')
    
    await client.login(
        auth_info_1='PromoKuota123',  # Username
        auth_info_2='your@email.com',  # Email
        password='your_password'       # Password
    )
    
    # Save cookies
    client.save_cookies('accounts/account2_PromoKuota123/cookies.json')
    print("✅ Cookies saved!")

asyncio.run(login())
```

Jalankan:
```bash
python tmp_login.py
rm tmp_login.py  # Hapus setelah selesai
```

---

## 🌐 **METODE 4: Export dari Browser (Advanced)**

### **Chrome/Edge:**

1. Login ke Twitter di browser dengan account yang ingin ditambahkan
2. Buka DevTools (F12)
3. Go to: `Application` → `Cookies` → `https://twitter.com`
4. Copy semua cookies yang ada
5. Convert ke format JSON twikit:

```json
{
  "ct0": "value_dari_browser",
  "auth_token": "value_dari_browser",
  ...
}
```

6. Save ke: `accounts/account2_PromoKuota123/cookies.json`

**⚠️ Rumit dan rawan error!** Gunakan Metode 1 atau 3 saja.

---

## ✅ **Step 3: Verify Cookies**

Test apakah cookies valid:

```bash
# Via CLI
python main.py --account account2 --test

# Output yang diharapkan:
✅ Connection test passed!
   Logged in as: @PromoKuota123
   Followers: 150
   Following: 80
```

Jika error:
- ❌ Cookies invalid/expired → Login ulang
- ❌ Account suspended → Gunakan account lain
- ❌ Rate limited → Tunggu 1 jam

---

## 🚀 **Step 4: Enable & Start Account**

### **Via Web Dashboard:**

1. Go to: `http://localhost:5000/accounts`
2. Find account `account2`
3. Toggle **Enabled** switch ke ON
4. Click "▶️ Start" button
5. Status akan berubah menjadi "🟢 Running"

### **Via CLI:**

```bash
# Enable via API
curl -X PUT http://localhost:5000/api/accounts/account2/update \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'

# Start account
python main.py --account account2 --daemon
```

---

## 🔄 **Refresh Cookies (Jika Expired)**

Cookies Twitter biasanya bertahan **1-3 bulan**. Jika expired:

```bash
# Login ulang dengan script
python add_account_cookies.py

# Pilih account yang sama
Account ID: account2

# Cookies akan di-overwrite dengan yang baru
```

---

## 🐛 **TROUBLESHOOTING**

### **1. Error: "Invalid cookies"**

**Penyebab:**
- Cookies expired
- Format cookies salah
- Account suspended

**Solusi:**
```bash
# Login ulang
python add_account_cookies.py

# Atau manual
rm accounts/account2_PromoKuota123/cookies.json
# Login ulang dengan metode 1 atau 3
```

---

### **2. Error: "Rate limited"**

**Penyebab:**
- Terlalu banyak login attempts

**Solusi:**
```bash
# Tunggu 1-2 jam, lalu coba lagi
# ATAU gunakan cookies dari browser (Metode 4)
```

---

### **3. Error: "Account folder not found"**

**Penyebab:**
- Account belum dibuat di dashboard

**Solusi:**
```bash
# Create account dulu via dashboard atau API
curl -X POST http://localhost:5000/api/accounts/create \
  -H "Content-Type: application/json" \
  -d '{
    "id": "account2",
    "name": "Promo Kuota 2",
    "username": "@PromoKuota123",
    "enabled": false
  }'

# Baru tambahkan cookies
python add_account_cookies.py
```

---

### **4. Error: "Bot tidak bisa post tweet"**

**Penyebab:**
- Cookies valid, tapi account restricted

**Solusi:**
```bash
# Check account status di Twitter
# Jika kena restrict, tunggu atau gunakan account lain
```

---

## 📊 **STRUKTUR FILE COOKIES**

Format cookies.json (simplified):

```json
{
  "ct0": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "auth_token": "yyyyyyyyyyyyyyyyyyyyyyyyyy",
  "twid": "u%3Dxxxxxxxxxx",
  "kdt": "zzzzzzzzzzzzzzzzzzzzzzzzzz",
  ...
}
```

**Jangan edit manual!** Gunakan script untuk generate.

---

## ✅ **CHECKLIST LENGKAP**

### **Untuk Account Baru:**

- [ ] 1. Create account di dashboard (`/accounts`)
- [ ] 2. Run script: `python add_account_cookies.py`
- [ ] 3. Input credentials Twitter
- [ ] 4. Verify cookies: `python main.py --account account2 --test`
- [ ] 5. Enable account di dashboard
- [ ] 6. Start account: Click "▶️ Start"
- [ ] 7. Monitor di dashboard: Status = "🟢 Running"

### **Untuk Account Existing (Refresh Cookies):**

- [ ] 1. Stop account dulu (jika running)
- [ ] 2. Run script: `python add_account_cookies.py`
- [ ] 3. Pilih account ID yang sama
- [ ] 4. Input credentials
- [ ] 5. Verify: `python main.py --account account2 --test`
- [ ] 6. Start ulang account

---

## 💡 **BEST PRACTICES**

### **DO ✅**
- ✅ Gunakan script `add_account_cookies.py` (paling mudah)
- ✅ Test cookies setelah ditambahkan (`--test`)
- ✅ Backup cookies ke tempat aman
- ✅ Refresh cookies setiap 1-2 bulan
- ✅ Gunakan email yang benar untuk verification

### **DON'T ❌**
- ❌ Gunakan cookies yang sama untuk 2 account berbeda
- ❌ Share cookies ke orang lain
- ❌ Edit cookies.json manual
- ❌ Commit cookies.json ke Git
- ❌ Login terlalu sering (rate limit)

---

## 🎯 **QUICK REFERENCE**

```bash
# Add cookies (recommended)
python add_account_cookies.py

# Test cookies
python main.py --account account2 --test

# Start account
python main.py --account account2 --daemon

# Via dashboard
http://localhost:5000/accounts
```

---

## 📞 **BUTUH BANTUAN?**

Jika masih bingung atau ada error:

1. Check error message di terminal
2. Baca troubleshooting section di atas
3. Verify account tidak suspended di Twitter
4. Test dengan account lain
5. Check log files: `accounts/account2_YourAccount/data/logs/`

---

## 🔐 **KEAMANAN**

**PENTING:**
- 🔒 Cookies = Login credentials
- 🔒 Jangan share ke siapapun
- 🔒 Add `cookies.json` ke `.gitignore`
- 🔒 Backup cookies ke tempat aman
- 🔒 Gunakan password yang kuat untuk Twitter account

---

## ✨ **KESIMPULAN**

**Cara Termudah:**
```bash
python add_account_cookies.py
```

**Selesai dalam 2 menit!** 🚀

---

*Last Updated: December 21, 2025*
