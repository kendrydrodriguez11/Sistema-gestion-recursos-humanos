from django.urls import reverse_lazy
from apps.personal_training.forms.application import ApplicationForm, ApplicationByCourseForm, ApplicationByUpdateCostForm
from apps.security.mixins.mixins import ListViewMixin,CreateViewMixin,UpdateViewMixin,DeleteViewMixin,PermissionMixin
from apps.personal_training.models import Application, Course, Employee
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.urls import reverse
from crum import get_current_user

class ApplicationListView(PermissionMixin,ListViewMixin,ListView):
    model = Application
    template_name = 'applications/list.html'
    context_object_name = 'applications'
    permission_required="view_application"
    # paginate_by = 3
    # query=None
    
    def get_queryset(self):
        q1 = self.request.GET.get('q1')
        filter_by = self.request.GET.get('filter')
        query = Q()

        user_sucursal = None
        
        # Obtén la sucursal del usuario actual
        if self.request.user.is_authenticated:
            user_sucursal = self.request.user.sucursal

        if q1:
            if filter_by == 'employee':
                query |= Q(employee__firts_name__icontains=q1) | Q(employee__last_name__icontains=q1)
            elif filter_by == 'years':
                query |= Q(year__icontains=q1)

        # Agrega la condición de filtrado por sucursal al query
        if user_sucursal:
            query &= Q(sucursal=user_sucursal)

        if query:
            return self.model.objects.filter(query).order_by('id')
        else:
            return self.model.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Applications'
        context['create_url'] = reverse_lazy('personal_training:application_create')
        context['permission_add'] = context['permissions'].get('add_application','')
        return context
    
class ApplicationCreateView(PermissionMixin,CreateViewMixin,CreateView,):
    model = Application
    template_name = 'applications/form.html'
    form_class = ApplicationForm
    success_url = reverse_lazy('personal_training:application_list')
    permission_required="add_application"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Application'
        context['back_url'] = self.success_url
        return context
    
class ApplicationCreateByCurseView(PermissionMixin,CreateViewMixin,CreateView):
    model = Application
    template_name = 'applications/form.html'
    form_class = ApplicationByCourseForm
    success_url = reverse_lazy('personal_training:course_list')
    permission_required = "add_application"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        course_object = get_object_or_404(Course, id=self.kwargs.get('pk'))
        context['course_name'] = course_object.name
        context['grabar'] = 'Grabar Application'
        context['back_url'] = self.success_url
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['employee'] = get_object_or_404(Employee, login=get_current_user().username)
        initial['course'] = self.kwargs.get('pk')
        return initial

class ApplicationUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = Application
    template_name = 'applications/form.html'
    form_class = ApplicationForm
    success_url = reverse_lazy('personal_training:application_list')
    permission_required="change_application"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Application'
        context['back_url'] = self.success_url
        return context
    
class ApplicationDeleteView(PermissionMixin,DeleteViewMixin,DeleteView):
    model = Application
    template_name = 'applications/delete.html'
    success_url = reverse_lazy('personal_training:application_list')
    permission_required="delete_application"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Application'
        context['description'] = f"¿Desea Eliminar El Application: {self.object.employee.get_full_name()} - {self.object.course.name}?"
        context['back_url'] = self.success_url
        return context
    
class ApplicationDetailsView(PermissionMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            application = Application.objects.get(
                id=request.GET.get('id'))
            return JsonResponse({'application':{
                'employee': application.employee.get_full_name(),
                'course': application.course.name,
                'description': application.description,
                'approved_boss': application.approved_boss,
                'approved_commission': application.approved_commission,
                'state': application.state,
                'cost': application.cost,
                'state': application.state,
            }})
        except Application.DoesNotExist:
            return JsonResponse({'error': 'No existe la aplicación'}, status=400)
        

class ApplicationToggleApproveBossView(PermissionMixin, View):
   permission_required= "application_approve_boss"
   def get(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        application.approved_boss = not application.approved_boss
        application.save()
        return redirect('personal_training:application_list')

class ApplicationToggleApproveCommissionView(PermissionMixin, View):
   permission_required= "application_approve_commission"
   def get(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        application.approved_commission = not application.approved_commission
        application.save()
        return redirect('personal_training:application_list')


class ApplicationSetCostView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = Application
    template_name = 'applications/form.html'
    form_class = ApplicationByUpdateCostForm
    success_url = reverse_lazy('personal_training:application_list')
    permission_required = "application_add_cost"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar costo'
        context['back_url'] = self.success_url
        return context