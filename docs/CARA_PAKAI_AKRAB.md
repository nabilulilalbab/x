# 📖 CARA PAKAI CONFIG AKRAB

## 🔄 Switch ke Config Akrab

### Option 1: Rename Files
```bash
# Backup config lama
mv config/settings.yaml config/settings_old.yaml
mv config/templates.yaml config/templates_old.yaml

# Aktifkan config Akrab
mv config/settings_akrab.yaml config/settings.yaml
mv config/templates_akrab.yaml config/templates.yaml

# Restart bot
pkill -f dashboard.py
python dashboard.py
```

### Option 2: Edit via Dashboard
```
1. Open: http://localhost:5000
2. Go to Configuration Editor
3. Copy-paste settings dari settings_akrab.yaml
4. Copy-paste templates dari templates_akrab.yaml
5. Save
```

## 📱 Upload Gambar Produk

### Cara Upload:
```bash
# 1. Siapkan gambar produk di folder media/promo
cp /path/to/gambar-promo.jpg media/promo/

# 2. Bot akan random pilih gambar saat posting
# 3. Set use_media: true di schedule untuk post dengan gambar
```

## 🎯 Variables Baru untuk Akrab

Template sekarang support:
- `{kuota_area1}` = Kuota area 1
- `{kuota_area2}` = Kuota area 2  
- `{kuota_area3}` = Kuota area 3
- `{kuota_area4}` = Kuota area 4
- `{check_kuota_url}` = Link cek area
- Semua variables lama masih bisa dipakai

## 📊 Product List Lengkap

6 Paket sudah diinput:
1. SuperMini - Rp45.000 (13-32 GB)
2. Mini - Rp58.000 (31-50 GB)
3. Big - Rp62.000 (38-57 GB)
4. Jumbo V2 - Rp72.000 (50-69 GB)
5. Jumbo - Rp85.000 (65-123 GB) ⭐ Best value
6. MegaBig - Rp96.000 (88-107 GB)

Kuota berbeda per area sudah diinput lengkap!

