from django.urls import reverse_lazy
from apps.security.forms.menu import MenuForm
from apps.security.mixins.mixins import ListViewMixin,CreateViewMixin,UpdateViewMixin,DeleteViewMixin,PermissionMixin
from apps.security.models import Menu
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q

class MenuListView(PermissionMixin,ListViewMixin,ListView):
    model = Menu
    template_name = 'menus/list.html'
    context_object_name = 'menus'
    permission_required="view_menu"
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
        context['title'] = 'Menus'
        context['create_url'] = reverse_lazy('security:menu_create')
        context['permission_add'] = context['permissions'].get('add_menu','')
        
        return context
    
class MenuCreateView(PermissionMixin,CreateViewMixin,CreateView,):
    model = Menu
    template_name = 'menus/form.html'
    form_class = MenuForm
    success_url = reverse_lazy('security:menu_list')
    permission_required="add_menu"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Menu'
        context['back_url'] = self.success_url
        return context

class MenuUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = Menu
    template_name = 'menus/form.html'
    form_class = MenuForm
    success_url = reverse_lazy('security:menu_list')
    permission_required="update_menu"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Menu'
        context['back_url'] = self.success_url
        return context
    
class MenuDeleteView(PermissionMixin,DeleteViewMixin,DeleteView):
    model = Menu
    template_name = 'menus/delete.html'
    success_url = reverse_lazy('security:menu_list')
    permission_required="delete_menu"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Menu'
        context['description'] = f"¿Desea Eliminar El Menu: {self.object.name}?"
        context['back_url'] = self.success_url
        return context