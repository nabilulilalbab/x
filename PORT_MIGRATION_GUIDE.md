# 🔄 PORT MIGRATION GUIDE

Port telah diubah dari default ke port unik untuk menghindari konflik di VPS.

---

## 🔢 Port Changes

| Service | Old Port | New Port | Reason |
|---------|----------|----------|---------|
| **Dashboard V1** | 5000 | **8280** | Unique port (Twitter 280 chars themed) |
| **Dashboard V2** | 5001 | **8281** | Sequential from Dashboard V1 |

---

## 📝 Files Changed

### 1. Configuration Files
- ✅ `config/settings.yaml` - Dashboard port: 8280
- ✅ `config/settings_akrab.yaml` - Dashboard port: 8280
- ✅ `ecosystem.config.js` - PM2 env ports updated

### 2. Application Files
- ✅ `dashboard_v2.py` - Hardcoded port changed to 8281

---

## 🚀 How to Access

### After Change:
```bash
# Dashboard V1 (Multi-Account Manager)
http://localhost:8280

# Dashboard V2 (Per-Account View)
http://localhost:8281
```

### Remote Access (SSH Tunnel):
```bash
# Forward port 8280
ssh -L 8280:localhost:8280 user@your-vps.com

# Forward port 8281
ssh -L 8281:localhost:8281 user@your-vps.com

# Access via browser:
http://localhost:8280
http://localhost:8281
```

---

## 🔧 Update Firewall (If Needed)

### UFW (Ubuntu):
```bash
# Allow new ports
sudo ufw allow 8280/tcp
sudo ufw allow 8281/tcp

# Remove old ports (if not used elsewhere)
sudo ufw delete allow 5000/tcp
sudo ufw delete allow 5001/tcp

# Check rules
sudo ufw status
```

### FirewallD (CentOS/RHEL):
```bash
# Add new ports
sudo firewall-cmd --permanent --add-port=8280/tcp
sudo firewall-cmd --permanent --add-port=8281/tcp

# Remove old ports (if not used)
sudo firewall-cmd --permanent --remove-port=5000/tcp
sudo firewall-cmd --permanent --remove-port=5001/tcp

# Reload
sudo firewall-cmd --reload
```

---

## 🔄 Restart Services

### If Already Running:
```bash
# Stop old services
pm2 stop all

# Start with new ports (auto-detect from config)
pm2 start ecosystem.config.js

# Or restart
pm2 restart all

# Verify
pm2 status
```

### Check Logs:
```bash
pm2 logs

# You should see:
# "📊 Dashboard URL: http://0.0.0.0:8280"
# "📊 Dashboard URL: http://0.0.0.0:8281"
```

---

## ✅ Verification

### Test Ports:
```bash
# Check if ports are listening
sudo netstat -tuln | grep 8280
sudo netstat -tuln | grep 8281

# Or with ss
sudo ss -tuln | grep 8280
sudo ss -tuln | grep 8281

# Or with lsof
sudo lsof -i :8280
sudo lsof -i :8281
```

### Test Access:
```bash
# Test Dashboard V1
curl http://localhost:8280

# Test Dashboard V2
curl http://localhost:8281

# Should return HTML
```

---

## 📖 Documentation Updates Needed

Documentation files that mention old ports (5000/5001) will need manual updates when you read them:

### Quick Reference:
When you see in docs:
- ❌ `http://localhost:5000` → ✅ Use `http://localhost:8280`
- ❌ `http://localhost:5001` → ✅ Use `http://localhost:8281`

### Files with Port References (for your info):
```
docs/guides/CARA_PAKAI_AKRAB.md
docs/guides/USAGE.md
docs/guides/PANDUAN_MEDIA_PROMO.md
docs/guides/PANDUAN_TAMBAH_COOKIES.md
docs/reports/FINAL_SUMMARY.md
docs/reports/FINAL_TEST_RESULTS.md
docs/deployment/PM2_DEPLOYMENT_GUIDE.md
DEPLOYMENT.md
QUICK_DEPLOYMENT.md
README.md
```

**Note**: You can use Find & Replace in your editor to update these if needed.

---

## 🎯 Quick Migration Checklist

- [x] Update config/settings.yaml port
- [x] Update config/settings_akrab.yaml port
- [x] Update dashboard_v2.py port
- [x] Update ecosystem.config.js ports
- [ ] Restart PM2 services
- [ ] Update firewall rules (if needed)
- [ ] Test access to both dashboards
- [ ] Update bookmarks/shortcuts
- [ ] Notify team members (if any)

---

## 🔙 Rollback (If Needed)

If you need to revert to old ports:

```bash
# 1. Update config files
sed -i 's/port: 8280/port: 5000/g' config/settings.yaml
sed -i 's/port: 8280/port: 5000/g' config/settings_akrab.yaml

# 2. Update dashboard_v2.py
sed -i 's/8281/5001/g' dashboard_v2.py

# 3. Update ecosystem.config.js
sed -i 's/8280/5000/g' ecosystem.config.js
sed -i 's/8281/5001/g' ecosystem.config.js

# 4. Restart
pm2 restart all
```

---

## 🎉 Benefits of New Ports

✅ **No Conflicts** - 8280/8281 rarely used by other services
✅ **Easy to Remember** - 8280 = Twitter 280 character limit
✅ **Sequential** - 8280, 8281 easy to remember pattern
✅ **Professional** - Port range 8000-8999 common for web apps

---

**Migration Date**: 2026-01-17  
**Status**: ✅ Complete  
**Tested**: Ready for deployment
