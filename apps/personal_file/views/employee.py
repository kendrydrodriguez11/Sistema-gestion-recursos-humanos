from django.urls import reverse_lazy
from apps.personal_file.form.employee import EmployeeForm
from apps.personal_file.models import Employee

from apps.personal_file.models import Employee
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q

from apps.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin

class EmployeeListView(PermissionMixin,ListViewMixin,ListView):
    model = Employee
    template_name = 'employees/list.html'
    context_object_name = 'employees'
    permission_required="view_employee"
    # paginate_by = 3
    # query=None
    
    def get_queryset(self):
        # self.query=Q()
        q1 = self.request.GET.get('q1') # ver
        if q1 is not None:
            self.query.add(Q(last_name__icontains=q1), Q.AND) 
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('personal_file:employee_create')
        context['permission_add'] = context['permissions'].get('add_employee','')
        
        return context
    
class EmployeeCreateView(PermissionMixin,CreateViewMixin,CreateView,):
    model = Employee
    template_name = 'employees/form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('personal_file:employee_list')
    permission_required="add_employee"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Empleado'
        context['back_url'] = self.success_url
        return context

class EmployeeUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = Employee
    template_name = 'employees/form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('personal_file:employee_list')
    permission_required="update_employee"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Empleado'
        context['back_url'] = self.success_url
        return context
    
class EmployeeDeleteView(PermissionMixin,DeleteViewMixin,DeleteView):
    model = Employee
    template_name = 'employees/delete.html'
    success_url = reverse_lazy('personal_file:employee_list')
    permission_required="delete_employee"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Empleado'
        context['description'] = f"¿Desea Eliminar El Employee: {self.object.get_full_name()}?"
        context['back_url'] = self.success_url
        return context