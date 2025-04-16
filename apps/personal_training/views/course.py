from django.urls import reverse_lazy
from apps.personal_training.forms.course import CourseForm
from apps.security.mixins.mixins import ListViewMixin,CreateViewMixin,UpdateViewMixin,DeleteViewMixin,PermissionMixin
from apps.personal_training.models import Course
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q

class CourseListView(PermissionMixin,ListViewMixin,ListView):
    model = Course
    template_name = 'courses/list.html'
    context_object_name = 'courses'
    permission_required="view_course"
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
        context['title'] = 'Courses'
        context['create_url'] = reverse_lazy('personal_training:course_create')
        context['permission_add'] = context['permissions'].get('add_course','')
        return context
    
class CourseCreateView(PermissionMixin,CreateViewMixin,CreateView,):
    model = Course
    template_name = 'courses/form.html'
    form_class = CourseForm
    success_url = reverse_lazy('personal_training:course_list')
    permission_required="add_course"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Course'
        context['back_url'] = self.success_url
        return context

class CourseUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = Course
    template_name = 'courses/form.html'
    form_class = CourseForm
    success_url = reverse_lazy('personal_training:course_list')
    permission_required="change_course"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar course'
        context['back_url'] = self.success_url
        return context
    
class CourseDeleteView(PermissionMixin,DeleteViewMixin,DeleteView):
    model = Course
    template_name = 'courses/delete.html'
    success_url = reverse_lazy('personal_training:course_list')
    permission_required="delete_course"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar course'
        context['description'] = f"¿Desea Eliminar El Course: {self.object.name}?"
        context['back_url'] = self.success_url
        return context