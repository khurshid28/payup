# 🛠️ Extra Scripts - PayUp Utility Tools

Bu papkada PayUp loyihasini boshqarish uchun yordamchi skriptlar mavjud.

## 📋 Skriptlar Ro'yxati

| Skript | Vazifasi |
|--------|----------|
| `db_info.py` | Bazadagi ma'lumotlarni ko'rish |
| `cleanup_excel.py` | Excel jarayonlarini o'chirish |
| `cleanup_files.py` | Yaratilgan fayllarni tozalash |
| `backup_db.py` | Bazani zaxiralash va tiklash |

---

## 📊 db_info.py - Database Info

Bazadagi jadvallar va ma'lumotlar statistikasini ko'rsatadi.

### Ishlatish:
```bash
cd c:\payup_by_dilmurod\payup
python extra\db_info.py
```

### Natija:
- Jadvallar ro'yxati
- Har bir jadvaldagi yozuvlar soni
- Oxirgi mijozlar va hisobotlar
- Baza hajmi

---

## 🧹 cleanup_excel.py - Excel Cleanup

Ochiq Excel jarayonlarini to'g'ri yopadi (COM resource leak oldini oladi).

### Ishlatish:
```bash
# Interaktiv rejim
python extra\cleanup_excel.py

# Avtomatik rejim (skriptdan chaqirish uchun)
python extra\cleanup_excel.py --silent
```

### Tanlovlar:
1. **To'g'ri yopish** - COM orqali workbooklarni yopadi (tavsiya etiladi)
2. **Majburiy o'chirish** - taskkill bilan o'chiradi

### ⚠️ Ogohlantirish:
Bu skript boshqa ochiq Excel fayllaringizni ham yopishi mumkin!

---

## 🗑️ cleanup_files.py - Generated Files Cleanup

`media/uploads/generated/` papkasidagi fayllarni boshqaradi.

### Papkalar:
- `media/uploads/generated/docx/` - DOCX fayllar
- `media/uploads/generated/excel/` - Excel fayllar  
- `media/uploads/generated/pdf/` - PDF fayllar

### Ishlatish:
```bash
# Interaktiv rejim
python extra\cleanup_files.py

# Faqat statistika
python extra\cleanup_files.py --stats

# Avtomatik rejim (7 kundan eski fayllarni o'chirish)
python extra\cleanup_files.py --silent 7
```

### Tanlovlar:
1. 7 kundan eski fayllarni o'chirish
2. 30 kundan eski fayllarni o'chirish
3. BARCHA fayllarni o'chirish

---

## 💾 backup_db.py - Database Backup

SQLite bazani zaxiralash va tiklash.

### Ishlatish:
```bash
# Interaktiv rejim
python extra\backup_db.py

# Yangi zaxira yaratish
python extra\backup_db.py --create

# Zaxiralar ro'yxati
python extra\backup_db.py --list

# Eski zaxiralarni o'chirish (oxirgi 5 tasini saqlab)
python extra\backup_db.py --cleanup 5
```

### Zaxira joylashuvi:
```
extra/backups/
  db_backup_20250220_143000.sqlite3
  db_backup_20250219_120000.sqlite3
  ...
```

### Tanlovlar:
1. Yangi zaxira yaratish
2. Zaxiradan tiklash
3. Eski zaxiralarni o'chirish

---

## 🔧 Skriptlardan Python'da chaqirish

```python
# Excel tozalash
from extra.cleanup_excel import cleanup_silent
cleanup_silent()

# Fayllarni tozalash
from extra.cleanup_files import cleanup_old_files_silent
count, size = cleanup_old_files_silent(days=7)

# Baza zaxiralash
from extra.backup_db import backup_silent
backup_path = backup_silent()
```

---

## 📝 Tavsiyalar

1. **Har kuni** `backup_db.py --create` ishga tushiring
2. **Har hafta** `cleanup_files.py` bilan eski fayllarni tozalang
3. Agar Excel "qotib" qolsa, `cleanup_excel.py` ishlating
4. `db_info.py` bilan bazani muntazam tekshiring

---

## 🔗 Bog'liq fayllar

- `ANALYSIS_CLAUDE_OPUS.md` - Loyiha tahlili va tavsiyalar
- `requirements.txt` - Python kutubxonalari

---

> **Eslatma:** Skriptlarni loyiha root papkasidan (`c:\payup_by_dilmurod\payup`) ishga tushiring.
