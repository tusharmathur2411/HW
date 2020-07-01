from django.forms import ModelForm, Textarea, DateInput, DateField
from .models import Patient, PatientAddress


class PatientForm(ModelForm):
    birthday = DateField(widget=DateInput(format = '%d/%m/%Y'),
                                 input_formats=('%d/%m/%Y',))

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'birthday', 'gender']


class PatientAddressForm(ModelForm):
    class Meta:
        model = PatientAddress
        fields = ['line_one', 'line_two', 'primary_phone_no', 'alternate_phone_no', 'city']
        widgets = {
            'line_one': Textarea(attrs={'cols': 50, 'rows': 1}),
            'line_two': Textarea(attrs={'cols': 50, 'rows': 1}),
        }
