from django.views.generic import TemplateView
from apps.security.mixins.mixins import PermissionMixin

    
class SecurityTemplateView(PermissionMixin,TemplateView):
    template_name = 'security.html'
    
    
