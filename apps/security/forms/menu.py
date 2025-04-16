from django.forms import ModelForm
from apps.security.models import Menu

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'