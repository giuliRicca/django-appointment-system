from django import forms
from django.forms import ModelForm, Form
from django.utils import timezone
from appointments.models import Appointment, Service

class AppointmentForm(ModelForm):
    date = forms.DateField(initial=timezone.now().date(), widget=forms.DateInput(
        attrs={
        'class': 'disabledInput'
    }
    ))
    time = forms.TimeField(widget=forms.TimeInput(attrs={
        'class': 'disabledInput'
    }))
    length = forms.IntegerField(min_value=15, max_value=90, 
    label="Length: (min)",
    widget=forms.NumberInput(attrs={
        'step': '15',
        'value': '30'
    }))


    notes = forms.CharField(max_length=400, label="Notes: (optional)", widget=forms.Textarea(
    ), required=False)


    class Meta:
        model = Appointment
        fields = ['date','time','service','length','notes']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AppointmentForm, self).__init__(*args, **kwargs)
        if not user: return
        self.fields['service'].queryset = Service.objects.filter(user=user)

class ServiceForm(ModelForm):

    class Meta:
        model = Service
        fields = ['name']
    