from django import forms
from django.forms import ModelForm
from apps.gestion_venta.models import Factura
from apps.security.models import Menu

class FacturaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subtotal'].widget.attrs.update({
            'readonly': 'readonly',
        })
        self.fields['total'].widget.attrs.update({
            'readonly': 'readonly',
        })
    class Meta:
        model = Factura
        fields = '__all__'