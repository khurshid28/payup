import uuid

from django.db import models
from rest_framework.fields import JSONField


# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=1024)
    last_name = models.CharField(max_length=1024)
    document = models.CharField(max_length=1024)
    issuedby = models.CharField(max_length=1024)
    startdate = models.CharField(max_length=1024)
    address = models.CharField(max_length=1024)
    phone1 = models.CharField(max_length=1024)
    phone2 = models.CharField(max_length=1024)
    passport_series = models.CharField(max_length=1024)
    passport_number = models.CharField(max_length=1024)
    birth_date = models.CharField(max_length=1024)
    pinfl = models.CharField(max_length=1024)
    fullname = models.CharField(max_length=1024)
    fullname_initials = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'customer'

    def __str__(self):
        return self.fullname


class Contract(models.Model):
    id = models.AutoField(primary_key=True)
    contract_number = models.CharField(max_length=1024)
    contract_date = models.CharField(max_length=1024)
    credit_loan_total = models.DecimalField(max_digits=10, decimal_places=2)
    credit_start_date = models.DateField()
    credit_end_date = models.DateField()
    credit_percent = models.IntegerField()
    credit_term = models.IntegerField()
    credit_loan_total_word_uz = models.CharField(max_length=1024)
    credit_percent_word_uz = models.CharField(max_length=1024)
    credit_term_word_uz = models.CharField(max_length=1024)
    credit_graphic_type = models.CharField(max_length=1024)
    credit_graphic_meta = models.JSONField(default=dict)
    credit_type = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'contract'

    def __str__(self):
        return self.contract_number


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1024)
    address = models.CharField(max_length=1024)
    account_number = models.CharField(max_length=1024)
    mfo = models.CharField(max_length=1024)
    stir = models.CharField(max_length=1024)
    phone1 = models.CharField(max_length=1024)
    phone2 = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'organization'

    def __str__(self):
        return self.title


class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1024)
    head_initials_uz = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'branch'

    def __str__(self):
        return self.title


class Pledge(models.Model):
    id = models.AutoField(primary_key=True)
    pledge_is_owner = models.CharField(max_length=1024)
    vehicle_model_name = models.CharField(max_length=1024)
    vehicle_color = models.CharField(max_length=1024)
    vehicle_issue_year = models.IntegerField()
    vehicle_engine_number = models.CharField(max_length=1024)
    vehicle_shassi = models.CharField(max_length=1024)
    vehicle_type = models.CharField(max_length=1024)
    vehicle_body_number = models.CharField(max_length=1024)
    vehicle_gov_number = models.CharField(max_length=1024)
    vehicle_owner = models.CharField(max_length=1024)
    pledge_loan_total = models.IntegerField()
    pledge_loan_total_word_uz = models.CharField(max_length=1024)
    vehicle_tp_series = models.CharField(max_length=1024)
    vehicle_tp_number = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'pledge'

    def __str__(self):
        return self.vehicle_model_name


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contract_id = models.IntegerField()
    customer_id = models.IntegerField()
    organization_id = models.IntegerField()
    pledge_id = models.IntegerField()
    branch_id = models.IntegerField()
    owner_data_id = models.IntegerField()
    state = models.IntegerField()
    operator_signature = models.BooleanField(default=False)
    moderator_signature = models.BooleanField(default=False)
    direktor_signature = models.BooleanField(default=False, blank=False)
    # metadata = models.JSONField(default=dict)
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    xlsx = models.FileField(upload_to='uploads/')
    generated_doc_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'report2'

    def __str__(self):
        return str(self.id)


class Report3View(models.Model):
    id = models.AutoField(primary_key=True)
    contract_id = models.IntegerField()
    customer_id = models.IntegerField()
    pledge_id = models.IntegerField()
    owner_data_id = models.IntegerField()
    generated_doc_id = models.IntegerField()  # Generated doc id
    state = models.IntegerField()
    operator_signature = models.BooleanField(default=False)
    moderator_signature = models.BooleanField(default=False)
    direktor_signature = models.BooleanField(default=False)
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False)

    contract_number = models.CharField(max_length=1024)
    contract_date = models.CharField(max_length=1024)
    credit_loan_total = models.DecimalField(max_digits=10, decimal_places=2)
    credit_loan_total_word_uz = models.CharField(max_length=1024)
    credit_start_date = models.DateField()
    credit_end_date = models.DateField()
    credit_percent = models.IntegerField()
    credit_percent_word_uz = models.CharField(max_length=1024)
    credit_term = models.IntegerField()
    credit_term_word_uz = models.CharField(max_length=1024)
    credit_graphic_type = models.CharField(max_length=1024)
    credit_type = models.CharField(max_length=1024)

    customer_document = models.CharField(max_length=1024)
    customer_issuedby = models.CharField(max_length=1024)
    customer_startdate = models.CharField(max_length=1024)
    customer_address = models.CharField(max_length=1024)
    customer_phone1 = models.CharField(max_length=1024)
    customer_phone2 = models.CharField(max_length=1024)
    customer_passport_series = models.CharField(max_length=1024)
    customer_passport_number = models.CharField(max_length=1024)
    customer_birth_date = models.CharField(max_length=1024)
    customer_pinfl = models.CharField(max_length=1024)
    customer_fullname = models.CharField(max_length=1024)
    customer_fullname_initials = models.CharField(max_length=1024)

    organization_title = models.CharField(max_length=1024)
    organization_address = models.CharField(max_length=1024)
    organization_account_number = models.CharField(max_length=1024)
    organization_mfo = models.CharField(max_length=1024)
    organization_stir = models.CharField(max_length=1024)
    organization_phone1 = models.CharField(max_length=1024)
    organization_phone2 = models.CharField(max_length=1024)

    pledge_modelname = models.CharField(max_length=1024)
    pledge_vehiclecolor = models.CharField(max_length=1024)
    pledge_issueyear = models.CharField(max_length=1024)
    pledge_enginenumber = models.CharField(max_length=1024)
    pledge_shassi = models.CharField(max_length=1024)
    pledge_vehicletypestr = models.CharField(max_length=1024)
    pledge_bodynumber = models.CharField(max_length=1024)
    pledge_govnumber = models.CharField(max_length=1024)
    pledge_owner = models.CharField(max_length=1024)
    pledge_loan_total = models.DecimalField(max_digits=10, decimal_places=2)
    pledge_loan_total_word_uz = models.CharField(max_length=1024)
    pledge_is_owner = models.CharField(max_length=1024)
    pledge_vehicle_tp_series = models.CharField(max_length=1024)
    pledge_vehicle_tp_number = models.CharField(max_length=1024)
    branch_name_uz = models.CharField(max_length=1024)
    head_initials_uz = models.CharField(max_length=1024)
    owner_document = models.CharField(max_length=1024)
    owner_issuedby = models.CharField(max_length=1024)
    owner_startdate = models.CharField(max_length=1024)
    owner_address = models.CharField(max_length=1024)
    owner_passport_series = models.CharField(max_length=1024)
    owner_passport_number = models.CharField(max_length=1024)
    owner_birthdate = models.CharField(max_length=1024)
    owner_passport_pinfl = models.CharField(max_length=1024)
    owner_fullname = models.CharField(max_length=1024)
    owner_fullname_initials = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'view_report_4'

    def __str__(self):
        return str(self.id)


# TEST uchun
class Document(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(default=dict)
    state = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'document'

    def __str__(self):
        return str(self.id)


class Report3(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    document_id = models.IntegerField()
    generated_doc_id = models.IntegerField()
    state = models.BooleanField(default=False)
    operator_signature = models.BooleanField(default=False)
    moderator_signature = models.BooleanField(default=False)
    direktor_signature = models.BooleanField(default=False, blank=False)
    unique_identifier = models.CharField(default=uuid.uuid4, editable=False)
    xlsx = models.FileField(upload_to='uploads/')

    class Meta:
        managed = False
        db_table = 'report3'

    def __str__(self):
        return str(self.id)


class ViewReport3Document(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    document_id = models.IntegerField()
    meta = models.JSONField(default=dict)
    generated_doc_id = models.IntegerField()
    state = models.BooleanField(default=False)
    operator_signature = models.BooleanField(default=False)
    moderator_signature = models.BooleanField(default=False)
    direktor_signature = models.BooleanField(default=False)
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    xlsx = models.FileField(upload_to='uploads/')
    filename = models.CharField(max_length=1024)
    shartnoma_pdf = models.FileField()
    buyruq_pdf = models.FileField()
    dalolatnoma_pdf = models.FileField()
    grafik_pdf = models.FileField()

    class Meta:
        managed = False
        db_table = 'view_report3_document'

    def __str__(self):
        return str(self.id)
