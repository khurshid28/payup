from django.contrib import admin
from .models import Branch, DocxTemplate, GeneratedDocument, Application, Organization, XlsxTemplate
from django.utils.safestring import mark_safe
import json


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "contract",
                    "customer",
                    "monitoring_head_signature",
                    "loan_head_signature",
                    "moderator_signature",
                    "direktor_signature",
                    'xlsx',
                    "state",
                    "created_at")
    list_display_links = ("id", "contract")
    search_fields = ("id",)
    list_editable = (
        'monitoring_head_signature', 'loan_head_signature', 'moderator_signature', 'direktor_signature', 'state')
    list_filter = ("state", "created_at", "direktor_signature")
    search_fields = ("id", "contract_id", "customer_id", "owner_id")
    readonly_fields = ("created_at",)

    # Meta ichidagi alohida key'larni chiqarish
    def contract(self, obj):
        """Meta ichidagi 'key1' ni chiqarish"""
        contract_number = obj.meta.get('contract')['contract_number']
        contract_date = obj.meta.get('contract')['contract_date']
        contract = f"{contract_date} yildagi {contract_number}-sonli shartnoma"
        return contract

    def customer(self, obj):
        """Meta ichidagi 'key2' ni chiqarish"""
        customer_fullname_initials = obj.meta.get('customer')['customer_fullname_initials']
        return customer_fullname_initials

    # Sarlavhalarni chiroyli qilish
    contract.short_description = "meta: contract"
    customer.short_description = "meta: customer"




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
    list_display = ('id', 'product_type', 'shartnoma', 'buyruq', 'dalolatnoma', 'bayonnoma',)
    search_fields = ('product_type', 'buyruq', 'dalolatnoma')
    list_filter = ('product_type',)
    ordering = ('id',)


@admin.register(GeneratedDocument)
class GeneratedDocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "application_id",  "contract", "customer", "has_all_files", "state", "created_at")
    list_filter = ("state", "created_at")
    search_fields = ("id", "application_id")
    readonly_fields = ("created_at",)

    # Hujjatlar bor-yo'qligini tekshirish uchun
    def has_all_files(self, obj):
        """Barcha PDF hujjatlar yuklanganmi yoki yo‘qmi ko‘rsatish"""
        files = [
            obj.pdf_shartnoma,
            obj.pdf_buyruq,
            obj.pdf_dalolatnoma,
            obj.pdf_grafik,
            obj.pdf_bayonnoma,
            obj.pdf_xulosa,
            obj.pdf_ariza,
            obj.pdf_muqova,
            obj.pdf_mijoz_anketasi,
            obj.pdf_majburiyatnoma,
        ]
        if all(files):
            return "✅ Barchasi bor"
        return "❌ Hujjat yetishmaydi"

        # Meta ichidagi alohida key'larni chiqarish

    def contract(self, obj):
        """Meta ichidagi 'key1' ni chiqarish"""
        application_id = obj.application_id

        contract_number = Application.objects.filter(id=application_id).first().meta.get('contract')['contract_number']
        contract_date = Application.objects.filter(id=application_id).first().meta.get('contract')['contract_date']
        contract = f"{contract_date} yildagi {contract_number}-sonli shartnoma"
        return contract

    def customer(self, obj):
        """Meta ichidagi 'key1' ni chiqarish"""
        application_id = obj.application_id
        customer_fullname_initials = Application.objects.filter(id=application_id).first().meta.get('customer')['customer_fullname_initials']
        return customer_fullname_initials


    # Sarlavhalarni chiroyli qilish
    has_all_files.short_description = "Hujjatlar holati"
    contract.short_description = "contract"


@admin.register(XlsxTemplate)
class XlsxTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'status', 'created_by', 'created_at')
    list_filter = ('type', 'status')
    search_fields = ('title', 'type', 'status')
    ordering = ('-created_at',)
