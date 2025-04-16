from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q
from apps.security.forms.user import UserForm
from apps.security.models import User
from apps.security.mixins.mixins import ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin

class UserListView(ListViewMixin, ListView):
    template_name = 'user/list.html'
    model = User
    context_object_name = 'users'
    paginate_by=1
    permission_required = 'view_user'
    
    def get_queryset(self):
        q1 = self.request.GET.get('q1') # ver
        q2 = self.request.GET.get('q2') # ver
        q3 = self.request.GET.get('q3') # ver
        if q1 is not None: self.query.add(Q(dni__icontains=q1), Q.AND) 
        if q2 is not None: self.query.add(Q(last_name__icontains=q2), Q.AND)
        if q3 is not None: self.query.add(Q(email__icontains=q3), Q.AND)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permission_add'] = context['permissions'].get('add_user','')
        context['create_url'] = reverse_lazy('security:user_create')
        return context

  

class UserCreateView(CreateViewMixin, CreateView):
    model = User
    template_name = 'user/form.html'
    form_class = UserForm
    success_url = reverse_lazy('security:user_list')
    permission_required = 'add_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Usuario'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        form.instance.set_password(form.cleaned_data['password'])
        form.instance.save()
        return super().form_valid(form)

class UserUpdateView(UpdateViewMixin, UpdateView):
    model = User
    template_name = 'user/form.html'
    form_class = UserForm
    success_url = reverse_lazy('security:user_list')
    permission_required = 'change_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Usuario'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        password_anterior = form.fields['password'].initial
        self.object = form.save()
        if form.cleaned_data['password'] != password_anterior:
            form.instance.set_password(form.cleaned_data['password'])
        form.instance.save()
        return super().form_valid(form)

class UserDeleteView(DeleteViewMixin, DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('security:user_list')
    permission_required = 'delete_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Usuario'
        context['description'] = f"¿Desea Eliminar El Usuario: {self.object.get_full_name}?"
        context['back_url'] = self.success_url
        return context
