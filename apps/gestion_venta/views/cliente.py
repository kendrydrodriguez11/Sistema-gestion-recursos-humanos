from django.urls import reverse_lazy
from apps.gestion_venta.forms.cliente import ClienteForm
from apps.security.mixins.mixins import ListViewMixin,CreateViewMixin,UpdateViewMixin,DeleteViewMixin,PermissionMixin
from apps.gestion_venta.models import Cliente
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q

class ClienteListView(PermissionMixin,ListViewMixin,ListView):
    model = Cliente
    template_name = 'clientes/list.html'
    context_object_name = 'clientes'
    permission_required="view_cliente"
    # paginate_by = 3
    # query=None
    
    def get_queryset(self):
        self.query=Q()
        q1 = self.request.GET.get('q1') # ver
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.AND) 
        # q2 = self.request.GET.get('q2') # ver
        # if q2 is not None:
        #     query.add(Q(estado__icontains=q2), Q.AND)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'clientes'
        context['create_url'] = reverse_lazy('gestion_venta:cliente_create')
        context['permission_add'] = context['permissions'].get('add_cliente','')
        return context
    
class ClienteCreateView(PermissionMixin,CreateViewMixin,CreateView,):
    model = Cliente
    template_name = 'clientes/form.html'
    form_class = ClienteForm
    success_url = reverse_lazy('gestion_venta:cliente_list')
    permission_required="add_cliente"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Cliente'
        context['back_url'] = self.success_url
        return context

class ClienteUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = Cliente
    template_name = 'clientes/form.html'
    form_class = ClienteForm
    success_url = reverse_lazy('gestion_venta:cliente_list')
    permission_required="change_cliente"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar cliente'
        context['back_url'] = self.success_url
        return context
    
class ClienteDeleteView(PermissionMixin,DeleteViewMixin,DeleteView):
    model = Cliente
    template_name = 'clientes/delete.html'
    success_url = reverse_lazy('gestion_venta:cliente_list')
    permission_required="delete_cliente"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar cliente'
        context['description'] = f"¿Desea Eliminar el cliente: {self.object.name}?"
        context['back_url'] = self.success_url
        return context