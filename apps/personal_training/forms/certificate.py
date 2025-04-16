from django import forms
from django.forms import ModelForm
from apps.personal_training.models import Certificate

class CertificateForm(ModelForm):
    class Meta:
        model = Certificate
        fields = '__all__'
        exclude = ['created_at', 'created_by', 'updated_at', 'update_by']
        

class CertificateByCourseForm(ModelForm):
    class Meta:
        model = Certificate
        fields = '__all__'
        exclude = ['created_at', 'created_by', 'updated_at', 'update_by']
        widgets = {
           'employee': forms.HiddenInput(),
           'course': forms.HiddenInput(),
        }