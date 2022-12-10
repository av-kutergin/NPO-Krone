import datetime

from django import forms
from django.core.exceptions import ValidationError

from projects.models import Guest

from django.utils.translation import gettext_lazy as _


class AddGuestForm(forms.ModelForm):

    class Meta:
        model = Guest
        fields = ['firstname', 'lastname',  'phone', 'telegram', 'email', 'birthdate']
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-form-item__input'}),
            'lastname': forms.TextInput(attrs={'class': 'form-item__input'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-item__input'}),
            'phone': forms.TextInput(attrs={'class': 'form-item__input'}),
            'email': forms.EmailInput(attrs={'class': 'form-item__input'}),
            'telegram': forms.TextInput(attrs={'class': 'form-item__input'}),
        }
        labels = {
            'firstname': _('Имя'),
            'lastname': _('Фамилия'),
            'phone': _('Телефон'),
            'telegram': _('Телеграм'),
            'email': _('Электронная почта'),
            'birthdate': _('Дата рождения'),
        }
