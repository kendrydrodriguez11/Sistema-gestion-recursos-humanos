from django.urls import reverse_lazy
from apps.gestion_venta.forms.producto import ProductoForm
from apps.security.mixins.mixins import ListViewMixin,CreateViewMixin,UpdateViewMixin,DeleteViewMixin,PermissionMixin
from apps.gestion_venta.models import Producto
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q

class ProductoListView(PermissionMixin,ListViewMixin,ListView):
    model = Producto
    template_name = 'productos/list.html'
    context_object_name = 'productos'
    permission_required="view_producto"
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
        context['title'] = 'Productos'
        context['create_url'] = reverse_lazy('gestion_venta:producto_create')
        context['permission_add'] = context['permissions'].get('add_producto','')
        return context
    
class ProductoCreateView(PermissionMixin,CreateViewMixin,CreateView,):
    model = Producto
    template_name = 'productos/form.html'
    form_class = ProductoForm
    success_url = reverse_lazy('gestion_venta:producto_list')
    permission_required="add_producto"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Producto'
        context['back_url'] = self.success_url
        return context

class ProductoUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = Producto
    template_name = 'productos/form.html'
    form_class = ProductoForm
    success_url = reverse_lazy('gestion_venta:producto_list')
    permission_required="change_producto"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar producto'
        context['back_url'] = self.success_url
        return context
    
class ProductoDeleteView(PermissionMixin,DeleteViewMixin,DeleteView):
    model = Producto
    template_name = 'productos/delete.html'
    success_url = reverse_lazy('gestion_venta:producto_list')
    permission_required="delete_producto"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar producto'
        context['description'] = f"¿Desea Eliminar el producto: {self.object.name}?"
        context['back_url'] = self.success_url
        return context