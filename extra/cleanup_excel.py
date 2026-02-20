"""
Excel Cleanup Script - Excel jarayonlarini to'g'ri yopish
=========================================================
Ishlatish: python extra/cleanup_excel.py

Bu script:
- Ochiq Excel jarayonlarini ko'rsatadi
- Excel workbooklarini to'g'ri yopadi
- Kerak bo'lsa taskkill bilan majburiy o'chiradi

OGOHLANTIRISH: Bu boshqa Excel fayllaringizni ham yopishi mumkin!
"""
import os
import sys
import subprocess
from datetime import datetime

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    import win32com.client
    import pythoncom
    WIN32COM_AVAILABLE = True
except ImportError:
    WIN32COM_AVAILABLE = False


def print_separator(char="=", length=60):
    print(char * length)


def get_excel_processes():
    """Excel jarayonlarini topish"""
    if not PSUTIL_AVAILABLE:
        # psutil yo'q bo'lsa tasklist ishlatamiz
        try:
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq EXCEL.EXE'],
                capture_output=True, text=True
            )
            if 'EXCEL.EXE' in result.stdout:
                lines = result.stdout.strip().split('\n')
                return [line for line in lines if 'EXCEL.EXE' in line]
            return []
        except Exception as e:
            print(f"Xatolik: {e}")
            return []
    else:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'create_time']):
            if proc.info['name'] and 'excel' in proc.info['name'].lower():
                processes.append(proc.info)
        return processes


def close_excel_gracefully():
    """Excel'ni to'g'ri yopish (COM orqali)"""
    if not WIN32COM_AVAILABLE:
        print("⚠️  win32com kutubxonasi o'rnatilmagan")
        print("   O'rnatish: pip install pywin32")
        return False
    
    try:
        pythoncom.CoInitialize()
        excel = win32com.client.Dispatch("Excel.Application")
        
        workbooks = list(excel.Workbooks)
        if workbooks:
            print(f"📂 {len(workbooks)} ta ochiq workbook topildi:")
            for wb in workbooks:
                print(f"   - {wb.Name}")
                wb.Close(SaveChanges=False)
            print("✅ Barcha workbooklar yopildi")
        else:
            print("📂 Ochiq workbook yo'q")
        
        excel.Quit()
        del excel
        print("✅ Excel to'g'ri yopildi")
        return True
        
    except Exception as e:
        print(f"⚠️  Excel'ni to'g'ri yopib bo'lmadi: {e}")
        return False
        
    finally:
        pythoncom.CoUninitialize()


def force_kill_excel():
    """Excel'ni majburiy o'chirish"""
    print("🔨 Excel majburiy o'chirilmoqda...")
    result = os.system("taskkill /f /im excel.exe 2>nul")
    if result == 0:
        print("✅ Excel o'chirildi")
    else:
        print("ℹ️  Excel jarayoni topilmadi yoki allaqachon yopilgan")


def show_excel_status():
    """Excel holatini ko'rsatish"""
    print_separator()
    print("📊 EXCEL JARAYONLARI HOLATI")
    print_separator()
    print(f"📅 Vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    processes = get_excel_processes()
    
    if not processes:
        print("✅ Hech qanday Excel jarayoni ishlamayapti")
        return False
    
    print(f"⚠️  {len(processes)} ta Excel jarayoni topildi:")
    print()
    
    if PSUTIL_AVAILABLE:
        for proc in processes:
            memory_mb = proc.get('memory_info', None)
            if memory_mb:
                memory_mb = memory_mb.rss / (1024 * 1024)
            else:
                memory_mb = 0
            print(f"  PID: {proc['pid']:<8} | Memory: {memory_mb:.1f} MB")
    else:
        for line in processes:
            print(f"  {line}")
    
    return True


def main():
    """Asosiy funksiya"""
    print_separator()
    print("🧹 EXCEL CLEANUP SCRIPT")
    print_separator()
    
    # Excel holatini ko'rsat
    has_excel = show_excel_status()
    
    if not has_excel:
        print_separator()
        return
    
    print_separator()
    print("\n🔧 TANLOV:")
    print("  1. Excel'ni to'g'ri yopish (tavsiya etiladi)")
    print("  2. Majburiy o'chirish (taskkill)")
    print("  3. Chiqish")
    print()
    
    try:
        choice = input("Tanlovingiz (1/2/3): ").strip()
    except EOFError:
        choice = "1"  # Script mode uchun default
    
    print()
    
    if choice == "1":
        success = close_excel_gracefully()
        if not success:
            print("\n💡 To'g'ri yopib bo'lmadi. Majburiy o'chirishni xohlaysizmi? (y/n)")
            try:
                confirm = input().strip().lower()
            except EOFError:
                confirm = "y"
            if confirm == 'y':
                force_kill_excel()
    elif choice == "2":
        force_kill_excel()
    else:
        print("Chiqildi")
    
    print()
    print_separator()
    print("✅ Tugadi!")


def cleanup_silent():
    """
    Skriptdan chaqirish uchun - foydalanuvchi kiritishisiz ishlaydi
    Ishlatish: from cleanup_excel import cleanup_silent; cleanup_silent()
    """
    processes = get_excel_processes()
    if processes:
        success = close_excel_gracefully()
        if not success:
            force_kill_excel()
        return True
    return False


if __name__ == "__main__":
    # Agar --silent argument berilsa, interaktiv bo'lmagan rejimda ishlaydi
    if len(sys.argv) > 1 and sys.argv[1] == "--silent":
        cleanup_silent()
    else:
        main()
