from django import forms
from django.forms import ModelForm
from apps.payment_role.models import Overtime
from apps.security.models import Menu

class OvertimeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value_hour'].widget.attrs.update({
            'readonly': 'readonly',
        })
        self.fields['sucursal'].widget.attrs.update({
            'readonly': 'readonly',
        })
        self.fields['total'].widget.attrs.update({
            'readonly': 'readonly',
        })
    class Meta:
        model = Overtime
        fields = '__all__'
    
    