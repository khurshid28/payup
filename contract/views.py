from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from contract.models import Customer, Contract, Pledge, Report


@login_required(login_url='account_login')
def mikroqarz_form(request):
    return render(request, 'contract/mikroqarz_form.html')


@login_required(login_url='account_login')
def mikroqarz_list(request):
    report = Report.objects.all()
    context = {'report': report}
    return render(request, 'contract/mikroqarz_list.html', context)


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
            vehicle_loan_total=int(pledge_dict.get('pledge_loan_total').replace(" ", "")),
            vehicle_loan_total_word_uz=pledge_dict.get('pledge_loan_total_word_uz'),
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
            metadata=request.data
        )
        report.save()
        return Response(customer_dict, status=status.HTTP_201_CREATED)
