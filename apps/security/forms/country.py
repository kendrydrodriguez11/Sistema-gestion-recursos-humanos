from django.forms import ModelForm

from apps.core.models import Country

class CountryForm(ModelForm):
    class Meta:
        model = Country
        fields = '__all__'