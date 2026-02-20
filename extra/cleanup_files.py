"""
Generated Files Cleanup Script - Yaratilgan fayllarni tozalash
===============================================================
Ishlatish: python extra/cleanup_files.py

Bu script:
- media/uploads/generated papkasidagi fayllarni ko'rsatadi
- Eski fayllarni o'chirish imkonini beradi
- Papka hajmini hisoblab ko'rsatadi

Papkalar:
- media/uploads/generated/docx/  - DOCX fayllar
- media/uploads/generated/excel/ - Excel fayllar
- media/uploads/generated/pdf/   - PDF fayllar
"""
import os
import sys
from datetime import datetime, timedelta
import shutil

# Loyiha root papkasi
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GENERATED_DIRS = {
    'docx': os.path.join(BASE_DIR, 'media', 'uploads', 'generated', 'docx'),
    'excel': os.path.join(BASE_DIR, 'media', 'uploads', 'generated', 'excel'),
    'pdf': os.path.join(BASE_DIR, 'media', 'uploads', 'generated', 'pdf'),
}


def print_separator(char="=", length=60):
    print(char * length)


def get_folder_size(path):
    """Papka hajmini hisoblash"""
    total_size = 0
    file_count = 0
    
    if not os.path.exists(path):
        return 0, 0
    
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(filepath)
                file_count += 1
            except OSError:
                pass
    
    return total_size, file_count


def format_size(size_bytes):
    """Hajmni o'qilishi oson formatga o'tkazish"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def get_files_by_age(path, days=7):
    """Fayllarni yoshiga qarab ajratish"""
    if not os.path.exists(path):
        return [], []
    
    old_files = []
    new_files = []
    cutoff_time = datetime.now() - timedelta(days=days)
    
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                file_info = {
                    'path': filepath,
                    'name': filename,
                    'size': os.path.getsize(filepath),
                    'modified': mtime
                }
                
                if mtime < cutoff_time:
                    old_files.append(file_info)
                else:
                    new_files.append(file_info)
            except OSError:
                pass
    
    return old_files, new_files


def show_folder_stats():
    """Papkalar statistikasini ko'rsatish"""
    print_separator()
    print("📁 YARATILGAN FAYLLAR STATISTIKASI")
    print_separator()
    print(f"📅 Vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    total_size = 0
    total_files = 0
    
    print(f"{'Papka':<20} {'Fayllar soni':>15} {'Hajmi':>15}")
    print("-" * 55)
    
    for name, path in GENERATED_DIRS.items():
        size, count = get_folder_size(path)
        total_size += size
        total_files += count
        print(f"  {name:<18} {count:>15} {format_size(size):>15}")
    
    print("-" * 55)
    print(f"  {'JAMI:':<18} {total_files:>15} {format_size(total_size):>15}")
    print()
    
    return total_files, total_size


def show_old_files(days=7):
    """Eski fayllarni ko'rsatish"""
    print(f"\n📅 {days} kundan eski fayllar:")
    print("-" * 55)
    
    all_old_files = []
    
    for name, path in GENERATED_DIRS.items():
        old_files, _ = get_files_by_age(path, days)
        if old_files:
            print(f"\n  📂 {name.upper()}:")
            for f in old_files[:5]:  # Faqat 5 tasini ko'rsat
                print(f"     - {f['name'][:40]:<40} | {format_size(f['size']):>10}")
            if len(old_files) > 5:
                print(f"     ... va yana {len(old_files) - 5} ta fayl")
            all_old_files.extend(old_files)
    
    if not all_old_files:
        print(f"  ✅ {days} kundan eski fayl yo'q")
    
    return all_old_files


def delete_old_files(days=7):
    """Eski fayllarni o'chirish"""
    deleted_count = 0
    deleted_size = 0
    
    for name, path in GENERATED_DIRS.items():
        old_files, _ = get_files_by_age(path, days)
        for f in old_files:
            try:
                os.remove(f['path'])
                deleted_count += 1
                deleted_size += f['size']
            except OSError as e:
                print(f"  ⚠️  O'chirib bo'lmadi: {f['name']} - {e}")
    
    return deleted_count, deleted_size


def clear_all_generated_files():
    """Barcha yaratilgan fayllarni o'chirish"""
    deleted_count = 0
    deleted_size = 0
    
    for name, path in GENERATED_DIRS.items():
        if not os.path.exists(path):
            continue
            
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            try:
                if os.path.isfile(filepath):
                    deleted_size += os.path.getsize(filepath)
                    os.remove(filepath)
                    deleted_count += 1
                elif os.path.isdir(filepath):
                    deleted_size += get_folder_size(filepath)[0]
                    shutil.rmtree(filepath)
                    deleted_count += 1
            except OSError as e:
                print(f"  ⚠️  O'chirib bo'lmadi: {filename} - {e}")
    
    return deleted_count, deleted_size


def main():
    """Asosiy funksiya"""
    print_separator()
    print("🧹 GENERATED FILES CLEANUP SCRIPT")
    print_separator()
    
    # Statistika ko'rsat
    total_files, total_size = show_folder_stats()
    
    if total_files == 0:
        print("✅ Yaratilgan fayllar papkasi bo'sh")
        print_separator()
        return
    
    # Eski fayllarni ko'rsat
    old_files = show_old_files(days=7)
    
    print_separator()
    print("\n🔧 TANLOV:")
    print("  1. Faqat 7 kundan eski fayllarni o'chirish")
    print("  2. Faqat 30 kundan eski fayllarni o'chirish")
    print("  3. BARCHA fayllarni o'chirish (ehtiyot bo'ling!)")
    print("  4. Chiqish")
    print()
    
    try:
        choice = input("Tanlovingiz (1/2/3/4): ").strip()
    except EOFError:
        choice = "4"
    
    print()
    
    if choice == "1":
        print("🗑️  7 kundan eski fayllar o'chirilmoqda...")
        count, size = delete_old_files(days=7)
        print(f"✅ {count} ta fayl o'chirildi ({format_size(size)})")
        
    elif choice == "2":
        print("🗑️  30 kundan eski fayllar o'chirilmoqda...")
        count, size = delete_old_files(days=30)
        print(f"✅ {count} ta fayl o'chirildi ({format_size(size)})")
        
    elif choice == "3":
        print("⚠️  OGOHLANTIRISH: Barcha yaratilgan fayllar o'chiriladi!")
        try:
            confirm = input("Davom etasizmi? (yes/no): ").strip().lower()
        except EOFError:
            confirm = "no"
            
        if confirm == 'yes':
            print("🗑️  Barcha fayllar o'chirilmoqda...")
            count, size = clear_all_generated_files()
            print(f"✅ {count} ta fayl o'chirildi ({format_size(size)})")
        else:
            print("Bekor qilindi")
    else:
        print("Chiqildi")
    
    print()
    print_separator()
    print("✅ Tugadi!")


def cleanup_old_files_silent(days=7):
    """
    Skriptdan chaqirish uchun - foydalanuvchi kiritishisiz ishlaydi
    Ishlatish: from cleanup_files import cleanup_old_files_silent; cleanup_old_files_silent(7)
    """
    count, size = delete_old_files(days=days)
    return count, size


if __name__ == "__main__":
    # Agar --silent argument berilsa
    if len(sys.argv) > 1:
        if sys.argv[1] == "--silent":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            count, size = cleanup_old_files_silent(days)
            print(f"O'chirildi: {count} ta fayl ({format_size(size)})")
        elif sys.argv[1] == "--stats":
            show_folder_stats()
    else:
        main()
