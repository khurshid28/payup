from django import forms
from .models import Report


class ModeratorForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['xlsx', 'moderator_signature']


class DirektorForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['direktor_signature']
