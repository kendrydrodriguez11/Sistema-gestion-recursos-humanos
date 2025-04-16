from django.forms import ModelForm
from apps.personal_training.models import Supplier

class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        exclude = ['created_at', 'created_by', 'updated_at', 'update_by']