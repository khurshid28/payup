from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from contract.models import Document


@login_required()
def home(request):
    user = request.user
    user_groups = user.groups.all()  # Foydalanuvchi guruhlarini olish

    context = {
        'user_groups': user_groups
    }

    return render(request, 'pages/index.html', context)
