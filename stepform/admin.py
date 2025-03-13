from django.contrib import admin
from .models import Branch, DocxTemplate, GeneratedDocument, Application, Organization


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "contract_id", "customer_id", "state", "direktor_signature")
    list_filter = ("state", "created_at", "direktor_signature")
    search_fields = ("id", "contract_id", "customer_id", "owner_id")
    readonly_fields = ("created_at",)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'address', 'account_number', 'mfo', 'stir',
        'phone1', 'phone2', 'direktor_fullname', 'loan_head_fullname', 'monitoring_head_fullname'
    )
    search_fields = ('title', 'stir', 'direktor_fullname', 'loan_head_fullname', 'monitoring_head_fullname')
    list_filter = ('mfo',)



@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'head_initials_uz', 'state', 'created_by', 'created_at')
    list_filter = ('state', 'created_at')
    search_fields = ('title', 'head_initials_uz')
    ordering = ('-created_at',)

@admin.register(DocxTemplate)
class DocxTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_type', 'shartnoma', 'buyruq', 'dalolatnoma', 'bayonnoma', )
    search_fields = ('product_type', 'buyruq', 'dalolatnoma')
    list_filter = ('product_type',)
    ordering = ('id',)

@admin.register(GeneratedDocument)
class GeneratedDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'docx_shartnoma', 'pdf_shartnoma')
