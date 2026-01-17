# 📝 CHANGELOG - Twitter Bot

## [2.0.0] - 2025-12-21

### 🎉 Major Update: Simplified Template System

#### ✨ Added
- **New template system**: Full text templates (no complex variables!)
- **Media per template**: Each tweet can have different image/video
- **Backward compatibility**: Old format still works
- **Documentation**: `docs/NEW_TEMPLATE_SYSTEM.md` with complete guide
- **Project cleanup**: Organized documentation in `docs/` folder

#### 🔄 Changed
- **content_generator.py**: Simplified variable system
  - Removed: `_get_price_data()`, `_get_base_variables()`
  - Added: `_fill_wa_variables()` (simple fill for WA variables only)
  - Updated: `generate_promo_tweet()` now returns `(text, media)`
  
- **templates.yaml**: New format
  ```yaml
  # Old format (deprecated but still works):
  - "🔥 KUOTA XL {paket} cuma {harga}!"
  
  # New format (recommended):
  - text: "🔥 KUOTA XL 10GB cuma Rp25.000!"
    media: "media/promo/image.jpg"  # Optional
  ```

- **settings.yaml**: Simplified
  - Removed: `business.prices` section (not needed anymore!)
  - Keep: `wa_number`, `wa_link`, `product`, `niche`

- **automation.py**: Support media from templates
  - `run_morning_slot()`: Get media from template
  - `run_evening_slot()`: Get media from template

- **dashboard.py**: Updated preview function
  - Only fills WA variables (`{wa_number}`, `{wa_link}`)

#### 🗂️ Project Structure
- Created `docs/` folder for all documentation
- Moved 8 MD files from root to `docs/`
- Deleted 8 unnecessary files (Go files, PDFs, test files)
- Updated README.md with new structure
- Updated .gitignore for better security

#### 📖 Documentation
- `docs/NEW_TEMPLATE_SYSTEM.md` - Complete guide for new system
- `docs/README.md` - Index of all documentation
- Updated all config files for XL Akrab variant
- `config/settings_akrab.yaml` - Updated (prices → prices_reference)
- `config/templates_akrab.yaml` - Updated with full text templates

#### ✅ Benefits
1. **Simpler**: Edit 1 file only (`templates.yaml`)
2. **More custom**: Write tweets as you like, different styles
3. **More flexible**: Mix different packages & prices in one list
4. **Media per template**: Each tweet can have different image
5. **Faster**: No complex variable replacement logic
6. **Cleaner project**: Organized documentation structure

---

## [1.0.0] - Previous Version

### Features
- Twitter automation with scheduling
- AI-powered content improvement
- Dynamic template system with variables
- Metrics tracking with SQLite
- Web dashboard for monitoring
- Rate limiting & safety features
- Support for XL and XL Akrab products

---

## Migration Guide: v1 → v2

### For Regular Users:

**Option 1: Use New System (Recommended)**
1. Backup old templates: `cp config/templates.yaml config/templates.yaml.backup`
2. Edit `config/templates.yaml` with new format (full text)
3. Remove prices from `config/settings.yaml` (optional)
4. Test: `python main.py --run-once morning`

**Option 2: Keep Old System**
- No action needed! Old format still works
- But you miss benefits of new system

### For Developers:

**API Changes:**
```python
# Old (v1):
tweet = await content_gen.generate_promo_tweet(use_ai=True)

# New (v2):
tweet, media = await content_gen.generate_promo_tweet(use_ai=True)
```

**Template Format:**
```yaml
# Old (still works):
promo_templates:
  - "🔥 KUOTA XL {paket} cuma {harga}!"

# New (recommended):
promo_templates:
  - text: "🔥 KUOTA XL 10GB cuma Rp25.000!"
    media: null
```

---

## Roadmap

### v2.1 (Planned)
- [ ] Dashboard UI for template editor with media upload
- [ ] Template preview with real-time character count
- [ ] Bulk template import/export
- [ ] Template scheduling (specific template for specific time)

### v2.2 (Future)
- [ ] A/B testing for templates
- [ ] Template performance analytics
- [ ] Auto-optimization based on engagement
- [ ] Multi-account support

---

## Breaking Changes

### v2.0.0
- ⚠️ `generate_promo_tweet()` now returns tuple `(text, media)` instead of just `text`
- ⚠️ `business.prices` in settings.yaml is deprecated (use `prices_reference` or remove)
- ✅ Backward compatible: Old template format still works

---

## Credits

- **Developer**: [Your Name]
- **Version**: 2.0.0
- **Last Updated**: 2025-12-21
- **License**: Private Project

---

For more information, see:
- `docs/NEW_TEMPLATE_SYSTEM.md` - Complete guide
- `docs/USAGE.md` - Usage guide
- `README.md` - Project overview
