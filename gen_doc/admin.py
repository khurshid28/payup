from django.contrib import admin

from gen_doc.models import DocxTemplate, GeneratedDocPdfModel

@admin.register(DocxTemplate)
class DocxTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'shartnoma', 'buyruq', 'product_type')


