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
            'firstname': forms.TextInput(attrs={'placeholder': _('Имя')}),
            'lastname': forms.TextInput(attrs={'placeholder': _('Фамилия')}),
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'phone': forms.TextInput(attrs={'placeholder': _('+70000000000')}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@email.ru'}),
            'telegram': forms.TextInput(attrs={'placeholder': 'Telegram'}),
        }
        labels = {
            'firstname': _('Имя*'),
            'lastname': _('Фамилия*'),
            'phone': _('Телефон*'),
            'telegram': _('Телеграм'),
            'email': _('Электронная почта'),
            'birthdate': _('Дата рождения*'),
        }
