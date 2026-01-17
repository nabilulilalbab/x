# 📝 NEW TEMPLATE SYSTEM - Panduan Lengkap

## 🎯 Konsep Baru: Simple & Custom

Sistem template baru ini **lebih sederhana dan fleksibel**. Tidak perlu lagi variable rumit seperti `{paket}`, `{harga}`, `{diskon}` - langsung tulis tweet lengkap sesuka hati!

## ✅ Apa yang Berubah?

### ❌ Sistem Lama (Kompleks):

1. **settings.yaml** - Input data paket & harga:
```yaml
prices:
  - paket: 10GB
    harga: '25000'
    harga_display: Rp25.000
    harga_normal: Rp45.000
    diskon: 44
```

2. **templates.yaml** - Template dengan variable:
```yaml
promo_templates:
  - "🔥 KUOTA XL MURAH! {paket} cuma {harga}!"
```

3. Bot akan replace `{paket}` dan `{harga}` dari settings.yaml

**Masalah:** Ribet, harus edit 2 file, tidak fleksibel!

---

### ✅ Sistem Baru (Simple):

**templates.yaml** - Tulis full text langsung:
```yaml
promo_templates:
  - text: "🔥 KUOTA XL MURAH! 10GB cuma Rp25.000! Hemat 44%!
    
📲 Order: {wa_number}"
    media: null  # Optional: path ke gambar/video
  
  - text: "📱 Stok ready! 25GB Rp50.000 aja! Fast response: {wa_number}"
    media: "media/promo/promo-25gb.jpg"
  
  - text: "⚡ FLASH SALE! Unlimited Rp75.000!
    
Order: {wa_number}"
    media: null
```

**Benefit:**
- ✅ Edit 1 file aja
- ✅ Custom per tweet (bisa beda harga, beda style)
- ✅ Setiap tweet bisa punya media berbeda
- ✅ Lebih fleksibel & cepat

---

## 📖 Cara Pakai

### 1. Edit Templates

Buka `config/templates.yaml`:

```yaml
promo_templates:
  - text: "Tweet lengkap dengan harga & paket"
    media: null
  
  - text: "Tweet kedua dengan style berbeda"
    media: "media/promo/gambar.jpg"
```

**Tips:**
- Tulis tweet lengkap dengan harga, paket, emoji
- Max 280 karakter (Twitter limit)
- Gunakan `{wa_number}` untuk auto-fill nomor WA
- Gunakan `{wa_link}` untuk auto-fill link WA
- Field `media` bisa `null` atau path ke file

### 2. Variable yang Tersedia

Hanya 2 variable (optional):

| Variable | Isi | Contoh |
|----------|-----|--------|
| `{wa_number}` | Nomor WhatsApp | 085117557905 |
| `{wa_link}` | Link WA dengan text | https://wa.me/6285117... |

**Contoh penggunaan:**
```yaml
- text: "💰 Kuota XL 10GB Rp25.000!
  
Order sekarang: {wa_number}"
  media: null
```

Bot akan replace `{wa_number}` dengan nomor dari `settings.yaml`.

### 3. Tambah Media per Template

**Cara 1: Edit YAML Manual**

```yaml
- text: "🔥 PROMO! 10GB Rp25.000!"
  media: "media/promo/promo-10gb.jpg"  # Path relatif
```

**Cara 2: Via Dashboard** (Coming soon)
- Buka dashboard
- Klik "Edit Templates"
- Upload gambar untuk setiap template

**Supported formats:**
- Images: `.jpg`, `.jpeg`, `.png`
- Videos: `.mp4`

### 4. Mix Berbagai Paket

Bisa campur berbagai paket dalam satu list:

```yaml
promo_templates:
  - text: "🔥 10GB cuma Rp25.000! WA: {wa_number}"
    media: "media/promo/10gb.jpg"
  
  - text: "📱 25GB Rp50.000 aja! Order: {wa_number}"
    media: "media/promo/25gb.jpg"
  
  - text: "⚡ Unlimited Rp75.000! Fast: {wa_number}"
    media: "media/promo/unlimited.jpg"
  
  - text: "🎯 50GB Rp100.000! Limited! WA: {wa_number}"
    media: null  # Tanpa gambar
```

Bot akan random pilih salah satu setiap kali posting.

---

## 🎨 Contoh Template Bagus

### Template Promo Hard Selling:

```yaml
- text: "🔥 FLASH SALE! 
Kuota XL 10GB = Rp25.000 
Hemat 44%! 

✅ Proses 1-5 menit
✅ Garansi uang kembali

Order: {wa_number}"
  media: "media/promo/flash-sale.jpg"
```

### Template Soft Selling:

```yaml
- text: "📱 Butuh kuota buat WFH? 

Kuota XL 25GB cuma Rp50.000 aja! 
Sinyal stabil, proses cepat.

Info: {wa_number}"
  media: null
```

### Template Weekend Special:

```yaml
- text: "🎉 WEEKEND SALE! 

Kuota XL Unlimited Rp75.000
Dari Rp150.000 → Rp75.000 🔥

Buruan sebelum kehabisan!
WA: {wa_number}"
  media: "media/promo/weekend.jpg"
```

---

## 🔧 Settings.yaml (Simplified)

Section `prices` sudah dihapus! Sekarang lebih simple:

```yaml
business:
  product: Kuota XL
  niche: pulsa_kuota
  wa_number: 085117557905
  wa_link: https://wa.me/6285117557905?text=Halo%20min%20mau%20order%20kuota%20XL
```

**Apa yang berubah:**
- ❌ Hapus section `prices` (tidak perlu lagi!)
- ✅ Keep: `wa_number`, `wa_link`, `product`, `niche`

---

## 📊 Flow Bot

### Old Flow:
1. Ambil random price dari settings.yaml
2. Ambil random template dari templates.yaml
3. Replace `{paket}`, `{harga}`, dll dengan data price
4. AI improve
5. Post

### New Flow:
1. Ambil random template dari templates.yaml (sudah full text)
2. Replace `{wa_number}` dan `{wa_link}` aja
3. Check ada media? Upload jika ada
4. AI improve
5. Post dengan/tanpa media

**Lebih simple & cepat!**

---

## 🎯 Value Content (Tips/Tutorials/FAQs)

Value templates tetap pakai variable (untuk auto-generate):

```yaml
value_templates:
  - "💡 Tips hemat kuota #{number}: {tip}

Btw, kalau butuh kuota XL murah, DM aja ya! 📲"
  
  - "🎓 Tutorial: {tutorial_title}

{tutorial_content}

Kalau kuota habis, order di sini aja: {wa_number}"
```

Bot akan auto-fill:
- `{tip}` → Random dari list tips
- `{tutorial_title}` → Random dari list tutorials
- `{number}` → Random number 1-50
- `{wa_number}` → Your WA number

**Ini tetap otomatis**, tidak perlu diubah!

---

## 🚀 Quick Start

### 1. Backup Config Lama

```bash
cp config/templates.yaml config/templates.yaml.backup
```

### 2. Edit Templates

Buka `config/templates.yaml`, ganti promo_templates dengan tweet lengkap:

```yaml
promo_templates:
  - text: "Your full tweet here with price and package!"
    media: null
  
  - text: "Another tweet with different style!"
    media: "media/promo/image.jpg"
```

### 3. Test

```bash
# Test generate tweet
python3 -c "
import asyncio
from bot.config_loader import ConfigLoader
from bot.content_generator import ContentGenerator

async def test():
    config = ConfigLoader()
    gen = ContentGenerator(config, None)
    tweet, media = await gen.generate_promo_tweet(use_ai=False)
    print(f'Tweet: {tweet}')
    print(f'Media: {media}')

asyncio.run(test())
"
```

### 4. Run Bot

```bash
# Test manual posting
python main.py --run-once morning

# Atau daemon mode
python main.py --daemon
```

---

## ❓ FAQ

**Q: Bagaimana kalau mau ganti nomor WA?**
A: Edit `settings.yaml` di section `business.wa_number`, otomatis semua template update.

**Q: Bisa mix template dengan/tanpa media?**
A: Yes! Set `media: null` untuk tanpa media, atau `media: "path/to/image.jpg"` untuk dengan media.

**Q: Berapa maksimal karakter tweet?**
A: Twitter limit 280 karakter. Bot akan tetap post tapi Twitter bisa truncate.

**Q: AI improvement masih jalan?**
A: Yes! AI tetap improve tweet sebelum posting (jika enabled di settings).

**Q: Old templates masih work?**
A: Yes! Bot support backward compatibility. Old format (string) masih bisa, tapi recommend pakai format baru (dict dengan text & media).

---

## 🎉 Summary

### Before:
- Edit 2 files (settings.yaml + templates.yaml)
- Variable rumit: `{paket}`, `{harga}`, `{diskon}`, dll
- Media random dari folder (tidak bisa per template)
- Tidak fleksibel (semua template harus pakai variable yang sama)

### After:
- Edit 1 file aja (templates.yaml)
- Variable simple: `{wa_number}`, `{wa_link}` (optional)
- Media per template (custom setiap tweet)
- Sangat fleksibel (tulis sesuka hati!)

**Happy tweeting! 🚀**
