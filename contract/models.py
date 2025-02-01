import uuid

from django.db import models


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

    class Meta:
        managed = False
        db_table = 'contract'

    def __str__(self):
        return self.contract_number

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
    vehicle_loan_total = models.IntegerField()
    vehicle_loan_total_word_uz = models.CharField(max_length=1024)

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
    direktor_signature = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict)
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        managed = False
        db_table = 'report'

    def __str__(self):
        return str(self.contract_id)