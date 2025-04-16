from django.contrib import admin

from apps.personal_training.models import Application, Supplier, Course, Certificate

# Register your models here.
admin.site.register(Supplier)
admin.site.register(Course)
admin.site.register(Application)
admin.site.register(Certificate)