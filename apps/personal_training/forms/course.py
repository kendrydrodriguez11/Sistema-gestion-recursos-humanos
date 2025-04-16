from django.forms import ModelForm
from apps.personal_training.models import Course

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['created_at', 'created_by', 'updated_at', 'update_by']