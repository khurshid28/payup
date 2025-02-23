import os
import time
import os
import pythoncom
import win32com.client
from datetime import datetime
from io import BytesIO

import qrcode, jinja2
from django.core.files.base import ContentFile, File
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert
from openpyxl.reader.excel import load_workbook

from payup import settings
from payup.settings import BASE_DIR, MEDIA_ROOT, GLOBAL_IP


class GenDocument:
    def __init__(self, generated_document=None, filename=None, shartnoma=None, buyruq=None, dalolatnoma=None,
                 grafik=None, context=None, application=None):
        self.generated_document = generated_document
        self.filename = filename
        self.shartnoma = shartnoma  # docx shaklidagi shartnoma template
        self.buyruq = buyruq  # docx shaklidagi buyruq template
        self.dalolatnoma = dalolatnoma  # docx shaklidagi dalolatnoma template
        self.grafik = grafik  # docx shaklidagi grafik template
        self.context = context  # application meta json
        self.application = application

    def display_info(self):
        print(self.generated_document)
        print(self.filename)
        print("shartnoma_template=", self.shartnoma)
        print(self.buyruq)
        print(self.dalolatnoma)
        print(self.grafik)
        print(self.context)
        print(self.application)
        return "ok"

    # Shartnoma yaratish
    def gen_shartnoma(self):
        # Application ID saqlab olish
        self.generated_document.application_id = self.application.id
        self.generated_document.save()

        # 1. Shablonni ochish
        docx = DocxTemplate(self.shartnoma)

        # 2. Shablonni to'ldirish va saqlash
        self.context['qr_code'] = "{{qr_code}}"
        docx.render(self.context)

        # 3. Faylni xotirada saqlash
        buffer = BytesIO()
        docx.save(buffer)
        buffer.seek(0)  # Faylni boshidan o‘qish uchun

        # 4. Modelga saqlash
        self.generated_document.docx_shartnoma.save(f"{self.filename}_shartnoma.docx",
                                                    ContentFile(buffer.getvalue()), save=True)

        # DOCXga QR-CODE joylashtirish va pdfga convert qilish
        pdf_filename = f"{self.filename}_shartnoma"
        pdf_url = self.generate_qr_pdf(self.generated_document.docx_shartnoma, pdf_filename)
        # Fayl yo‘lini nisbiy qilish (MEDIA_ROOT ni olib tashlash)
        relative_path = os.path.relpath(pdf_url, settings.MEDIA_ROOT).replace("\\", "/")
        # Faylni modelga saqlash
        self.generated_document.pdf_shartnoma.save(relative_path, File(open(pdf_url, "rb")), save=True)

        return self.generated_document

    # Buyruq yaratish
    def gen_buyruq(self):
        # 1. Shablonni ochish
        docx = DocxTemplate(self.buyruq)

        # 2. Shablonni to'ldirish va saqlash
        self.context['qr_code'] = "{{qr_code}}"
        docx.render(self.context)

        # 3. Faylni xotirada saqlash
        buffer = BytesIO()
        docx.save(buffer)
        buffer.seek(0)  # Faylni boshidan o‘qish uchun

        # 4. Modelga saqlash
        self.generated_document.docx_buyruq.save(f"{self.filename}_buyruq.docx", ContentFile(buffer.getvalue()),
                                                 save=True)

        # DOCXga QR-CODE joylashtirish va pdfga convert qilish
        pdf_filename = f"{self.filename}_buyruq"
        pdf_url = self.generate_qr_pdf(self.generated_document.docx_buyruq, pdf_filename)
        # Fayl yo‘lini nisbiy qilish (MEDIA_ROOT ni olib tashlash)
        relative_path = os.path.relpath(pdf_url, settings.MEDIA_ROOT).replace("\\", "/")
        # Faylni modelga saqlash
        self.generated_document.pdf_buyruq.save(relative_path, File(open(pdf_url, "rb")), save=True)

        return self.generated_document

    # Dalolatnoma yaratish
    def gen_dalolatnoma(self):
        # 1. Shablonni ochish
        docx = DocxTemplate(self.dalolatnoma)

        # 2. Shablonni to'ldirish va saqlash
        self.context['qr_code'] = "{{qr_code}}"
        docx.render(self.context)

        # 3. Faylni xotirada saqlash
        buffer = BytesIO()
        docx.save(buffer)
        buffer.seek(0)  # Faylni boshidan o‘qish uchun

        # 4. Modelga saqlash
        self.generated_document.docx_dalolatnoma.save(f"{self.filename}_dalolatnoma.docx",
                                                      ContentFile(buffer.getvalue()), save=True)

        # DOCXga QR-CODE joylashtirish va pdfga convert qilish
        pdf_filename = f"{self.filename}_dalolatnoma"
        pdf_url = self.generate_qr_pdf(self.generated_document.docx_dalolatnoma, pdf_filename)
        # Fayl yo‘lini nisbiy qilish (MEDIA_ROOT ni olib tashlash)
        relative_path = os.path.relpath(pdf_url, settings.MEDIA_ROOT).replace("\\", "/")
        # Faylni modelga saqlash
        self.generated_document.pdf_dalolatnoma.save(relative_path, File(open(pdf_url, "rb")), save=True)
        return self.generated_document

    # Gfafik yaratish
    def gen_grafik(self):
        # 1. Shablonni ochish
        docx = DocxTemplate(self.grafik)

        # 2. Shablonga EXCELdab olingan to'lov grafikni joylashtirish
        self.context['graphics'] = self.extract_excel()
        self.context['qr_code'] = "{{qr_code}}"
        docx.render(self.context)

        # 3. Faylni xotirada saqlash
        buffer = BytesIO()
        docx.save(buffer)
        buffer.seek(0)  # Faylni boshidan o‘qish uchun

        # 4. Modelga saqlash
        self.generated_document.docx_grafik.save(f"{self.filename}_grafik.docx", ContentFile(buffer.getvalue()),
                                                 save=True)
        # DOCXga QR-CODE joylashtirish va pdfga convert qilish
        pdf_filename = f"{self.filename}_grafik"
        pdf_url = self.generate_qr_pdf(self.generated_document.docx_grafik, pdf_filename)
        # Fayl yo‘lini nisbiy qilish (MEDIA_ROOT ni olib tashlash)
        relative_path = os.path.relpath(pdf_url, settings.MEDIA_ROOT).replace("\\", "/")
        # Faylni modelga saqlash
        self.generated_document.pdf_grafik.save(relative_path, File(open(pdf_url, "rb")), save=True)

        return self.generated_document

    # EXCELdan ma'lumotlarni o'qish
    def extract_excel(self):
        xlsx = self.application.xlsx
        wb = load_workbook(filename=xlsx, read_only=True, data_only=True)
        ws = wb['График']

        # Cheklangan qatordan o'qish
        data = []

        for row in ws.iter_rows(min_row=9, max_row=100, min_col=1, max_col=6, values_only=True):
            obj = {
                "id": row[0],
                "date": row[1].strftime('%d.%m.%Y') if type(row[1]) is datetime else row[1],
                "total_payment": '{:,.2f}'.format(row[2]) if type(row[2]) is float else row[2],
                "principal_balance": '{:,.2f}'.format(row[3]) if isinstance(row[3], float) else '{:,.0f}'.format(
                    row[3]),
                "interest_payment": '{:,.2f}'.format(row[4]) if isinstance(row[4], float) else '{:,.0f}'.format(row[4]),
                "principal_payment": '{:,.2f}'.format(row[5]) if isinstance(row[5], float) else '{:,.0f}'.format(
                    row[5]),
            }
            if obj['date'] != None and obj['id'] != None:
                data.append(obj)
            if obj["date"] == 'JAMI':
                obj['id'] = ""
                obj['total_payment'] = ""
                data.append(obj)
                break
        wb.close()
        print(data)
        return data

    def generate_qr_pdf(self, docx, pdf_filename):
        # QRCODE yaratish
        qr_file_name = f"{pdf_filename}.png"
        qr_file_path = os.path.join(settings.MEDIA_ROOT, "uploads/generated/qrcode", qr_file_name)

        # Papka mavjudligini tekshirish va yaratish
        os.makedirs(os.path.dirname(qr_file_path), exist_ok=True)

        # QR kod yaratish
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"{GLOBAL_IP}/media/uploads/generated/pdf/{pdf_filename}.pdf/")
        qr.make(fit=True)

        # QR kodni tasvirga aylantirish va saqlash
        img = qr.make_image(fill="black", back_color="white")
        img.save(qr_file_path)

        # WORD templatega qrcode joylashtirish
        # 1. Shablonni ochish
        docx = DocxTemplate(docx)
        # 2. Tasvirni yuklash va o'lchamini belgilash
        image_path = qr_file_path
        image = InlineImage(docx, image_path, width=Mm(30), height=Mm(30))  # 50mm x 50mm
        self.context['qr_code'] = image
        docx.render(self.context)
        # Saqlash joyi
        docx_output_name = f"{self.filename}_upd.docx"
        docx_output_path = os.path.join(settings.MEDIA_ROOT, "uploads/generated/docx", docx_output_name)

        # Papka mavjudligini tekshirish va yaratish
        os.makedirs(os.path.dirname(docx_output_path), exist_ok=True)

        # Tayyorlangan hujjatni saqlash
        docx.save(docx_output_path)

        # Docxni pdfga aylantirish
        pdf_output_name = f"{pdf_filename}.pdf"
        pdf_output_path = os.path.join(settings.MEDIA_ROOT, pdf_output_name)

        pythoncom.CoInitialize()  # COM obyektlarini ishga tushirish
        convert(docx_output_path, pdf_output_path)

        return pdf_output_path

    def remove_temp_files(self):
        # Katalog yo'li
        time.sleep(2)
        directory = settings.MEDIA_ROOT
        for filename in os.listdir(directory):
            # Faylning to'liq yo'li
            file_path = os.path.join(directory, filename)

            # Fayl `.pdf` bilan tugasa va u haqiqiy fayl bo'lsa
            if filename.endswith('.pdf') and os.path.isfile(file_path):
                os.remove(file_path)  # Faylni o'chiradi
                print(f"{file_path} fayli o'chirildi.")
        return print('Barcha fayllar ochirildi.')
