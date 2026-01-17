# 🍪 COOKIE EXTENSIONS GUIDE - Twitter Bot

Panduan lengkap extension browser untuk export cookies Twitter yang **plug and play** dengan project ini.

---

## 🎯 Cookie Format yang Dibutuhkan

Project ini menggunakan **Twikit library** yang membutuhkan cookies dalam format JSON sederhana:

```json
{
  "ct0": "csrf_token_value_here",
  "auth_token": "authentication_token_value_here"
}
```

**2 cookies yang WAJIB:**
1. ✅ `ct0` - CSRF token (Cross-Site Request Forgery)
2. ✅ `auth_token` - Authentication token

---

## ⭐ REKOMENDASI EXTENSION (Ranking)

### 🥇 **1. Cookie-Editor (RECOMMENDED)**

**Platform**: Chrome, Firefox, Edge  
**Rating**: ⭐⭐⭐⭐⭐ (5/5)  
**Plug & Play**: ✅ YES  

#### Download:
- **Chrome**: https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm
- **Firefox**: https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/
- **Edge**: https://microsoftedge.microsoft.com/addons/detail/cookie-editor/ajfboaconbpkglpfanbmlfgojgndmhmc

#### Cara Pakai (3 Langkah):

**Step 1: Login ke Twitter**
```
1. Buka browser → Login ke Twitter (x.com)
2. Pastikan berhasil login (lihat homepage Twitter Anda)
```

**Step 2: Export Cookies**
```
1. Klik icon Cookie-Editor di toolbar
2. Klik "Export" → "JSON"
3. Copy semua JSON yang muncul
```

**Step 3: Filter & Save**
```python
# Paste ke file sementara (semua cookies)
# Lalu filter hanya ct0 dan auth_token

# Cara cepat dengan Python:
python3 << 'EOF'
import json

# Paste hasil export dari Cookie-Editor di sini
all_cookies = [
    # Paste hasil copy dari Cookie-Editor
]

# Filter hanya yang dibutuhkan
needed = {}
for cookie in all_cookies:
    if cookie['name'] == 'ct0':
        needed['ct0'] = cookie['value']
    elif cookie['name'] == 'auth_token':
        needed['auth_token'] = cookie['value']

# Save to file
with open('accounts/account1_GrnStore4347/cookies.json', 'w') as f:
    json.dump(needed, f, indent=2)

print("✅ Cookies saved!")
print(json.dumps(needed, indent=2))
EOF
```

**Kenapa Cookie-Editor?**
- ✅ Paling simple & ringan
- ✅ Export format JSON native
- ✅ Open source & trusted (1M+ users)
- ✅ No tracking, no ads
- ✅ Support semua browser

---

### 🥈 **2. EditThisCookie**

**Platform**: Chrome, Edge  
**Rating**: ⭐⭐⭐⭐☆ (4/5)  
**Plug & Play**: ✅ YES (dengan edit manual)

#### Download:
- **Chrome**: https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg

#### Cara Pakai:

**Step 1: Login & Export**
```
1. Login ke Twitter (x.com)
2. Klik icon EditThisCookie
3. Klik "Export" (ikon diskette)
4. Cookies akan di-copy ke clipboard (JSON format)
```

**Step 2: Filter Cookies**
```bash
# Save clipboard ke file sementara
nano tmp_all_cookies.json

# Filter dengan jq (jika installed)
cat tmp_all_cookies.json | jq '[.[] | select(.name == "ct0" or .name == "auth_token") | {(.name): .value}] | add' > accounts/account1_GrnStore4347/cookies.json

# Or manual: Copy hanya ct0 dan auth_token values
```

**Kenapa EditThisCookie?**
- ✅ Interface user-friendly
- ✅ Banyak dipakai developer
- ✅ Features lengkap (edit, delete, search)
- ⚠️ Hanya Chrome/Edge (tidak ada Firefox)

---

### 🥉 **3. Get cookies.txt LOCALLY**

**Platform**: Chrome, Firefox  
**Rating**: ⭐⭐⭐⭐☆ (4/5)  
**Plug & Play**: ⚠️ Butuh konversi format

#### Download:
- **Chrome**: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
- **Firefox**: https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/

#### Cara Pakai:

**Step 1: Export**
```
1. Login ke Twitter
2. Klik extension icon
3. Click "Export" → Export as cookies.txt format
```

**Step 2: Convert Format**
```python
# Konversi dari cookies.txt ke JSON
import json

# Read cookies.txt
cookies_txt = """
# Paste isi cookies.txt di sini
.twitter.com	TRUE	/	TRUE	1234567890	ct0	your_ct0_value
.twitter.com	TRUE	/	TRUE	1234567890	auth_token	your_auth_token_value
"""

# Parse
cookies = {}
for line in cookies_txt.strip().split('\n'):
    if line.startswith('#') or not line.strip():
        continue
    parts = line.split('\t')
    if len(parts) >= 7:
        name = parts[5]
        value = parts[6]
        if name in ['ct0', 'auth_token']:
            cookies[name] = value

# Save
with open('accounts/account1_GrnStore4347/cookies.json', 'w') as f:
    json.dump(cookies, f, indent=2)

print("✅ Converted!")
```

**Kenapa Get cookies.txt?**
- ✅ Format Netscape (standard)
- ✅ Work dengan banyak tools
- ⚠️ Butuh konversi ke JSON
- ⚠️ Less user-friendly

---

### 🔧 **4. Developer Tools (Built-in Browser)**

**Platform**: All Browsers  
**Rating**: ⭐⭐⭐☆☆ (3/5)  
**Plug & Play**: ⚠️ Manual extraction

#### Cara Pakai:

**Chrome/Edge/Firefox:**
```
1. Login ke Twitter (x.com)
2. Press F12 (open DevTools)
3. Go to "Application" tab (Chrome) / "Storage" tab (Firefox)
4. Click "Cookies" → "https://x.com" atau "https://twitter.com"
5. Find:
   - Name: ct0        → Copy Value
   - Name: auth_token → Copy Value
6. Paste ke JSON format
```

**Manual JSON Creation:**
```json
{
  "ct0": "paste_ct0_value_here",
  "auth_token": "paste_auth_token_value_here"
}
```

**Kenapa DevTools?**
- ✅ No extension needed
- ✅ Available di semua browser
- ⚠️ Manual & tedious
- ⚠️ Easy to make mistakes

---

## 🚀 QUICK COMPARISON

| Extension | Browser Support | Ease of Use | Format | Recommendation |
|-----------|----------------|-------------|---------|----------------|
| **Cookie-Editor** | Chrome, Firefox, Edge | ⭐⭐⭐⭐⭐ | JSON native | ✅ **BEST** |
| **EditThisCookie** | Chrome, Edge | ⭐⭐⭐⭐☆ | JSON | ✅ Good |
| **Get cookies.txt** | Chrome, Firefox | ⭐⭐⭐☆☆ | Netscape | ⚠️ Need conversion |
| **DevTools** | All | ⭐⭐☆☆☆ | Manual | ⚠️ Manual work |

---

## 📋 STEP-BY-STEP GUIDE (Cookie-Editor)

### **Full Walkthrough - Copy Paste Ready:**

#### **1. Install Extension**
```
Chrome: https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm
Firefox: https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/
```

#### **2. Login Twitter**
```
1. Buka browser baru (incognito/private jika perlu)
2. Go to: https://x.com (atau https://twitter.com)
3. Login dengan username & password account Anda
4. Pastikan sudah masuk (lihat homepage feed Twitter)
```

#### **3. Export Cookies**
```
1. Klik icon Cookie-Editor di toolbar (pojok kanan atas)
2. Akan muncul popup list cookies
3. Klik tombol "Export" di bawah
4. Pilih "JSON" format
5. All cookies akan dicopy ke clipboard
```

#### **4. Extract ct0 & auth_token**

**Option A: Via Python Script (Recommended)**
```bash
# Buat script helper
cat > extract_cookies.py << 'EOF'
#!/usr/bin/env python3
import json
import sys

print("🍪 Twitter Cookie Extractor")
print("=" * 50)
print("\nPaste semua JSON dari Cookie-Editor, lalu tekan Ctrl+D (Linux/Mac) atau Ctrl+Z Enter (Windows):\n")

# Read from stdin
try:
    input_data = sys.stdin.read()
    all_cookies = json.loads(input_data)
    
    # Extract needed cookies
    needed = {}
    for cookie in all_cookies:
        if cookie.get('name') == 'ct0':
            needed['ct0'] = cookie['value']
        elif cookie.get('name') == 'auth_token':
            needed['auth_token'] = cookie['value']
    
    if not needed.get('ct0') or not needed.get('auth_token'):
        print("❌ Error: ct0 or auth_token not found!")
        print("   Make sure you're logged in to Twitter first.")
        sys.exit(1)
    
    # Ask for account folder
    print("\n✅ Cookies extracted successfully!")
    print(f"   ct0: {needed['ct0'][:20]}...")
    print(f"   auth_token: {needed['auth_token'][:20]}...")
    
    account_folder = input("\nEnter account folder (e.g., account1_GrnStore4347): ").strip()
    
    output_file = f"accounts/{account_folder}/cookies.json"
    
    with open(output_file, 'w') as f:
        json.dump(needed, f, indent=2)
    
    print(f"\n🎉 Cookies saved to: {output_file}")
    print("\n💡 Next steps:")
    print(f"   python main.py --account {account_folder.split('_')[0]} --test")
    
except json.JSONDecodeError:
    print("❌ Error: Invalid JSON format")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
EOF

chmod +x extract_cookies.py

# Run script
python3 extract_cookies.py
# Paste JSON dari Cookie-Editor, lalu Ctrl+D
```

**Option B: Manual (Quick & Dirty)**
```bash
# 1. Paste JSON ke file
nano tmp_all_cookies.json
# Paste hasil dari Cookie-Editor

# 2. Filter dengan grep/python one-liner
python3 -c "
import json
data = json.load(open('tmp_all_cookies.json'))
needed = {}
for c in data:
    if c['name'] in ['ct0', 'auth_token']:
        needed[c['name']] = c['value']
print(json.dumps(needed, indent=2))
" > accounts/account1_GrnStore4347/cookies.json

# 3. Verify
cat accounts/account1_GrnStore4347/cookies.json

# 4. Cleanup
rm tmp_all_cookies.json
```

#### **5. Verify Cookies**
```bash
# Test connection
python3 main.py --account account1 --test

# Expected output:
# ✅ Logged in as @YourUsername
#    Followers: 123
#    Following: 45
```

---

## 🔒 SECURITY TIPS

### **1. Jangan Share Cookies!**
```
❌ JANGAN post cookies ke:
   - GitHub/GitLab (public repo)
   - Screenshot
   - Chat group
   - Discord/Telegram
   
✅ Cookies = Password
   Siapa punya cookies bisa login sebagai Anda!
```

### **2. Regenerate Jika Kebocoran**
```
Jika cookies bocor:
1. Login ke Twitter via browser
2. Logout semua devices: Settings → Security → Sessions
3. Change password
4. Login lagi & export cookies baru
```

### **3. Cookie Expiration**
```
Cookies Twitter biasanya valid:
- ✅ 30-60 hari jika tidak logout
- ❌ Invalid jika: logout, change password, suspicious activity

Jika cookies expired:
1. Export cookies baru (ulangi proses ini)
2. Replace di accounts/*/cookies.json
3. Restart bot
```

### **4. File Permissions**
```bash
# Set proper permissions (Linux/Mac)
chmod 600 accounts/*/cookies.json
chmod 700 accounts/

# Verify
ls -la accounts/account1_GrnStore4347/cookies.json
# Should show: -rw------- (600)
```

---

## 🆘 TROUBLESHOOTING

### **Issue 1: Extension tidak muncul di toolbar**
```
Solution:
1. Klik icon "Extensions" (puzzle piece) di toolbar
2. Find "Cookie-Editor"
3. Click "pin" icon untuk pin ke toolbar
```

### **Issue 2: "ct0" atau "auth_token" tidak ada**
```
Possible causes:
❌ Not logged in to Twitter
❌ Using wrong domain (use x.com or twitter.com)
❌ Cookies cleared recently

Solution:
1. Clear browser cache & cookies
2. Login fresh ke Twitter
3. Export cookies lagi
```

### **Issue 3: Cookies tidak valid (bot tidak bisa login)**
```
Symptoms:
❌ Error: "Failed to setup Twitter client"
❌ Error: "Invalid credentials"

Solution:
1. Verify cookies.json format correct (2 keys: ct0, auth_token)
2. Check no extra characters (quotes, spaces)
3. Try logout & login Twitter again
4. Export fresh cookies
```

### **Issue 4: JSON format error**
```
Error:
❌ json.decoder.JSONDecodeError: Expecting value

Solution:
1. Use extract_cookies.py script (auto format)
2. Or validate JSON: https://jsonlint.com
3. Check no trailing commas
4. Check quotes are double quotes (")
```

---

## 📦 AUTOMATION SCRIPT (BONUS)

Script untuk auto-extract cookies dari Cookie-Editor export:

```bash
# Save as: get_twitter_cookies.sh
#!/bin/bash

cat > /tmp/extract.py << 'PYTHON'
import json
import sys

data = json.loads(sys.stdin.read())
needed = {}
for c in data:
    if c['name'] in ['ct0', 'auth_token']:
        needed[c['name']] = c['value']

if len(needed) != 2:
    print("Error: Missing cookies!", file=sys.stderr)
    sys.exit(1)

print(json.dumps(needed, indent=2))
PYTHON

echo "🍪 Twitter Cookie Extractor"
echo "1. Copy cookies dari Cookie-Editor (Export → JSON)"
echo "2. Paste di sini, lalu Ctrl+D:"
echo ""

python3 /tmp/extract.py
rm /tmp/extract.py
```

**Usage:**
```bash
chmod +x get_twitter_cookies.sh
./get_twitter_cookies.sh > accounts/account1_GrnStore4347/cookies.json
```

---

## 📚 REFERENCES

### Extension Links:
- **Cookie-Editor**: https://cookie-editor.cgagnier.ca/
- **EditThisCookie**: http://www.editthiscookie.com/
- **Get cookies.txt**: https://github.com/lennonhill/cookies-txt

### Documentation:
- **Twikit**: https://github.com/d60/twikit
- **Twitter API**: https://developer.twitter.com/en/docs

---

## ✅ CHECKLIST

Setup cookies checklist:

- [ ] Extension installed (Cookie-Editor recommended)
- [ ] Logged in to Twitter (x.com)
- [ ] Cookies exported via extension
- [ ] Extracted ct0 & auth_token
- [ ] Saved to accounts/*/cookies.json
- [ ] File format valid JSON
- [ ] Tested with `--test` flag
- [ ] Bot logged in successfully

---

## 🎯 SUMMARY

**BEST PRACTICE:**
1. ✅ Use **Cookie-Editor** extension (easiest)
2. ✅ Login ke Twitter di browser
3. ✅ Export → JSON
4. ✅ Filter ct0 & auth_token (via script atau manual)
5. ✅ Save ke `accounts/*/cookies.json`
6. ✅ Test dengan `python main.py --test`

**Format Final:**
```json
{
  "ct0": "your_csrf_token_value_here",
  "auth_token": "your_auth_token_value_here"
}
```

---

**Version**: 1.0  
**Last Updated**: 2026-01-17  
**Status**: ✅ Production Ready
