from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from stepform.models import Organization


@login_required()
def home(request):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish
    organization = Organization.objects.first()
    if organization:
        organization = organization
    else:
        organization = "Topilmadi"
    context = {
        'user_groups': user_groups,
        'organization': organization,
    }

    return render(request, 'pages/index.html', context)
