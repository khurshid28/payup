from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from stepform.models import Organization, XlsxTemplate
import logging

logger = logging.getLogger('django')

def test_error(request):
    logger.error("🚨 Django ichki serverida xatolik chiqdi!")
    return HttpResponse("Xatolik sinovi!")

@login_required()
def home(request):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish
    organization = Organization.objects.first()
    excel_templates = XlsxTemplate.objects.all().order_by('-id')
    if organization:
        organization = organization
    else:
        organization = "Topilmadi"
    context = {
        'user_groups': user_groups,
        'organization': organization,
        'excel_templates': excel_templates
    }

    return render(request, 'pages/index.html', context)
