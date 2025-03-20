from django.contrib.auth.models import User
from django.db import models
from openpyxl.styles.builtins import percent


class ContractStep(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    contract_number = models.CharField(max_length=500, unique=True, blank=True, null=True)
    contract_date = models.DateField(blank=True, null=True)
    credit_start_date = models.DateField(blank=True, null=True)
    credit_end_date = models.DateField(blank=True, null=True)
    credit_loan_total = models.IntegerField(blank=True, null=True)
    credit_loan_total_word_uz = models.CharField(max_length=1024, blank=True, null=True)
    credit_percent = models.IntegerField(blank=True, null=True)
    credit_percent_word_uz = models.CharField(max_length=1024, blank=True, null=True)
    credit_term = models.PositiveIntegerField(help_text="Muddat oyda", blank=True, null=True)
    credit_term_word_uz = models.CharField(max_length=1024, blank=True, null=True)
    credit_type = models.CharField(max_length=512)
    credit_graphic_type = models.CharField(max_length=512)
    insurance_premium = models.IntegerField(blank=True, null=True)
    insurance_premium_word_uz = models.CharField(max_length=512)

    def __str__(self):
        return self.contract_number

    class Meta:
        db_table = 'contract'
        managed = False


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    customer_passport_series = models.CharField(max_length=5, blank=True, null=True)  # Pasport seriyasi (AA, AB, AC...)
    customer_passport_number = models.CharField(max_length=10, blank=True, null=True)  # Pasport raqami
    customer_passport_pinfl = models.CharField(max_length=14, blank=True, null=True)  # PINFL (14 xonali)
    customer_birthDate = models.DateField()  # Tug‘ilgan sana
    customer_document = models.CharField(max_length=255, blank=True, null=True)  # Hujjat fayli
    customer_fullname = models.CharField(max_length=512, blank=True, null=True)  # To‘liq ism
    customer_fullname_initials = models.CharField(max_length=512, blank=True, null=True)  # Ism-sharif initsiallari
    customer_issuedBy = models.CharField(max_length=1024, blank=True, null=True)  # Kim tomonidan berilgan
    customer_startDate = models.DateField(blank=True, null=True)  # Pasport berilgan sana
    customer_endDate = models.DateField(blank=True, null=True)  # Pasport amal qilish muddati sana
    customer_address = models.TextField(blank=True, null=True)  # Mijozning manzili
    customer_phone1 = models.CharField(max_length=255, blank=True, null=True)  # Asosiy telefon raqami
    customer_phone2 = models.CharField(max_length=255, blank=True, null=True)  # Qo‘shimcha telefon
    customer_phone3 = models.CharField(max_length=255, blank=True, null=True)  # Qo‘shimcha telefon
    customer_average_monthly_income = models.IntegerField(blank=True, null=True)  # Mijozning o‘rtacha oylik daromadi
    customer_average_monthly_income_word = models.CharField(max_length=1024, blank=True,
                                                            null=True)  # Mijozning o‘rtacha oylik daromadi
    customer_average_monthly_expenses = models.IntegerField(blank=True, null=True)  # O‘rtacha oylik xarajatlari
    customer_average_monthly_expenses_word = models.CharField(max_length=1024, blank=True,
                                                              null=True)  # O‘rtacha oylik xarajatlari
    customer_position = models.CharField(max_length=1024, blank=True, null=True)  # O‘rtacha oylik xarajatlari
    customer_first_principal_payment = models.IntegerField(blank=True, null=True)  # Birinchi oy uchun toʻlov
    customer_first_principal_payment_word = models.CharField(max_length=1024, blank=True,
                                                             null=True)  # Birinchi oy uchun toʻlov

    def __str__(self):
        return self.customer_fullname

    class Meta:
        db_table = 'customer'
        managed = False


class Pledge(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    pledge_is_owner = models.CharField(max_length=255, blank=True, null=True)  # Garovga qo‘ygan shaxs egami yoki yo‘q
    pledge_vehicle_TP_series = models.CharField(max_length=255, blank=True, null=True)  # Texnik pasport seriyasi
    pledge_vehicle_TP_number = models.CharField(max_length=255, blank=True, null=True)  # Texnik pasport raqami
    pledge_vehicle_techPassportIssueDate = models.DateField(blank=True, null=True)  # Texnik pasport berilgan sana
    pledge_vehicleColor = models.CharField(max_length=255, blank=True, null=True)  # Avtomobil rangi
    pledge_issueYear = models.PositiveIntegerField(blank=True, null=True)  # Ishlab chiqarilgan yil
    pledge_engineNumber = models.CharField(max_length=255, blank=True, null=True)  # Dvigatel raqami
    pledge_shassi = models.CharField(max_length=255, blank=True, null=True)  # Shassi raqami
    pledge_vehicleTypeStr = models.CharField(max_length=255, blank=True, null=True)  # Avtomobil turi
    pledge_bodyNumber = models.CharField(max_length=255, blank=True, null=True)  # Kuzov raqami
    pledge_govNumber = models.CharField(max_length=255, blank=True, null=True)  # Davlat raqami (YTH 01)
    pledge_modelName = models.CharField(max_length=255, blank=True, null=True)  # Avtomobil modeli
    pledge_owner = models.CharField(max_length=1024, blank=True, null=True)  # Avtomobil egasi

    pledge_loan_total = models.IntegerField(blank=True, null=True)  # Garov qiymati
    pledge_loan_total_word_uz = models.CharField(max_length=1024)  # Garov summasi so‘z bilan
    pledge_division = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.pledge_modelName} - {self.pledge_govNumber} ({self.pledge_loan_total} UZS)"

    class Meta:
        db_table = 'pledge'
        managed = False


class Organization(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=255, blank=True, null=True)  # Tashkilot nomi
    address = models.CharField(max_length=255, blank=True, null=True)  # Tashkilot manzili
    account_number = models.CharField(max_length=50, blank=True, null=True)  # Hisob raqami
    mfo = models.CharField(max_length=10, blank=True, null=True)  # Bank MFO kodi
    stir = models.CharField(max_length=15, blank=True, null=True)  # Soliq identifikatsiya raqami (STIR)

    phone1 = models.CharField(max_length=20, blank=True, null=True)  # 1-telefon raqami
    phone2 = models.CharField(max_length=20, blank=True, null=True)  # 2-telefon raqami
    direktor_fullname = models.CharField(max_length=512, blank=True, null=True)  # Direktor FIO
    direktor_initials = models.CharField(max_length=512, blank=True, null=True)  # Direktor  initials
    loan_head_fullname = models.CharField(max_length=512, blank=True, null=True)  # Kreditlash FIO
    loan_head_initials = models.CharField(max_length=512, blank=True, null=True)  # Kreditlash  initials
    monitoring_head_fullname = models.CharField(max_length=512, blank=True, null=True)  # Monitoring FIO
    monitoring_head_initials = models.CharField(max_length=512, blank=True, null=True)  # Monitoring initials

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'organization'  # Jadval nomini PostgreSQLda 'organization' qilib saqlaydi
        managed = False


class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024, blank=True, null=True)
    head_fullname = models.CharField(max_length=1024, blank=True, null=True)  # Markaz rahbari FIO
    head_initials_uz = models.CharField(max_length=1024, blank=True, null=True)  # Markaz rahbari initials
    state = models.BooleanField(default=True)
    position = models.CharField(max_length=1024, blank=True, null=True)  # Lavozimi

    def __str__(self):
        return f"Application {self.head_initials_uz} "

    class Meta:
        db_table = 'branch'
        managed = False


class Application(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    contract_id = models.IntegerField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    owner_id = models.IntegerField(blank=True, null=True)
    pledge_id = models.IntegerField(blank=True, null=True)
    branch_id = models.IntegerField(blank=True, null=True)
    organization_id = models.IntegerField(blank=True, null=True)
    state = models.BooleanField(default=True)
    meta = models.JSONField(blank=True, null=True, default=dict)
    operator_signature = models.BooleanField(default=False)
    moderator_signature = models.BooleanField(default=False)
    direktor_signature = models.BooleanField(default=False)
    loan_head_signature = models.BooleanField(default=False)
    monitoring_head_signature = models.BooleanField(default=False)
    xlsx = models.FileField(blank=True, null=True, upload_to='uploads/xlsx_template/')

    def __str__(self):
        return f"Application {self.id} - {self.state}"

    def sum_signatures(self):
        percent = 0
        if self.moderator_signature:
            percent = percent + 25
        if self.loan_head_signature:
            percent = percent + 25
        if self.monitoring_head_signature:
            percent = percent + 25
        if self.direktor_signature:
            percent = percent + 25
        return percent

    class Meta:
        db_table = 'application'
        managed = False


class DocxTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    product_type = models.CharField(max_length=500, blank=True, null=True)
    shartnoma = models.FileField(blank=True, null=True, upload_to='uploads/docx_templates/')
    buyruq = models.FileField(blank=True, null=True, upload_to='uploads/docx_templates/')
    dalolatnoma = models.FileField(blank=True, null=True, upload_to='uploads/docx_templates/')
    grafik = models.FileField(blank=True, null=True, upload_to='uploads/docx_templates/')
    bayonnoma = models.FileField(blank=True, null=True, upload_to='uploads/docx_templates/')
    # xulosa = models.FileField(blank=True, null=True, upload_to='uploads/docx_templates/') # Bu exceldan chiqadi

    shartnoma_ishonchnoma = models.FileField(blank=True, null=True, upload_to='uploads/docx_templates/')
    buyruq_ishonchnoma = models.FileField(blank=True, null=True, upload_to='uploads/docx_templates/')
    dalolatnoma_ishonchnoma = models.FileField(blank=True, null=True, upload_to='uploads/docx_templates/')
    grafik_ishonchnoma = models.FileField(blank=True, null=True, upload_to='uploads/docx_templates/')
    bayonnoma_ishonchnoma = models.FileField(blank=True, null=True, upload_to='uploads/docx_templates/')
    # xulosa_ishonchnoma = models.FileField(blank=True, null=True, upload_to='uploads/docx_templates/') # Bu exceldan chiqadi

    state = models.BooleanField(default=True)

    def __str__(self):
        return f"DocxTemplate {self.id} - {self.product_type}"

    class Meta:
        db_table = 'docx_template'
        managed = False


class GeneratedDocument(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    state = models.BooleanField(default=True)
    application_id = models.IntegerField(blank=True, null=True)

    pdf_shartnoma = models.FileField(blank=True, null=True, upload_to='uploads/generated/pdf/')
    pdf_buyruq = models.FileField(blank=True, null=True, upload_to='uploads/generated/pdf/')
    pdf_dalolatnoma = models.FileField(blank=True, null=True, upload_to='uploads/generated/pdf/')
    pdf_grafik = models.FileField(blank=True, null=True, upload_to='uploads/generated/pdf/')
    pdf_bayonnoma = models.FileField(blank=True, null=True, upload_to='uploads/generated/pdf/')
    pdf_xulosa = models.FileField(blank=True, null=True, upload_to='uploads/generated/pdf/')
    pdf_ariza = models.FileField(blank=True, null=True, upload_to='uploads/generated/pdf/')
    pdf_muqova = models.FileField(blank=True, null=True, upload_to='uploads/generated/pdf/')
    pdf_mijoz_anketasi = models.FileField(blank=True, null=True, upload_to='uploads/generated/pdf/')
    pdf_majburiyatnoma = models.FileField(blank=True, null=True, upload_to='uploads/generated/pdf/')

    def __str__(self):
        return f"GeneratedDocument {self.id}"

    class Meta:
        db_table = 'generated_document'
        managed = False


class XlsxTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    title = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=500, blank=True, null=True)
    file = models.FileField(blank=True, null=True, upload_to='uploads/docx_org_templates/excel_template/')
    description = models.CharField(max_length=1024, blank=True, null=True)
    status = models.BooleanField(default=True)


    def __str__(self):
        return f"XlsxTemplate {self.id}"

    class Meta:
        db_table = 'xlsx_template'
        managed = False