from datetime import datetime

from stepform.models import ContractStep, Customer, Pledge, Organization, Branch, Application


def form_save(request, contract_dict, customer_dict, pledge_dict):
    contract = ContractStep(
        created_by=request.user.id,
        contract_number=contract_dict.get('contract_number'),
        contract_date=datetime.strptime(contract_dict.get('contract_date'), '%d.%m.%Y'),
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

    customer = Customer(
        created_by=request.user.id,
        customer_document=customer_dict.get('customer_document'),
        customer_passport_pinfl=customer_dict.get('customer_passport_pinfl'),
        customer_birthDate=datetime.strptime(customer_dict.get('customer_birthDate'), '%d.%m.%Y'),
        customer_fullname=customer_dict.get('customer_fullname'),
        customer_address=customer_dict.get('customer_address'),
        customer_fullname_initials=customer_dict.get('customer_fullname_initials'),
        customer_issuedBy=customer_dict.get('customer_issuedBy'),
        customer_startDate=datetime.strptime(customer_dict.get('customer_startDate'), '%d.%m.%Y'),
        customer_phone1=customer_dict.get('customer_phone1'),
        customer_phone2=customer_dict.get('customer_phone2')
    )
    customer.save()

    pledge = Pledge(
        created_by=request.user.id,
        pledge_is_owner=pledge_dict.get('pledge_is_owner'),
        pledge_vehicle_TP_series=pledge_dict.get('pledge_vehicle_TP_series'),
        pledge_vehicle_TP_number=pledge_dict.get('pledge_vehicle_TP_number'),
        pledge_vehicle_techPassportIssueDate=datetime.strptime(pledge_dict.get('pledge_vehicle_techPassportIssueDate'),
                                                               '%d.%m.%Y'),
        pledge_govNumber=pledge_dict.get('pledge_govNumber'),
        pledge_modelName=pledge_dict.get('pledge_modelName'),
        pledge_issueYear=int(pledge_dict.get('pledge_issueYear')),
        pledge_vehicleColor=pledge_dict.get('pledge_vehicleColor'),
        pledge_shassi=pledge_dict.get('pledge_shassi'),
        pledge_vehicleTypeStr=pledge_dict.get('pledge_vehicleTypeStr'),
        pledge_engineNumber=pledge_dict.get('pledge_engineNumber'),
        pledge_bodyNumber=pledge_dict.get('pledge_bodyNumber'),
        pledge_owner=pledge_dict.get('pledge_owner'),
        pledge_loan_total=int(pledge_dict.get('pledge_loan_total').replace(" ", "")),
        pledge_loan_total_word_uz=pledge_dict.get('pledge_loan_total_word_uz')
    )
    pledge.save()

    if pledge_dict['pledge_is_owner'] == 'no':
        owner = Customer(
            created_by=request.user.id,
            customer_document=pledge_dict.get('owner_document'),
            customer_passport_pinfl=pledge_dict.get('owner_passport_pinfl'),
            customer_birthDate=datetime.strptime(pledge_dict.get('owner_birthDate'), '%d.%m.%Y'),
            customer_fullname=pledge_dict.get('owner_fullname'),
            customer_address=pledge_dict.get('owner_address'),
            customer_fullname_initials=pledge_dict.get('owner_fullname_initials'),
            customer_issuedBy=pledge_dict.get('owner_issuedBy'),
            customer_startDate=datetime.strptime(pledge_dict.get('owner_startDate'), '%d.%m.%Y'),
        )
        owner.save()
        owner_id = owner.id
    else:
        owner_id = None
    organization = Organization.objects.first()
    branch = Branch.objects.get(user=request.user)

    organization_dict = organization.__dict__
    del organization_dict["_state"]
    # del organization_dict["id"]
    print(organization_dict)

    branch_dict = branch.__dict__
    del branch_dict["_state"]
    del branch_dict["created_at"]
    del branch_dict["created_by"]
    del branch_dict["user_id"]
    print(branch_dict)

    application = Application(
        created_by=request.user.id,
        contract_id=contract.id,
        customer_id=customer.id,
        owner_id=owner_id,
        pledge_id=pledge.id,
        organization_id=organization.id,
        branch_id=branch.id,
        state=True,
        meta={
            "contract": contract_dict,
            "customer": customer_dict,
            "pledge": pledge_dict,
            "organization": organization_dict,
            "branch": branch_dict,
        }
    )
    application.save()
    return application
