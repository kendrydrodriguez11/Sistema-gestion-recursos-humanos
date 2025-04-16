from django.forms import ModelForm
from apps.gestion_venta.models import Categoria

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        exclude = ['created_at', 'created_by', 'updated_at', 'update_by']