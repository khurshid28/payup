import pythoncom
from docx2pdf import convert

pythoncom.CoInitialize()  # COM obyektlarini ishga tushirish
# DOCX fayl yo‘li
docx_file = r"C:\Users\Admin\PycharmProjects\payup\media\docx_org_templates\mikrokredit\mikrokredit_buyruq.docx"
pdf_file = r"C:\Users\Admin\PycharmProjects\payup\media"

# DOCXni PDFga aylantirish
convert(docx_file, pdf_file)

print("PDF yaratildi:", pdf_file)
