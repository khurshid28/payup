from django.contrib import admin
from .models import Branch, DocxTemplate, GeneratedDocument


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'head_initials_uz', 'state', 'created_by', 'created_at')
    list_filter = ('state', 'created_at')
    search_fields = ('title', 'head_initials_uz')
    ordering = ('-created_at',)

@admin.register(DocxTemplate)
class DocxTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_type', 'shartnoma', 'buyruq', 'dalolatnoma')
    search_fields = ('product_type', 'buyruq', 'dalolatnoma')
    list_filter = ('product_type',)
    ordering = ('id',)

@admin.register(GeneratedDocument)
class GeneratedDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'docx_shartnoma', 'pdf_shartnoma')
