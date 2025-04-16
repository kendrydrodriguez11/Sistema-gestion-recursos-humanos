from django.urls import reverse_lazy
from apps.personal_training.forms.supplier import SupplierForm
from apps.security.mixins.mixins import ListViewMixin,CreateViewMixin,UpdateViewMixin,DeleteViewMixin,PermissionMixin
from apps.personal_training.models import Supplier
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q

class SupplierListView(PermissionMixin,ListViewMixin,ListView):
    model = Supplier
    template_name = 'suppliers/list.html'
    context_object_name = 'suppliers'
    permission_required="view_supplier"
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
        context['title'] = 'Suppliers'
        context['create_url'] = reverse_lazy('personal_training:supplier_create')
        context['permission_add'] = context['permissions'].get('add_supplier','')
        
        return context
    
class SupplierCreateView(PermissionMixin,CreateViewMixin,CreateView,):
    model = Supplier
    template_name = 'suppliers/form.html'
    form_class = SupplierForm
    success_url = reverse_lazy('personal_training:supplier_list')
    permission_required="add_supplier"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Supplier'
        context['back_url'] = self.success_url
        return context

class SupplierUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = Supplier
    template_name = 'suppliers/form.html'
    form_class = SupplierForm
    success_url = reverse_lazy('personal_training:supplier_list')
    permission_required="change_supplier"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Supplier'
        context['back_url'] = self.success_url
        return context
    
class SupplierDeleteView(PermissionMixin,DeleteViewMixin,DeleteView):
    model = Supplier
    template_name = 'suppliers/delete.html'
    success_url = reverse_lazy('personal_training:supplier_list')
    permission_required="delete_supplier"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Supplier'
        context['description'] = f"¿Desea Eliminar El Supplier: {self.object.name}?"
        context['back_url'] = self.success_url
        return context