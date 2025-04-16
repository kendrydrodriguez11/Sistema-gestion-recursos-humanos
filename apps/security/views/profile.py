from django.urls import reverse_lazy
from apps.security.forms.profile import ProfileForm
from apps.security.forms.user import MyPasswordChangeForm2
from apps.security.mixins.mixins import PermissionMixin, UpdateViewMixin
from apps.security.models import User
from django.views.generic import UpdateView
from django.contrib.auth.forms import PasswordChangeForm

class ProfileUpdateView(PermissionMixin,UpdateViewMixin, UpdateView):
    model = User
    template_name = 'profile/form.html'
    form_class = ProfileForm
    success_url = reverse_lazy('security:profile_update')
    permission_required = 'change_userprofile'
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Perfil'
        context['back_url'] = self.success_url
        return context
    

class UserPasswordUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = User
    template_name = 'profile/change_password.html'
    form_class = MyPasswordChangeForm2
    success_url = reverse_lazy('home')
    permission_required = 'change_userpassword'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = ':Actualización de contraseña'
        context['grabar'] = 'Cambiar Password'
        context['back_url'] = self.success_url
        return context
