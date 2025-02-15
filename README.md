## ChatGPT PROMT matni 
``` 
Windows server 2022 quyidagi ishlarni bajarish kerak:
1. Postgresql o'rnatish va db yaratish, user: ulugbek, dbname: payupdb, password: nc778119 bo'lsin
2. PGadmin ornatish va Postgresql ulanish
3. Djangoni production deploy qilish va postgresqlda yaratilgan db ulash
4. Apache server o'rnatish va djangoni unga sozlash
5. STATIC, MEDIA fayllar bilan ishlashni sodda tushintir
6. Hammasini oddiy tilda example shaklida yo'riqnoma tayyorlab ber
```

# Quyida Windows Server 2022 ga Django loyihasini PostgreSQL va Apache bilan ishlab chiqarish muhitida deploy qilish bo‘yicha sodda va tushunarli yo‘riqnoma keltirilgan.


# 1. PostgreSQL o‘rnatish va baza yaratish
## 1.1 PostgreSQL o‘rnatish
### PostgreSQL yuklab oling: https://www.postgresql.org/download/windows/
### O‘rnatish jarayonida quyidagilarni tanlang:

```
Database Server
1. pgAdmin 4
2. Command Line Tools
3. O‘rnatish tugagach, PostgreSQL xizmatini ishga tushiring.
```

# 1.2 Yangi ma'lumotlar bazasini yaratish. PostgreSQL ni oching va quyidagi buyruqlarni bajaring:
```
CREATE DATABASE payupdb;
CREATE USER ulugbek WITH ENCRYPTED PASSWORD 'nc778119';
ALTER ROLE ulugbek SET client_encoding TO 'utf8';
ALTER ROLE ulugbek SET default_transaction_isolation TO 'read committed';
ALTER ROLE ulugbek SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE payupdb TO ulugbek;
```

# 2. pgAdmin o‘rnatish va PostgreSQL-ga ulanish
``` 
pgAdmin 4 ni ishga tushiring.
Serverni qo‘shish uchun:
Host: localhost
Port: 5432
Username: ulugbek
Password: nc778119
Bazani ochib, payupdb mavjudligini tekshiring.
```
# 3. Django loyihasini Windows Server-ga deploy qilish
## 3.1 Python va kerakli modullarni o‘rnatish
### Python yuklab oling va o‘rnating:
👉 https://www.python.org/downloads/windows/

### Python uchun pip va virtual environment modullarini o‘rnating:
```
python -m pip install --upgrade pip
pip install virtualenv
```

## Django loyihasini yuklab oling va virtual muhit yarating:
```
git clone https://github.com/username/project.git
cd project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 3.2 Django-ni PostgreSQL-ga ulash
### 1. Django loyihangizdagi settings.py faylida quyidagilarni sozlang:
``` 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'payupdb',
        'USER': 'ulugbek',
        'PASSWORD': 'nc778119',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
### 2. Migratsiyalarni ishga tushiring:
``` 
python manage.py migrate
python manage.py createsuperuser

```

### 3. Statik fayllarni yig‘ish:
``` 
python manage.py collectstatic --noinput
```

# 4. Apache o‘rnatish va Django-ni unga sozlash
## 4.1. Apache HTTP Server o‘rnatish
Apache yuklab oling va o‘rnating:
👉 https://www.apachelounge.com/download/
Apache-ni C:\Apache24 papkasiga joylashtiring.
Apache-ni ishga tushirish:

````
httpd -k install
httpd -k start
````

# 4.2 Apache-ni Django bilan ulash
## 1. Django loyihasida WSGI serverni o‘rnating:
```
 pip install mod_wsgi
```
## 2. Keyin quyidagi buyruq bilan tekshiring:
``` 
mod_wsgi-express module-config
```

## 2. httpd.conf faylida quyidagilarni qo‘shing:
````
LoadModule wsgi_module "C:/path_to_your_virtualenv/venv/Lib/site-packages/mod_wsgi/server/mod_wsgi.cp311-win_amd64.pyd"

WSGIPythonHome "C:/path_to_your_virtualenv/venv"
WSGIScriptAlias / "C:/path_to_your_django_project/project/wsgi.py"

<Directory "C:/path_to_your_django_project">
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>
````

## 3. Apache xizmatini qayta yuklang:
```
httpd -k restart
```

# 5. STATIC va MEDIA fayllarni sozlash
## 1. Django settings.py faylida quyidagilarni qo‘shing:
````
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
````

## 2. Apache httpd.conf faylida quyidagilarni qo‘shing:
```` 
# Python DLL yuklash
LoadFile "C:/Users/Администратор/AppData/Local/Programs/Python/Python312/python312.dll"

# mod_wsgi yuklash
LoadModule wsgi_module "C:/DjangoApp/venv/Lib/site-packages/mod_wsgi/server/mod_wsgi.cp312-win_amd64.pyd"

# WSGI muhitini o‘rnatish
WSGIPythonHome "C:/DjangoApp/venv"
WSGIPythonPath "C:/DjangoApp/myproject"

# Django loyihasi uchun WSGI sozlamalari
WSGIScriptAlias / "C:/DjangoApp/myproject/myproject/wsgi.py"
WSGIPythonHome "C:/DjangoApp/venv"
WSGIPythonPath "C:/DjangoApp/myproject"

<Directory "C:/DjangoApp/myproject/myproject">
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>

# Django static fayllar
Alias /static "C:/DjangoApp/myproject/staticfiles/"
<Directory "C:/DjangoApp/myproject/staticfiles">
    Require all granted
</Directory>
````
## 3. Django statik fayllarni yig‘ish:
``` 
python manage.py collectstatic --noinput
```

# 6. Django serverini doimiy ishlashga moslash
## 1. Windows Services orqali Django-ni avtomatik ishga tushirish:
``` 
Task Scheduler -> "Create Basic Task"
Ishga tushirish:
python manage.py runserver 0.0.0.0:8000
```
## 2. Ishga tushirishni tekshirish
```
curl http://127.0.0.1:8000
```

##  Shu bosqichlardan so‘ng Django loyihangiz PostgreSQL, Apache va statik fayllar bilan to‘liq ishlab chiqarish (production) muhitida ishlaydi!

# Qo'shimchalar
## 1. Microsoft Visual C++ Build Tools ni o‘rnatish
## Sizga Microsoft Visual C++ 14.0 yoki undan yangi versiya kerak. Quyidagi bosqichlarni bajaring:

### Rasmiy sayt ga kiring.
### "Download Build Tools" tugmasini bosing.
### Visual Studio Installer ochiladi.
### C++ Build Tools ni tanlang va quyidagilarni belgilang:
### ✅ MSVC v142 - Visual C++ build tools
### ✅ Windows 10 SDK
### ✅ C++ CMake tools for Windows

O‘rnatishni boshlang va tugashini kuting.
⏳ O‘rnatish tugagach, kompyuterni qayta yuklang.