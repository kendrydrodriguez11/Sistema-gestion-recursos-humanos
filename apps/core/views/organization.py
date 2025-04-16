from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q
from apps.core.form.organization import OrganizationForm
from apps.core.models import Organization
from apps.security.mixins.mixins import ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin

class OrganizationListView(ListViewMixin, ListView):
    template_name = 'organization/list.html'
    model = Organization
    context_object_name = 'organizations'
    permission_required = 'view_organization'
    
    def get_queryset(self):
        q1 = self.request.GET.get('q1') # ver
        if q1 is not None: self.query.add(Q(name__icontains=q1), Q.AND) 
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permission_add'] = context['permissions'].get('add_organization','')
        context['create_url'] = reverse_lazy('core:organization_create')
        return context

class OrganizationCreateView(CreateViewMixin, CreateView):
    model = Organization
    template_name = 'organization/form.html'
    form_class = OrganizationForm
    success_url = reverse_lazy('core:organization_list')
    permission_required = 'add_organization'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Sucursal'
        context['back_url'] = self.success_url
        return context


class OrganizationUpdateView(UpdateViewMixin, UpdateView):
    model = Organization
    template_name = 'organization/form.html'
    form_class = OrganizationForm
    success_url = reverse_lazy('core:organization_list')
    permission_required = 'change_organization'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Sucursal'
        context['back_url'] = self.success_url
        return context


class OrganizationDeleteView(DeleteViewMixin, DeleteView):
    model = Organization
    template_name = 'organization/delete.html'
    success_url = reverse_lazy('core:organization_list')
    permission_required = 'delete_organization'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Sucursal'
        context['description'] = f"¿Desea Eliminar la Sucursal: {self.object.name}?"
        context['back_url'] = self.success_url
        return context
