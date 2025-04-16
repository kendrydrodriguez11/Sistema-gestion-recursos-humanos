from django.forms import ModelForm
from apps.core.models import Organization

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'