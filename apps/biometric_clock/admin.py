from django.contrib import admin

from apps.biometric_clock.models import Jornada, MarcadaReloj

# Register your models here.
admin.site.register(Jornada)
admin.site.register(MarcadaReloj)