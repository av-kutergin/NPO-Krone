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
        fields = ['lastname', 'firstname', 'birthdate', 'phone', 'email', 'telegram']
        widgets = {
            'lastname': forms.TextInput(attrs={'style': {'grid-column': '1 / 1;', 'grid-row': '2 / 2;'}}),
            'firstname': forms.TextInput(attrs={'style': {'grid-column': '2 / 2;', 'grid-row': '2 / 2;'}}),
            'birthdate': forms.DateInput(attrs={'style': {'grid-column': '1 / 1;', 'grid-row': '4 / 4;'}}),
            'phone': forms.TextInput(attrs={'style': 'grid-column: 2 / 2; grid-row: 3 / 3;'}),
            'email': forms.EmailInput(attrs={'style': 'grid-column: 2 / 2; grid-row: 3 / 3;'}),
            'telegram': forms.TextInput(attrs={'style': 'grid-column: 2 / 2; grid-row: 6 / 6;'}),
        }

