# 📸 PANDUAN UPLOAD GAMBAR PROMO - Twitter Bot

## 🎯 OVERVIEW

Setiap promo template sekarang **sudah support media (gambar/video)**! Bot akan otomatis upload dan attach media saat posting tweet.

---

## 📋 MEDIA FILES YANG DIBUTUHKAN

### **6 Gambar Promo (Recommended):**

```
media/promo/
├── promo_10gb_25k.jpg       # Promo 10GB Rp25.000
├── promo_25gb_50k.jpg       # Promo 25GB Rp50.000
├── promo_flash_sale.jpg     # Flash Sale generic
├── promo_unlimited_75k.jpg  # Unlimited Rp75.000
├── promo_50gb_100k.jpg      # 50GB Rp100.000
└── promo_weekend.jpg        # Weekend Sale
```

---

## 🎨 SPESIFIKASI DESAIN GAMBAR

### **Dimensi & Format:**
- ✅ **Dimensi:** 1200x675px (16:9 ratio) - Optimal untuk Twitter
- ✅ **Format:** JPG atau PNG (MP4 untuk video)
- ✅ **Ukuran:** Max 5MB untuk gambar, max 15MB untuk video
- ✅ **DPI:** 72 DPI (untuk web)

### **Elemen Desain yang Harus Ada:**

#### 1. **HARGA BESAR & JELAS** 💰
- Font besar, bold, warna kontras
- Contoh: "Rp25.000" atau "25K"
- Posisi: Center atau top-center

#### 2. **PAKET KUOTA PROMINENT** 📦
- Ukuran GB harus jelas
- Contoh: "10GB", "25GB", "UNLIMITED"
- Font size minimum 48px

#### 3. **BADGE PROMO** 🏷️
- Label seperti: "HEMAT 44%", "DISKON", "FLASH SALE"
- Warna eye-catching (merah, orange, kuning)
- Posisi: Top-left atau top-right corner

#### 4. **LOGO XL (Optional)** 📱
- Logo provider (XL) untuk kredibilitas
- Ukuran kecil, posisi bottom atau corner

#### 5. **CTA (Call to Action)** 📲
- Text seperti: "ORDER NOW", "WA: 08xxx"
- Button visual atau text prominent
- Posisi: Bottom atau bottom-right

---

## 📁 CARA UPLOAD GAMBAR

### **Method 1: Via Web Dashboard (Recommended)** ✅

1. Buka dashboard: `python dashboard.py`
2. Access: http://localhost:5000
3. Go to: **Configuration Editor → Settings Tab**
4. Scroll to: **Media Settings**
5. Click: **📤 Upload Image/Video**
6. Select file → Upload
7. File otomatis masuk ke `media/promo/`

### **Method 2: Manual Upload** 📂

```bash
# Copy gambar ke folder media/promo
cp promo_10gb_25k.jpg media/promo/
cp promo_25gb_50k.jpg media/promo/
# ... dan seterusnya
```

---

## ⚙️ MAPPING TEMPLATE → MEDIA

File `config/templates.yaml` sudah di-update:

```yaml
promo_templates:
  - text: "🔥 KUOTA XL MURAH! 10GB cuma Rp25.000!..."
    media: "media/promo/promo_10gb_25k.jpg"  ← Gambar ini
  
  - text: "📱 Stok ready! Kuota XL 25GB = Rp50.000..."
    media: "media/promo/promo_25gb_50k.jpg"  ← Gambar ini
  
  # ... dan seterusnya
```

**Bot akan:**
1. Random pilih salah satu promo template
2. Cek apakah ada media path
3. Upload media ke Twitter
4. Post tweet dengan media attached

---

## 🎨 TEMPLATE DESAIN GAMBAR

### **Example Layout:**

```
┌─────────────────────────────────────────┐
│  [BADGE: HEMAT 44%]          [Logo XL]  │
│                                          │
│           🔥 KUOTA XL MURAH! 🔥          │
│                                          │
│               10GB                       │
│             Rp25.000                     │
│                                          │
│          Harga Normal: Rp45.000          │
│                                          │
│         [ORDER NOW] [WA: 08xxx]          │
└─────────────────────────────────────────┘
```

### **Color Palette Recommended:**

- **Primary:** #667eea (Purple/Blue) - XL brand color
- **Accent:** #f59e0b (Orange) - Promo/discount
- **Success:** #10b981 (Green) - CTA button
- **Background:** #ffffff (White) or #f9fafb (Light gray)
- **Text:** #1f2937 (Dark gray)

---

## 🛠️ TOOLS DESIGN RECOMMENDED

### **Online (Free):**
- ✅ **Canva** - https://canva.com (Paling mudah!)
- ✅ **Figma** - https://figma.com (Professional)
- ✅ **Photopea** - https://photopea.com (Photoshop online)

### **Desktop:**
- Adobe Photoshop
- Adobe Illustrator
- GIMP (Free)

### **Template Sites:**
- ✅ Canva templates: "Social Media Post"
- ✅ Freepik: https://freepik.com
- ✅ Unsplash: https://unsplash.com (Background images)

---

## ✅ CHECKLIST SEBELUM UPLOAD

- [ ] Dimensi 1200x675px (16:9)
- [ ] Format JPG atau PNG
- [ ] Ukuran < 5MB
- [ ] Harga jelas & prominent
- [ ] Paket kuota terlihat besar
- [ ] Badge promo ada (HEMAT, DISKON, dll)
- [ ] CTA button/text ada (ORDER, WA)
- [ ] Text readable (font size cukup besar)
- [ ] Warna kontras & eye-catching
- [ ] File name sesuai: `promo_xxx.jpg`

---

## 🧪 TESTING MEDIA UPLOAD

### **Test Flow:**

```bash
# 1. Upload gambar via dashboard atau manual copy

# 2. Verify file exists
ls -la media/promo/

# 3. Test single post dengan media
python main.py --run-once morning

# 4. Check Twitter:
#    - Tweet posted? ✅
#    - Gambar attached? ✅
#    - Text correct? ✅
```

---

## 🔥 PRO TIPS

### **Tip 1: Gunakan Template Canva** 🎨
- Search: "Social Media Post"
- Pilih yang ukuran 1200x675px
- Customize text & colors
- Export as JPG

### **Tip 2: A/B Testing** 📊
- Buat 2 versi gambar berbeda (warna, layout)
- Upload keduanya dengan nama berbeda
- Edit `templates.yaml` untuk test both
- Track performance via dashboard
- Keep yang terbaik

### **Tip 3: Seasonal Designs** 🎉
- Buat versi spesial: Ramadan, Lebaran, New Year
- Ganti gambar di `templates.yaml` sesuai musim
- No code changes needed!

### **Tip 4: Video Support** 🎥
- Bot juga support video (MP4)
- Max 15MB, max 2 minutes 20 seconds
- Format: H.264 video, AAC audio
- Dimension: 1280x720px or 1920x1080px

### **Tip 5: Text on Image** 📝
- Jangan terlalu banyak text di gambar
- Tweet text sudah describe promo
- Gambar untuk visual appeal aja
- Focus: Harga + Paket + Badge

---

## ❓ TROUBLESHOOTING

### **Gambar tidak ter-upload saat posting:**

```bash
# Check 1: File exists?
ls -la media/promo/promo_10gb_25k.jpg

# Check 2: Path correct di templates.yaml?
cat config/templates.yaml | grep media

# Check 3: File size < 5MB?
du -h media/promo/promo_10gb_25k.jpg

# Check 4: Format supported?
file media/promo/promo_10gb_25k.jpg
```

### **Bot skip media (no image attached):**

**Reason:** File tidak ditemukan

**Fix:**
```yaml
# Option 1: Set media to null
media: null

# Option 2: Upload file yang benar
# Copy file ke media/promo/xxx.jpg
```

---

## 📸 EXAMPLE PROMPTS UNTUK AI IMAGE GENERATION

Jika pakai AI image generator (Midjourney, DALL-E, Stable Diffusion):

```
"Create a promotional social media post for mobile data plan. 
Features: 10GB data, price Rp25.000, 44% discount badge, 
XL logo, modern design, purple and orange colors, 
1200x675px, clean layout, professional"

"Design a flash sale banner for internet data package. 
Text: '25GB only 50K', discount badge, call-to-action button, 
minimalist design, Twitter post format, 16:9 ratio"
```

---

## 🎯 NEXT STEPS

1. ✅ **Design 6 gambar promo** (atau minimal 3 dulu)
2. ✅ **Upload via dashboard** atau manual copy
3. ✅ **Test posting** dengan `python main.py --run-once morning`
4. ✅ **Monitor performance** via dashboard
5. ✅ **Optimize design** based on engagement

---

## 📊 TRACKING MEDIA PERFORMANCE

Dashboard akan track:
- Tweet engagement rate (with vs without media)
- Best performing template (text + media combo)
- Media file usage statistics

**Expected:** Tweets dengan media biasanya **2-3x more engagement**!

---

## 💡 KESIMPULAN

- ✅ Sistem sudah 100% support media per template
- ✅ Upload gambar via dashboard (easy!)
- ✅ Bot otomatis handle upload & posting
- ✅ No coding needed untuk ganti gambar
- ✅ Design guidelines jelas untuk optimal results

**Ready to create amazing promo visuals! 🚀**
