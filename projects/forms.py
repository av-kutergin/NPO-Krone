from django import forms
from projects.models import Guest

from django.utils.translation import gettext_lazy as _


class AddGuestForm(forms.ModelForm):

    class Meta:
        model = Guest
        fields = ['lastname', 'firstname', 'phone', 'telegram', 'email', 'birthdate']
        widgets = {
            'lastname': forms.TextInput(attrs={'class': 'element'}),
            'firstname': forms.TextInput(attrs={'class': 'element'}),
            'birthdate': forms.DateInput(attrs={'class': 'element'}),
            'phone': forms.TextInput(attrs={'class': 'element'}),
            'email': forms.EmailInput(attrs={'class': 'element'}),
            'telegram': forms.TextInput(attrs={'class': 'element'}),
        }
        labels = {
            'lastname': _('Фамилия'),
            'firstname': _('Имя'),
            'phone': _('Телефон'),
            'telegram': _('Телеграм'),
            'email': _('Электронная почта'),
            'birthdate': _('Дата рождения')
        }
