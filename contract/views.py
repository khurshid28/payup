import os
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from openpyxl.reader.excel import load_workbook
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from contract.forms import ModeratorForm, DirektorForm
from contract.models import Customer, Contract, Pledge, Report3View, Report, Document, Report3, ViewReport3Document, \
    Organization
from gen_doc.models import DocxTemplate, GeneratedDocPdfModel
from gen_doc.views import GenDocument
from payup import settings
from payup.settings import BASE_DIR


# Mikroqarz
@login_required(login_url='account_login')
def mikroqarz_form(request):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish
    context = {
        'user_groups': user_groups
    }
    return render(request, 'contract/mikroqarz_form.html', context)


@login_required(login_url='account_login')
def mikroqarz_detail(request, pk):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish

    obj = get_object_or_404(ViewReport3Document, pk=pk)
    print(obj.meta)
    context = {
        'user_groups': user_groups,
        'obj': obj,
    }
    return render(request, 'contract/mikroqarz_detail.html', context)


# Mikrokredit
@login_required(login_url='account_login')
def mikrokredit_form(request):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish
    context = {
        'user_groups': user_groups
    }
    return render(request, 'contract/mikrokredit_form.html', context)


@login_required(login_url='account_login')
def mikrokredit_detail(request, pk):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish

    obj = get_object_or_404(Report3View, pk=pk)

    context = {
        'user_groups': user_groups,
        'obj': obj,
    }
    return render(request, 'contract/mikroqarz_detail.html', context)

# Mikroqqarz Moderator
@login_required(login_url='account_login')
def moderator_list(request, pk=None):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish
    reports = ViewReport3Document.objects.all().order_by('-id')
    context = {
        'user_groups': user_groups,
        'reports': reports,

    }
    return render(request, 'contract/moderator_list.html', context)


@login_required(login_url='account_login')
def moderator_form(request, pk):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish

    document = get_object_or_404(Document, pk=pk)
    credit_type = document.meta['contract']['credit_type']

    file_url = None

    if request.method == 'POST' and request.FILES.get('xlsx'):
        uploaded_file = request.FILES['xlsx']
        print(uploaded_file)

        # Fayl kengaytmasini olish
        ext = uploaded_file.name.split('.')[-1]
        new_filename = f"{credit_type}_{document.id}_excel.{ext}"  # Yangi UUID nom yaratish

        # Faylni `media/uploads/` ichiga saqlash
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads/xlsx/', new_filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Katalog yaratish

        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Faylga URL yaratish
        file_url = f"uploads/xlsx/{new_filename}"
        report = Report3.objects.get(document_id=document.id)
        report.xlsx = file_url

        # Moderator imzo qo'yishi
        report.moderator_signature = True
        report.save()
        return redirect('moderator_list')  # Bajarilgandan keyin boshqa sahifaga o'tish

    context = {
        'user_groups': user_groups,
        'obj': document,
        'file_url': file_url
    }
    return render(request, 'contract/moderator_form.html', context)


@login_required(login_url='account_login')
def direktor_list(request):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish

    reports = ViewReport3Document.objects.all().order_by('-id')

    context = {
        'user_groups': user_groups,
        'reports': reports,

    }

    return render(request, 'contract/direktor_list.html', context)


@login_required(login_url='account_login')
def direktor_form(request, document_id):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish
    report = Report3.objects.get(document_id=document_id)
    document = Document.objects.get(id=document_id)
    credit_type = document.meta['contract']['credit_type']
    docx_template = DocxTemplate.objects.get(product_type=credit_type)
    filename = f"{credit_type}_{document_id}"
    generated_document_doc_pdf = GeneratedDocPdfModel()

    if request.method == 'POST':
        report.direktor_signature = True
        generate_doc = GenDocument(
            generated_document_doc_pdf=generated_document_doc_pdf,
            filename=filename,
            shartnoma=docx_template.shartnoma,
            buyruq=docx_template.buyruq,
            dalolatnoma=docx_template.dalolatnoma,
            grafik=docx_template.grafik,
            context=document.meta,
            report_obj=report
        )
        # Documentlarni generatsiya qilish
        generate_doc.gen_qrcode()
        generate_doc.gen_shartnoma()
        generate_doc.gen_buyruq()
        generate_doc.gen_dalolatnoma()
        generate_doc.gen_grafik()
        # Reportga generatsiya qilingan document_id saqlash
        report.generated_doc_id = generated_document_doc_pdf.id
        report.save()

        return redirect('direktor_list')

    context = {
        'user_groups': user_groups,
    }
    return render(request, 'contract/direktor_form.html', context)





@login_required(login_url='account_login')
def document_list(request):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish

    reports = ViewReport3Document.objects.all().order_by('-id')
    print(reports)
    context = {
        'user_groups': user_groups,
        'reports': reports,

    }
    return render(request, 'contract/document_list.html', context)

def document_detail(request, unique_identifier):
    org = Organization.objects.get(id=1)
    report = get_object_or_404(Report3, unique_identifier=unique_identifier)
    document = Document.objects.get(id=report.document_id)
    generated_doc_pdf = GeneratedDocPdfModel.objects.get(id=report.generated_doc_id)
    context = {
        'report': report,
        'org': org,
        'document': document,
        'generated_doc_pdf': generated_doc_pdf,
    }
    return render(request, 'contract/document_detail.html', context)


# Oldingi kod buni keyin o'chiriib yuborish kerak

class CreateContract(APIView):
    def post(self, request, format=None):
        # Contractni saqlash
        contract_dict = request.data.get('contract')
        contract = Contract(
            contract_number=contract_dict.get('contract_number'),
            contract_date=contract_dict.get('contract_date'),
            credit_loan_total=int(contract_dict.get('credit_loan_total').replace(" ", "")),
            credit_start_date=datetime.strptime(contract_dict.get('credit_start_date'), '%d.%m.%Y'),
            credit_end_date=datetime.strptime(contract_dict.get('credit_end_date'), '%d.%m.%Y'),
            credit_percent=contract_dict.get('credit_percent'),
            credit_term=contract_dict.get('credit_term'),
            credit_loan_total_word_uz=contract_dict.get('credit_loan_total_word_uz'),
            credit_percent_word_uz=contract_dict.get('credit_percent_word_uz'),
            credit_term_word_uz=contract_dict.get('credit_term_word_uz'),
            credit_graphic_type=contract_dict.get('credit_graphic_type'),
            credit_type=contract_dict.get('credit_type')
        )
        contract.save()

        # Customerni saqlash
        customer_dict = request.data.get('customer')
        customer = Customer(
            first_name="",
            last_name="",
            document=customer_dict.get('customer_document'),
            issuedby=customer_dict.get('customer_issuedBy'),
            startdate=customer_dict.get('customer_startDate'),
            address=customer_dict.get('customer_address'),
            phone1=customer_dict.get('customer_phone1'),
            phone2=customer_dict.get('customer_phone2'),
            passport_series=customer_dict.get('customer_passport_series'),
            passport_number=customer_dict.get('customer_passport_number'),
            birth_date=customer_dict.get('customer_birthDate'),
            pinfl=customer_dict.get('customer_passport_pinfl'),
            fullname=customer_dict.get('customer_fullname'),
            fullname_initials=customer_dict.get('customer_fullname_initials')
        )
        customer.save()

        # Pledge saqlash
        pledge_dict = request.data.get('pledge')
        print(pledge_dict)

        pledge = Pledge(
            pledge_is_owner=pledge_dict.get('pledge_is_owner'),
            vehicle_model_name=pledge_dict.get('pledge_modelName'),
            vehicle_color=pledge_dict.get('pledge_vehicleColor'),
            vehicle_issue_year=pledge_dict.get('pledge_issueYear'),
            vehicle_engine_number=pledge_dict.get('pledge_engineNumber'),
            vehicle_shassi=pledge_dict.get('pledge_shassi'),
            vehicle_type=pledge_dict.get('pledge_vehicleTypeStr'),
            vehicle_body_number=pledge_dict.get('pledge_bodyNumber'),
            vehicle_gov_number=pledge_dict.get('pledge_govNumber'),
            vehicle_owner=pledge_dict.get('pledge_owner'),
            pledge_loan_total=int(pledge_dict.get('pledge_loan_total').replace(" ", "")),
            pledge_loan_total_word_uz=pledge_dict.get('pledge_loan_total_word_uz'),
            vehicle_tp_series=pledge_dict.get('pledge_vehicle_TP_series'),
            vehicle_tp_number=pledge_dict.get('pledge_vehicle_TP_number'),

        )
        pledge.save()

        # Owner saqlash

        owner_dict = request.data.get('owner_data')

        owner = Customer(
            first_name="",
            last_name="",
            document=owner_dict.get('owner_document'),
            issuedby=owner_dict.get('owner_issuedBy'),
            startdate=owner_dict.get('owner_startDate'),
            address=owner_dict.get('owner_address'),
            phone1=owner_dict.get('customer_phone1'),
            phone2=owner_dict.get('customer_phone2'),
            passport_series=owner_dict.get('owner_passport_series'),
            passport_number=owner_dict.get('owner_passport_number'),
            birth_date=owner_dict.get('owner_birthDate'),
            pinfl=owner_dict.get('owner_passport_pinfl'),
            fullname=owner_dict.get('owner_fullname'),
            fullname_initials=owner_dict.get('owner_fullname_initials')
        )
        owner.save()
        print(owner.id)

        report = Report(
            created_by=request.data['config']['created_by'],
            updated_by=None,
            contract_id=contract.id,
            customer_id=customer.id,
            organization_id=1,
            pledge_id=pledge.id,
            branch_id=1,
            owner_data_id=owner.id,
            state=1,
            operator_signature=False,
            moderator_signature=False,
            direktor_signature=False,
            # metadata=request.data
        )
        report.save()
        return Response(customer_dict, status=status.HTTP_201_CREATED)


# Create Document
class CreateContractDoc(APIView):
    def post(self, request, format=None):
        print(request.data)
        metadata_dict = request.data
        document = Document(
            meta=metadata_dict,
            state=True
        )
        document.save()
        report = Report3(
            created_by=request.data['config']['created_by'],
            document_id=document.id,
            state=True
        )
        report.save()
        return Response("document", status=status.HTTP_201_CREATED)
