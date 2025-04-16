from django.urls import reverse_lazy
from apps.personal_training.forms.certificate import CertificateForm, CertificateByCourseForm
from apps.security.mixins.mixins import ListViewMixin,CreateViewMixin,UpdateViewMixin,DeleteViewMixin,PermissionMixin
from apps.personal_training.models import Certificate, Course
from apps.personal_file.models import Employee
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q
from crum import get_current_user
from django.shortcuts import get_object_or_404
import os
from django.http import HttpResponse
from django.conf import settings
from django.views import View

class CertificateListView(PermissionMixin,ListViewMixin,ListView):
    model = Certificate
    template_name = 'certificates/list.html'
    context_object_name = 'certificates'
    permission_required="view_application"
    # paginate_by = 3
    # query=None
    
    def get_queryset(self):
        self.query=Q()
        q1 = self.request.GET.get('q1') # ver
        if q1 is not None:
            self.query |= Q(employee__firts_name__icontains=q1) | Q(employee__last_name__icontains=q1)
        # q2 = self.request.GET.get('q2') # ver
        # if q2 is not None:
        #     query.add(Q(estado__icontains=q2), Q.AND)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Certificates'
        context['create_url'] = reverse_lazy('personal_training:certificate_create')
        context['permission_add'] = context['permissions'].get('add_certificate','')
        
        return context
    
class CertificateCreateView(PermissionMixin,CreateViewMixin,CreateView,):
    model = Certificate
    template_name = 'certificates/form.html'
    form_class = CertificateForm
    success_url = reverse_lazy('personal_training:certificate_list')
    permission_required="add_certificate"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['grabar'] = 'Grabar Certificate'
        context['back_url'] = self.success_url
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        return initial

class CertificateCreateByCourseView(PermissionMixin,CreateViewMixin,CreateView,):
    model = Certificate
    template_name = 'certificates/form.html'
    form_class = CertificateByCourseForm
    success_url = reverse_lazy('personal_training:course_list')
    permission_required="add_certificate"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        course_object = get_object_or_404(Course, id=self.kwargs.get('pk'))
        context['course_name'] = course_object.name
        context['grabar'] = 'Grabar Certificate'
        context['back_url'] = self.success_url
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        initial['employee'] = get_object_or_404(Employee, login=get_current_user().username)
        initial['course'] = self.kwargs['pk']
        return initial


class CertificateUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = Certificate
    template_name = 'applications/form.html'
    form_class = CertificateForm
    success_url = reverse_lazy('personal_training:certificate_list')
    permission_required="change_certificate"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Certificate'
        context['back_url'] = self.success_url
        return context
    
class CertificateDeleteView(PermissionMixin,DeleteViewMixin,DeleteView):
    model = Certificate
    template_name = 'certificates/delete.html'
    success_url = reverse_lazy('personal_training:certificate_list')
    permission_required = "delete_certificate"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Certificate'
        context['description'] = f"¿Desea Eliminar El Certificate: {self.object.employee.get_full_name()} - {self.object.course.name}?"
        context['back_url'] = self.success_url
        return context
    
class CertificateView(PermissionMixin, View):
    permission_required = "certificate_view_pdf"
    def get(self, request, certificate_id):
        certificate = get_object_or_404(Certificate, id=certificate_id)
                
        pdf_path = os.path.join(settings.MEDIA_ROOT, str(certificate.certificado_pdf))
        
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        
        response['Content-Disposition'] = f'inline; filename="{certificate.certificado_pdf.name}"'
        return response