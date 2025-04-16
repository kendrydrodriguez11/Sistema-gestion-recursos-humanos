from django.forms import ModelForm
from apps.gestion_venta.models import Producto

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        exclude = ['created_at', 'created_by', 'updated_at', 'update_by']