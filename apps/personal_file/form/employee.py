from django.forms import ModelForm
from apps.personal_file.models import Employee

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['created_at','created_by','updated_at','update_by']