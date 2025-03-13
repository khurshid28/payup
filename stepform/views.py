import os

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime

from payup import settings
from payup.asgi import application
from stepform.models import ContractStep, Customer, Pledge, Application, Branch, Organization, DocxTemplate, \
    GeneratedDocument
from stepform.utils import form_save
from gen_doc.views import GenDocument


def step_mikroqarz(request, pk):
    return redirect('step_contract')


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


def step_customer(request):
    if request.method == "POST":
        request.session["step_customer_data"] = request.POST
        return redirect("step_pledge")
    context = {
        "step": 2,
        "credit_type": request.session["step_contract_data"]["credit_type"],
    }
    return render(request, "stepform/step_customer_form.html", context)


def step_pledge(request):
    if request.method == "POST":
        request.session["step_pledge_data"] = request.POST
        return redirect("done")
    context = {
        "step": 3,
        "credit_type": request.session["step_contract_data"]["credit_type"],
    }
    return render(request, "stepform/step_pledge_form.html", context)


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
        new_filename = f"{credit_type}_{application.id}_excel.{ext}"  # Yangi UUID nom yaratish

        # Faylni `media/uploads/` ichiga saqlash
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads/xlsx/', new_filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Katalog yaratish

        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Faylga URL yaratish
        file_url = f"uploads/xlsx/{new_filename}"
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
    credit_type = application.meta['contract']['credit_type']
    pledge_is_owner = application.meta['pledge']['pledge_is_owner']
    docx_template = DocxTemplate.objects.filter(product_type=credit_type, state=True).first()
    generated_document = GeneratedDocument()
    filename = f"{credit_type}_{application.id}"

    if request.method == "POST":
        if pledge_is_owner == 'yes': # Garov egasi o'zi
            gen_doc = GenDocument(
                generated_document=generated_document,
                filename=filename,
                shartnoma=docx_template.shartnoma,
                buyruq=docx_template.buyruq,
                dalolatnoma=docx_template.dalolatnoma,
                grafik=docx_template.grafik,
                bayonnoma=docx_template.bayonnoma,
                # xulosa=docx_template.xulosa,
                context=application.meta,
                application=application
            )
            gen_doc.display_info()
            gen_doc.gen_shartnoma()
            gen_doc.gen_buyruq()
            gen_doc.gen_dalolatnoma()
            gen_doc.gen_grafik()
            gen_doc.gen_bayonnoma()
            gen_doc.gen_excel_to_pdf() # bu yerda Xulosa exceldan asosida yaratiladi
            gen_doc.remove_temp_files()

            Application.objects.filter(pk=pk).update(direktor_signature=True)
        elif pledge_is_owner == 'no': # Garov egasi boshqa
            gen_doc = GenDocument(
                generated_document=generated_document,
                filename=filename,
                shartnoma=docx_template.shartnoma_ishonchnoma,
                buyruq=docx_template.buyruq_ishonchnoma,
                dalolatnoma=docx_template.dalolatnoma_ishonchnoma,
                grafik=docx_template.grafik_ishonchnoma,
                bayonnoma=docx_template.bayonnoma_ishonchnoma,
                xulosa=docx_template.xulosa_ishonchnoma,
                context=application.meta,
                application=application
            )
            # gen_doc.display_info()
            gen_doc.gen_shartnoma()
            gen_doc.gen_buyruq()
            gen_doc.gen_dalolatnoma()
            gen_doc.gen_grafik()
            gen_doc.gen_bayonnoma()
            gen_doc.gen_xulosa()
            gen_doc.remove_temp_files()

            Application.objects.filter(pk=pk).update(direktor_signature=True)

        return redirect('direktor_list')
    context = {
        'user_groups': user_groups,
        'application': application
    }
    return render(request, 'stepform/direktor_form.html', context)
