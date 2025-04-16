from django.urls import reverse_lazy
from apps.gestion_venta.forms.categoria import CategoriaForm
from apps.security.mixins.mixins import ListViewMixin,CreateViewMixin,UpdateViewMixin,DeleteViewMixin,PermissionMixin
from apps.gestion_venta.models import Categoria
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q

class CategoriaListView(PermissionMixin,ListViewMixin,ListView):
    model = Categoria
    template_name = 'categorias/list.html'
    context_object_name = 'categorias'
    permission_required="view_categoria"
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
        context['title'] = 'Categorias'
        context['create_url'] = reverse_lazy('gestion_venta:categoria_create')
        context['permission_add'] = context['permissions'].get('add_categoria','')
        return context
    
class CategoriaCreateView(PermissionMixin,CreateViewMixin,CreateView,):
    model = Categoria
    template_name = 'categorias/form.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('gestion_venta:categoria_list')
    permission_required="add_categoria"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Categoria'
        context['back_url'] = self.success_url
        return context

class CategoriaUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = Categoria
    template_name = 'categorias/form.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('gestion_venta:categoria_list')
    permission_required="change_categoria"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar categoria'
        context['back_url'] = self.success_url
        return context
    
class CategoriaDeleteView(PermissionMixin,DeleteViewMixin,DeleteView):
    model = Categoria
    template_name = 'categorias/delete.html'
    success_url = reverse_lazy('gestion_venta:categoria_list')
    permission_required="delete_categoria"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar categoria'
        context['description'] = f"¿Desea Eliminar La Categoria: {self.object.name}?"
        context['back_url'] = self.success_url
        return context