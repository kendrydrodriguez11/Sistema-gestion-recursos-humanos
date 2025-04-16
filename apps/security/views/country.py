from django.urls import reverse_lazy
from apps.core.models import Country
from apps.security.forms.country import CountryForm

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q

class CountryListView(ListView):
    model = Country
    template_name = 'country/list.html'
    context_object_name = 'countries'
    paginate_by = 2
    query=None
    
    def get_queryset(self):
        self.query=Q()
        q1 = self.request.GET.get('q1') # ver
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.AND) 
        #q2 = self.request.GET.get('q2') # ver
        # if q2 is not None:
        #     query.add(Q(estado__icontains=q2), Q.AND)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pais'
        context['create_url'] = reverse_lazy('security:country_create')
        return context

class CountryCreateView(CreateView):
    model = Country
    template_name = 'country/form.html'
    form_class = CountryForm
    success_url = reverse_lazy('security:country_list')
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Ingresar nuevo Pais'
        context['grabar'] = 'Grabar Pais'
        context['back_url'] = self.success_url
        return context
        
class CountryUpdateView(UpdateView):
    model = Country
    template_name = 'country/form.html'
    form_class = CountryForm
    success_url = reverse_lazy('security:country_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Actualizar el Pais'
        context['grabar'] = 'Actualizar Pais'
        context['back_url'] = self.success_url
        return context
    
class CountryDeleteView(DeleteView):
    model = Country
    template_name = 'country/delete.html'
    success_url = reverse_lazy('security:country_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Eliminar el Pais'
        context['grabar'] = 'Eliminar Pais'
        context['description'] = f"¿Desea Eliminar El Pais: {self.object.name}?"
        context['back_url'] = self.success_url
        return context