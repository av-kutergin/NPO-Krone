from django import forms
from projects.models import Guest


class AddGuestForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['lastname'].widget.attrs.update({'style': 'grid-column: 1 / 1; grid-row: 2 / 2;'})
    #     self.fields['firstname'].widget.attrs.update({'style': 'grid-column: 2 / 2; grid-row: 2 / 2;'})
    #     self.fields['phone'].widget.attrs.update({'style': 'grid-column: 1 / 1; grid-row: 4 / 4;'})
    #     self.fields['telegram'].widget.attrs.update({'style': 'grid-column: 2 / 2; grid-row: 3 / 3;'})
    #     self.fields['birthdate'].widget.attrs.update({'style': 'grid-column: 2 / 2; grid-row: 6 / 6;'})

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

