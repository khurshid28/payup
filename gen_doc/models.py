from django.db import models

class GeneratedDocPdfModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    filename = models.CharField(max_length=1024)
    shartnoma_docx= models.FileField(upload_to='uploads/docx')
    buyruq_docx= models.FileField(upload_to='uploads/docx')
    dalolatnoma_docx= models.FileField(upload_to='uploads/docx')
    grafik_docx= models.FileField(upload_to='uploads/docx')
    shartnoma_pdf= models.FileField(upload_to='uploads/pdf')
    buyruq_pdf= models.FileField(upload_to='uploads/pdf')
    dalolatnoma_pdf= models.FileField(upload_to='uploads/pdf')
    grafik_pdf= models.FileField(upload_to='uploads/pdf')
    qrcode = models.FileField(upload_to='uploads/qrcode')

    class Meta:
        managed = False
        db_table = 'generated_doc_pdf'

    def __str__(self):
        return str(self.id)

class DocxTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    shartnoma =  models.FileField(upload_to='uploads/doc_templates')
    buyruq = models.FileField(upload_to='uploads/doc_templates')
    dalolatnoma =  models.FileField(upload_to='uploads/doc_templates')
    grafik = models.FileField(upload_to='uploads/doc_templates')
    product_type = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'docx_template'

    def __str__(self):
        return str(self.id)