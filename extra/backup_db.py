"""
Database Backup Script - SQLite bazani zaxiralash
==================================================
Ishlatish: python extra/backup_db.py

Bu script:
- db.sqlite3 faylini zaxira qiladi
- Sana va vaqt bilan nomlaydi
- Eski zaxiralarni boshqarish
"""
import os
import sys
import shutil
from datetime import datetime, timedelta

# Loyiha root papkasi
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Papkalar
DB_FILE = os.path.join(BASE_DIR, 'db.sqlite3')
BACKUP_DIR = os.path.join(BASE_DIR, 'extra', 'backups')


def print_separator(char="=", length=60):
    print(char * length)


def ensure_backup_dir():
    """Zaxira papkasini yaratish"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"📁 Zaxira papkasi yaratildi: {BACKUP_DIR}")


def format_size(size_bytes):
    """Hajmni o'qilishi oson formatga o'tkazish"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def create_backup():
    """Yangi zaxira yaratish"""
    if not os.path.exists(DB_FILE):
        print(f"❌ Baza topilmadi: {DB_FILE}")
        return None
    
    ensure_backup_dir()
    
    # Zaxira fayl nomi
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"db_backup_{timestamp}.sqlite3"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    try:
        # Faylni nusxalash
        shutil.copy2(DB_FILE, backup_path)
        backup_size = os.path.getsize(backup_path)
        print(f"✅ Zaxira yaratildi: {backup_name}")
        print(f"   Hajmi: {format_size(backup_size)}")
        return backup_path
    except Exception as e:
        print(f"❌ Zaxira yaratishda xatolik: {e}")
        return None


def list_backups():
    """Mavjud zaxiralarni ko'rsatish"""
    ensure_backup_dir()
    
    backups = []
    for filename in os.listdir(BACKUP_DIR):
        if filename.startswith('db_backup_') and filename.endswith('.sqlite3'):
            filepath = os.path.join(BACKUP_DIR, filename)
            backups.append({
                'name': filename,
                'path': filepath,
                'size': os.path.getsize(filepath),
                'modified': datetime.fromtimestamp(os.path.getmtime(filepath))
            })
    
    # Sanaga qarab tartiblash (yangilari birinchi)
    backups.sort(key=lambda x: x['modified'], reverse=True)
    return backups


def show_backups():
    """Zaxiralar ro'yxatini ko'rsatish"""
    backups = list_backups()
    
    if not backups:
        print("📭 Hozircha zaxira yo'q")
        return []
    
    print(f"\n📦 MAVJUD ZAXIRALAR ({len(backups)} ta):")
    print("-" * 70)
    print(f"  {'#':<3} {'Fayl nomi':<35} {'Hajmi':>12} {'Sana':>15}")
    print("-" * 70)
    
    for i, backup in enumerate(backups, 1):
        date_str = backup['modified'].strftime('%Y-%m-%d %H:%M')
        print(f"  {i:<3} {backup['name']:<35} {format_size(backup['size']):>12} {date_str:>15}")
    
    print("-" * 70)
    
    # Jami hajm
    total_size = sum(b['size'] for b in backups)
    print(f"  {'JAMI:':<38} {format_size(total_size):>12}")
    
    return backups


def restore_backup(backup_path):
    """Zaxiradan tiklash"""
    if not os.path.exists(backup_path):
        print(f"❌ Zaxira topilmadi: {backup_path}")
        return False
    
    # Avval joriy bazani zaxiralash
    print("📦 Joriy ma'lumotlar zaxiralanmoqda...")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    current_backup = os.path.join(BACKUP_DIR, f"db_before_restore_{timestamp}.sqlite3")
    
    try:
        shutil.copy2(DB_FILE, current_backup)
        print(f"✅ Joriy baza zaxiralandi: {os.path.basename(current_backup)}")
    except Exception as e:
        print(f"⚠️  Joriy bazani zaxiralashda xatolik: {e}")
    
    # Tiklash
    try:
        shutil.copy2(backup_path, DB_FILE)
        print(f"✅ Baza tiklandi!")
        return True
    except Exception as e:
        print(f"❌ Tiklashda xatolik: {e}")
        return False


def delete_old_backups(keep_count=5):
    """Eski zaxiralarni o'chirish (oxirgi N tasini saqlab)"""
    backups = list_backups()
    
    if len(backups) <= keep_count:
        print(f"ℹ️  {len(backups)} ta zaxira bor, o'chirishga hojat yo'q")
        return 0
    
    deleted_count = 0
    for backup in backups[keep_count:]:
        try:
            os.remove(backup['path'])
            print(f"  🗑️  O'chirildi: {backup['name']}")
            deleted_count += 1
        except OSError as e:
            print(f"  ⚠️  O'chirib bo'lmadi: {backup['name']} - {e}")
    
    return deleted_count


def main():
    """Asosiy funksiya"""
    print_separator()
    print("💾 DATABASE BACKUP SCRIPT")
    print_separator()
    print(f"📅 Vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Baza: {DB_FILE}")
    
    if os.path.exists(DB_FILE):
        print(f"📦 Hajmi: {format_size(os.path.getsize(DB_FILE))}")
    else:
        print("❌ Baza topilmadi!")
        return
    
    # Mavjud zaxiralarni ko'rsat
    backups = show_backups()
    
    print_separator()
    print("\n🔧 TANLOV:")
    print("  1. Yangi zaxira yaratish")
    print("  2. Zaxiradan tiklash")
    print("  3. Eski zaxiralarni o'chirish (oxirgi 5 tasini saqlab)")
    print("  4. Chiqish")
    print()
    
    try:
        choice = input("Tanlovingiz (1/2/3/4): ").strip()
    except EOFError:
        choice = "4"
    
    print()
    
    if choice == "1":
        create_backup()
        
    elif choice == "2":
        if not backups:
            print("❌ Tiklash uchun zaxira yo'q")
        else:
            try:
                num = input("Qaysi zaxirani tiklash? (raqam): ").strip()
                num = int(num) - 1
                if 0 <= num < len(backups):
                    print(f"\n⚠️  OGOHLANTIRISH: Joriy ma'lumotlar yo'qoladi!")
                    confirm = input("Davom etasizmi? (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        restore_backup(backups[num]['path'])
                    else:
                        print("Bekor qilindi")
                else:
                    print("❌ Noto'g'ri raqam")
            except (ValueError, EOFError):
                print("❌ Noto'g'ri kiritma")
                
    elif choice == "3":
        deleted = delete_old_backups(keep_count=5)
        print(f"✅ {deleted} ta eski zaxira o'chirildi")
        
    else:
        print("Chiqildi")
    
    print()
    print_separator()
    print("✅ Tugadi!")


def backup_silent():
    """
    Skriptdan chaqirish uchun - foydalanuvchi kiritishisiz ishlaydi
    Ishlatish: from backup_db import backup_silent; backup_silent()
    """
    return create_backup()


if __name__ == "__main__":
    # Agar --create argument berilsa
    if len(sys.argv) > 1:
        if sys.argv[1] == "--create":
            create_backup()
        elif sys.argv[1] == "--list":
            show_backups()
        elif sys.argv[1] == "--cleanup":
            keep = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            delete_old_backups(keep_count=keep)
    else:
        main()
