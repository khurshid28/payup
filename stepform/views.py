import os
import threading
import time

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime

from gen_doc.excel_pdf_converter import ExcelToPDFConverter
from payup import settings
from payup.asgi import application
from stepform.models import ContractStep, Customer, Pledge, Application, Branch, Organization, DocxTemplate, \
    GeneratedDocument
from stepform.utils import form_save
from gen_doc.views import GenDocument
from django.contrib.auth.decorators import login_required

@login_required()
def step_mikroqarz(request, pk):
    return redirect('step_contract')

@login_required()
def step_contract(request, credit_type):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish

    if request.method == "POST":
        request.session["step_contract_data"] = request.POST
        return redirect("step_customer")
    context = {
        "step": 1,
        "credit_type": credit_type,
        "user_groups": user_groups
    }
    return render(request, "stepform/step_contract_form.html", context)

@login_required()
def step_customer(request):
    if request.method == "POST":
        request.session["step_customer_data"] = request.POST
        return redirect("step_pledge")
    context = {
        "step": 2,
        "credit_type": request.session["step_contract_data"]["credit_type"],
    }
    return render(request, "stepform/step_customer_form.html", context)

@login_required()
def step_pledge(request):
    if request.method == "POST":
        request.session["step_pledge_data"] = request.POST
        return redirect("done")
    context = {
        "step": 3,
        "credit_type": request.session["step_contract_data"]["credit_type"],
    }
    return render(request, "stepform/step_pledge_form.html", context)

@login_required()
def done(request):
    # Forma ma'lumotlarini dictga o'tkazish
    contract_dict = request.session["step_contract_data"]
    del contract_dict["csrfmiddlewaretoken"]
    customer_dict = request.session["step_customer_data"]
    del customer_dict["csrfmiddlewaretoken"]
    pledge_dict = request.session["step_pledge_data"]
    del pledge_dict["csrfmiddlewaretoken"]
    print(pledge_dict)
    application = form_save(request, contract_dict, customer_dict, pledge_dict)  # Application jadvaliga yozish
    return redirect("operator_list")


# Moderator
def operator_list(request, pk=None):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish
    applications = Application.objects.all().order_by('-id').filter(state=True)
    generated_documents = GeneratedDocument.objects.all().order_by('-id').filter(state=True)
    context = {
        'user_groups': user_groups,
        'applications': applications,
        'generated_documents': generated_documents,
    }
    return render(request, 'stepform/operator_list.html', context)


# Moderator
def moderator_list(request):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish
    applications = Application.objects.all().order_by('-id').filter(state=True)
    generated_documents = GeneratedDocument.objects.all().order_by('-id').filter(state=True)

    context = {
        'user_groups': user_groups,
        'applications': applications,
        'generated_documents': generated_documents,
    }
    return render(request, 'stepform/moderator_list.html', context)


def moderator_form(request, pk):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish

    application = get_object_or_404(Application, pk=pk)
    credit_type = application.meta['contract']['credit_type']

    file_url = None

    if request.method == 'POST' and request.FILES.get('xlsx'):
        uploaded_file = request.FILES['xlsx']
        print(uploaded_file)

        # Fayl kengaytmasini olish
        ext = uploaded_file.name.split('.')[-1]
        new_filename = f"{credit_type}_{application.id}.{ext}"  # Yangi UUID nom yaratish

        # Faylni `media/uploads/` ichiga saqlash
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads/xlsx_template/', new_filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Katalog yaratish

        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Faylga URL yaratish
        file_url = f"uploads/xlsx_template/{new_filename}"
        application.xlsx = file_url

        # Moderator imzo qo'yishi
        application.moderator_signature = True
        application.save()

        return redirect('moderator_list')  # Bajarilgandan keyin boshqa sahifaga o'tish
    context = {
        'user_groups': user_groups,
        'obj': application,
        'file_url': file_url
    }
    return render(request, 'stepform/moderator_form.html', context)


# KREDITLASH bo'limi
def loan_head_list(request):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish
    applications = Application.objects.all().order_by('-id').filter(state=True)
    generated_documents = GeneratedDocument.objects.all().order_by('-id').filter(state=True)

    context = {
        'user_groups': user_groups,
        'applications': applications,
        'generated_documents': generated_documents,
    }
    return render(request, 'stepform/loan_head_list.html', context)


def loan_head_form(request, pk):
    user = request.user
    user_groups = user.groups.all()
    application = get_object_or_404(Application, pk=pk)
    if request.method == "POST":
        application.loan_head_signature = True
        application.save()
        return redirect('loan_head_list')
    context = {
        'user_groups': user_groups,
        'application': application
    }
    return render(request, 'stepform/loan_head_form.html', context)

# MONITORING bo'limi
def monitoring_head_list(request):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish
    applications = Application.objects.all().order_by('-id').filter(state=True)
    generated_documents = GeneratedDocument.objects.all().order_by('-id').filter(state=True)

    context = {
        'user_groups': user_groups,
        'applications': applications,
        'generated_documents': generated_documents,
    }
    return render(request, 'stepform/monitoring_head_list.html', context)


def monitoring_head_form(request, pk):
    user = request.user
    user_groups = user.groups.all()
    application = get_object_or_404(Application, pk=pk)
    if request.method == "POST":
        application.monitoring_head_signature = True
        application.save()
        return redirect('monitoring_head_list')
    context = {
        'user_groups': user_groups,
        'application': application
    }
    return render(request, 'stepform/monitoring_head_form.html', context)


def direktor_list(request):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish

    applications = Application.objects.all().order_by('-id').filter(state=True)
    generated_documents = GeneratedDocument.objects.all().order_by('-id').filter(state=True)

    context = {
        'user_groups': user_groups,
        'applications': applications,
        'generated_documents': generated_documents,
    }

    return render(request, 'stepform/direktor_list.html', context)


# Direktor form
def direktor_form(request, pk):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish
    application = get_object_or_404(Application, pk=pk)
    xlsx_full_path = application.xlsx.path
    xlsx_filename_with_ext = os.path.basename(xlsx_full_path)
    # Fayl nomidan kengaytmani olib tashlash
    xlsx_filename = os.path.splitext(xlsx_filename_with_ext)[0]

    if request.method == "POST":
        filename = xlsx_filename  # Excel fayl nomi
        xlsx = application.xlsx  # Excel fayl nomi
        global_ip = settings.GLOBAL_IP  # O'zingizning IP yoki domain

        converter = ExcelToPDFConverter(filename=filename, xlsx=xlsx, global_ip=global_ip)

        # Excel ochiq bulsa uni yopamiz
        converter.force_kill_excel()

        # Fonda Generatsiya va tozalashni ketma-ket bajaradigan funksiya
        def background_task():
            converter.generate_multiple_pdfs_with_qr()
            converter.save_to_generated_document(application_id=application.id, user_id=request.user.id)
            converter.clear_generated_excel_files()
            converter.clear_generated_excel_files()
            converter.force_kill_excel()
        thread = threading.Thread(target=background_task)
        thread.start()

        pdf_paths = thread


        Application.objects.filter(pk=pk).update(direktor_signature=True)

        return render(request, 'stepform/converting_pdf.html')
    context = {
        'user_groups': user_groups,
        'application': application
    }
    return render(request, 'stepform/direktor_form.html', context)
