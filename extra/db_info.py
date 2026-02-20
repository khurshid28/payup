"""
Database Info Script - Bazadagi ma'lumotlarni ko'rish
======================================================
Ishlatish: python extra/db_info.py

Bu script bazadagi:
- Jadvallar ro'yxati
- Har bir jadvaldagi yozuvlar soni
- Oxirgi yozuvlar
ni ko'rsatadi.
"""
import os
import sys
import sqlite3
from datetime import datetime

# Django sozlamalarini yuklash
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payup.settings')

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3')


def get_db_connection():
    """SQLite bazaga ulanish"""
    return sqlite3.connect(DB_PATH)


def get_all_tables():
    """Barcha jadvallar ro'yxatini olish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables


def get_table_row_count(table_name):
    """Jadvaldagi yozuvlar sonini olish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
    except sqlite3.Error:
        count = "Xatolik"
    conn.close()
    return count


def get_table_columns(table_name):
    """Jadval ustunlarini olish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [(row[1], row[2]) for row in cursor.fetchall()]
    conn.close()
    return columns


def get_last_records(table_name, limit=5):
    """Oxirgi yozuvlarni olish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT {limit};")
        records = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
    except sqlite3.Error as e:
        records = []
        columns = []
    conn.close()
    return columns, records


def get_db_size():
    """Baza hajmini olish"""
    if os.path.exists(DB_PATH):
        size_bytes = os.path.getsize(DB_PATH)
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
    return "Topilmadi"


def print_separator(char="=", length=60):
    print(char * length)


def main():
    print_separator()
    print("📊 PAYUP DATABASE MA'LUMOTLARI")
    print_separator()
    print(f"📁 Baza joylashuvi: {DB_PATH}")
    print(f"📦 Baza hajmi: {get_db_size()}")
    print(f"📅 Tekshirilgan vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_separator()
    
    tables = get_all_tables()
    print(f"\n📋 JADVALLAR ({len(tables)} ta):\n")
    
    # Asosiy jadvallar
    main_tables = ['customer', 'contract', 'organization', 'branch', 'pledge', 'report2', 'generated_doc_pdf']
    
    print("🔹 ASOSIY JADVALLAR:")
    print("-" * 50)
    print(f"{'Jadval nomi':<25} {'Yozuvlar soni':>15}")
    print("-" * 50)
    
    for table in main_tables:
        if table in tables:
            count = get_table_row_count(table)
            print(f"  {table:<23} {count:>15}")
    
    print("-" * 50)
    
    # Boshqa jadvallar
    other_tables = [t for t in tables if t not in main_tables and not t.startswith('sqlite_') and not t.startswith('django_') and not t.startswith('auth_')]
    
    if other_tables:
        print("\n🔹 BOSHQA JADVALLAR:")
        print("-" * 50)
        for table in other_tables:
            count = get_table_row_count(table)
            print(f"  {table:<23} {count:>15}")
        print("-" * 50)
    
    # Django/System jadvallar
    system_tables = [t for t in tables if t.startswith('django_') or t.startswith('auth_') or t.startswith('sqlite_')]
    
    if system_tables:
        print("\n🔹 TIZIM JADVALLARI:")
        print("-" * 50)
        for table in system_tables:
            count = get_table_row_count(table)
            print(f"  {table:<23} {count:>15}")
    
    # Customer oxirgi yozuvlari
    print_separator()
    print("\n👤 OXIRGI 5 TA MIJOZ (customer):")
    print("-" * 70)
    columns, records = get_last_records('customer', 5)
    if records:
        for record in records:
            # id, fullname, phone1 ko'rsatish
            record_dict = dict(zip(columns, record))
            print(f"  ID: {record_dict.get('id', 'N/A'):<5} | {record_dict.get('fullname', 'N/A'):<30} | Tel: {record_dict.get('phone1', 'N/A')}")
    else:
        print("  Ma'lumot topilmadi")
    
    # Report oxirgi yozuvlari
    print("\n📝 OXIRGI 5 TA HISOBOT (report2):")
    print("-" * 70)
    columns, records = get_last_records('report2', 5)
    if records:
        for record in records:
            record_dict = dict(zip(columns, record))
            print(f"  ID: {record_dict.get('id', 'N/A'):<5} | State: {record_dict.get('state', 'N/A'):<3} | Created: {record_dict.get('created_at', 'N/A')}")
    else:
        print("  Ma'lumot topilmadi")
    
    print_separator()
    print("✅ Tahlil tugadi!")


if __name__ == "__main__":
    main()
