from django import forms
from django.forms import ModelForm
from apps.personal_training.models import Application
from django.forms.widgets import TextInput

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = '__all__'
        exclude = ['created_at', 'created_by', 'updated_at', 'update_by', 'sucursal', 'year', 'fecha_inicio', 'fecha_fin', 'approved_boss', 'approved_commission', 'approved_all', 'cost']

class ApplicationByCourseForm(ModelForm):
    class Meta:
        model = Application
        fields = ['employee', 'course','description']
        widgets = {
           'course': forms.HiddenInput(),
           'employee': forms.HiddenInput(),
        }

class ApplicationByUpdateCostForm(ModelForm):
    class Meta:
        model = Application
        fields = ['employee', 'course', 'cost']
        widgets = {
            'employee' : forms.HiddenInput(),
            'course': forms.HiddenInput(),
        }