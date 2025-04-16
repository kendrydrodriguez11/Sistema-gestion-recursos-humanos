from django.forms import ModelForm
from apps.gestion_venta.models import Cliente

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = ['created_at', 'created_by', 'updated_at', 'update_by']