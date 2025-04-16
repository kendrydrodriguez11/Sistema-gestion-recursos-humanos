
from django.views.generic import TemplateView
from apps.security.instance.menu_module import MenuModule
from apps.security.mixins.mixins import PermissionMixin


class HomeTemplateView(PermissionMixin,TemplateView):
    template_name = 'components/base.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context
    
class ModuloTemplateView(PermissionMixin,TemplateView):
    template_name = 'options/modules.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context
    
    