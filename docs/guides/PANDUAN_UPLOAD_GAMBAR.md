# 📸 PANDUAN UPLOAD GAMBAR PRODUK

## 🎯 Cara Upload Gambar

### **Step 1: Siapkan Gambar**

Buat gambar promosi produk Anda dengan tools seperti:
- Canva (recommended - ada template gratis)
- Photoshop
- Figma
- Atau screenshot dari HP

**Format yang didukung:**
- ✅ JPG / JPEG
- ✅ PNG
- ✅ MP4 (video)

**Ukuran maksimal:** 15 MB

---

### **Step 2: Upload ke Folder**

```bash
# Copy gambar ke folder media/promo
cp /path/to/gambar-promo.jpg media/promo/

# Atau multiple files
cp promo-supermini.jpg media/promo/
cp promo-jumbo.jpg media/promo/
cp promo-megabig.jpg media/promo/
```

**Via Dashboard (belum implement, tapi bisa manual):**
```bash
# Upload via terminal
cd media/promo
# Drag & drop file ke sini
```

---

### **Step 3: Configure Bot**

Edit `config/settings.yaml`:

```yaml
media:
  enabled: true  # Set true untuk aktifkan
  folder: "media/promo"
  formats: ["jpg", "jpeg", "png", "mp4"]
  max_size_mb: 15
  use_random: true  # Random pilih gambar
```

Edit schedule untuk set kapan pakai gambar:

```yaml
schedule:
  morning:
    time: "08:00"
    use_media: true  # Post dengan gambar
    
  afternoon:
    time: "13:00"
    use_media: false  # Post text only
    
  evening:
    time: "20:00"
    use_media: true  # Post dengan gambar
```

---

## 📊 Contoh Konten Gambar

### **Gambar 1: Daftar Harga**
```
[Background menarik]

🔥 AKRAB FRESH XLA

SuperMini: Rp45.000
Mini: Rp58.000
Big: Rp62.000
Jumbo V2: Rp72.000
Jumbo: Rp85.000 ⭐
MegaBig: Rp96.000

✅ Official & Bergaransi
✅ Masa aktif 28-30 hari

Cek area: bendith.my.id
Order: 085876423783
```

### **Gambar 2: Highlight Paket Terbaik**
```
[Background eye-catching]

🎯 PAKET JUMBO
Rp85.000

Kuota s/d 123 GB!
(Area 4)

✅ Full Reguler
✅ Resmi & Bergaransi

WA: 085876423783
```

### **Gambar 3: Comparison**
```
❌ Beli di MyXL: Rp115.000
✅ Beli Akrab: Rp85.000

HEMAT Rp30.000! 💰

Dapatkan kuota lebih banyak!
Order sekarang!
```

---

## 🤖 Cara Kerja Bot

### **Bot akan:**

1. Check `media.enabled` = true?
2. Check `use_media` di slot schedule
3. Scan folder `media/promo`
4. Random pilih 1 gambar
5. Upload ke Twitter
6. Post tweet dengan gambar

### **Example Flow:**

```
Morning Slot (08:00):
1. Generate tweet text: "🔥 AKRAB FRESH XLA Jumbo..."
2. use_media = true → cari gambar
3. Found: media/promo/promo-jumbo.jpg
4. Upload gambar → media_id: 12345
5. Post tweet dengan text + gambar
6. Done! ✅
```

---

## 💡 Tips Desain Gambar

### **Best Practices:**

1. **Ukuran optimal:** 1200x675 px (landscape) atau 1080x1080 px (square)
2. **Font:** Besar dan mudah dibaca
3. **Warna:** Kontras tinggi (background gelap, text terang)
4. **Emoji:** Max 3-5 emoji
5. **Call-to-action:** Jelas (nomor WA besar)
6. **Branding:** Consistent style untuk semua gambar

### **Tools Recommended:**

- **Canva** (free, mudah) - canva.com
- **Figma** (free, professional) - figma.com
- **Photopea** (free, online photoshop) - photopea.com

---

## 📝 Naming Convention

**Recommended:**

```
promo-supermini.jpg
promo-mini.jpg
promo-big.jpg
promo-jumbo-v2.jpg
promo-jumbo.jpg
promo-megabig.jpg
promo-daftar-harga.jpg
promo-testimoni.jpg
```

Bot akan random pilih, jadi semua gambar punya chance tampil!

---

## 🔄 Update Gambar

```bash
# 1. Hapus gambar lama
rm media/promo/promo-old.jpg

# 2. Upload gambar baru
cp promo-new.jpg media/promo/

# 3. No restart needed! Bot akan detect otomatis
```

---

## ⚠️ Troubleshooting

**Q: Bot tidak upload gambar?**
A: Check:
- `media.enabled: true` di settings.yaml
- `use_media: true` di schedule
- Ada file di `media/promo/`
- Format file benar (jpg/png/mp4)

**Q: Gambar terlalu besar?**
A: Compress dulu:
- Online: tinypng.com
- Or resize di Canva

**Q: Video tidak jalan?**
A: Check:
- Max 15 MB
- Format MP4
- Max 2 menit 20 detik

---

## ✅ Ready!

1. ✅ Buat gambar promosi
2. ✅ Upload ke `media/promo/`
3. ✅ Set `media.enabled: true`
4. ✅ Set `use_media: true` di schedule
5. ✅ Bot akan post dengan gambar!

**Selamat mencoba!** 🎉

