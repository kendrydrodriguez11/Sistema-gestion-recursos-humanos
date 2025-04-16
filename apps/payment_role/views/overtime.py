import json
from django.forms import model_to_dict
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from apps.payment_role.forms.overtime import OvertimeForm
from apps.security.mixins.mixins import ListViewMixin,CreateViewMixin,UpdateViewMixin,DeleteViewMixin,PermissionMixin
from apps.payment_role.models import Item, Overtime, OvertimeDetail
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q
from apps.personal_file.models import Employee

class OvertimeListView(PermissionMixin,ListViewMixin,ListView):
    model = Overtime
    template_name = 'overtimes/list.html'
    context_object_name = 'overtimes'
    permission_required="view_overtime"
    
    def get_queryset(self):
       
        q1 = self.request.GET.get('q1') # ver
        if q1 is not None:
            self.query.add(Q(employee__last_name__icontains=q1), Q.AND) 
        print("request",self.request.user)     
        return self.model.objects.filter(self.query,sucursal_id=self.request.user.sucursal_id).order_by('id')
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('payment_role:overtime_create')
        context['permission_add'] = context['permissions'].get('add_overtime','')
        
        return context
    
class OvertimeCreateView(PermissionMixin,CreateViewMixin,CreateView,):
    model = Overtime
    template_name = 'overtimes/form.html'
    form_class = OvertimeForm
    success_url = reverse_lazy('payment_role:overtime_list')
    permission_required="add_overtime"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Sobretiempo'
        context['back_url'] = self.success_url
        context['hours'] = Item.objects.filter(sucursal_id=self.request.user.sucursal_id,Hours_extras=True,active=True).order_by('id')
        context['detail_hours'] =[]
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        #data = form.save(commit=False)
        if not form.is_valid():
            print("form:",form.errors) 
            return JsonResponse({},status=400)
        data = request.POST
        calendar = data['calendar']
        emp_id = data['employee']
        sucursal =  Employee.objects.get(id=emp_id).sucursal_id
        value_hour = data['value_hour']
        # nume_hours = data['nume_hours']
        total = data['total']
        cabecera = Overtime.objects.create(
            calendar_id=calendar,
            employee_id=emp_id,
            sucursal_id=sucursal,
            value_hour=value_hour,
            # nume_hours=nume_hours,
            total=total
        )
        details = json.loads(request.POST['detail'])
        for detail in details:
            OvertimeDetail.objects.create( 
                overtime_id=cabecera.id,
                item_id=detail['idHour'],
                number_hours=detail['nh'],
                value=detail['value']
            )
        return JsonResponse({},status=200)
     
        
class OvertimeUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = Overtime
    template_name = 'overtimes/form.html'
    form_class = OvertimeForm
    success_url = reverse_lazy('payment_role:overtime_list')
    permission_required="update_overtime"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Sobretiempo'
        context['back_url'] = self.success_url
        context['hours'] = Item.objects.filter(sucursal_id=self.request.user.sucursal_id,Hours_extras=True,active=True).order_by('id')
        detOvertime = list(OvertimeDetail.objects.filter(
             overtime_id=self.object.id).values(
             "item_id","item__name_short","item__value","number_hours","value"
        ))
        lista=[]
        for det in  detOvertime:
          lista.append({"id":det["item_id"],"des":det["item__name_short"],
                        "fac":float(det["item__value"]),"nh":float(det["number_hours"]),
                        "vh":float(det["value"])})
    
        context['detail_hours'] =json.dumps(lista)
        print(context['detail_hours'])
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid(): return JsonResponse({},status=400)
        data = request.POST
        calendar = data['calendar']
        emp_id = data['employee']
        sucursal =  Employee.objects.get(id=emp_id).sucursal_id
        value_hour = data['value_hour']
        total = data['total']
        overtime= Overtime.objects.get(id=self.kwargs.get('pk'))
        print(overtime)
        print("calendar",calendar)
        overtime.calendar_id=calendar
        overtime.employee_id=emp_id
        overtime.sucursal_id=sucursal
        overtime.value_hour=value_hour
        overtime.total=total
        overtime.save()
        details = json.loads(request.POST['detail'])
        OvertimeDetail.objects.filter(overtime_id=overtime.id).delete()
        for detail in details:
            OvertimeDetail.objects.create( 
                overtime_id=overtime.id,
                item_id=detail['idHour'],
                number_hours=detail['nh'],
                value=detail['value']
            )
        return JsonResponse({},status=200)
    
class OvertimeDeleteView(PermissionMixin,DeleteViewMixin,DeleteView):
   
    model = Overtime
    template_name = 'overtimes/delete.html'
    success_url = reverse_lazy('payment_role:overtime_list')
    permission_required="delete_overtime"
    
    def get_context_data(self, **kwargs):
       
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Sobretiempo'
       
        context['description'] = f"¿Desea Eliminar El Sobretiempo de la nomina:{self.object.calendar.codigo_rol} de {self.object.employee.get_full_name()}?"
        context['back_url'] = self.success_url
      
        return context
    
class OvertimeValueHours(PermissionMixin, View):
 
    def get(self, request, *args, **kwargs):
        action = request.GET.get('action', None)
        if action == 'value_hours':
            try:
                employee = Employee.objects.get(
                    id=request.GET.get('idemp')
                )
                value_hour = str(round(employee.sueldo/240,2))
                sucursal = str(employee.sucursal_id)
                return JsonResponse({'hour':value_hour,"sucursal":sucursal},status=200)
                
            except Exception as ex:
                return JsonResponse({"message":ex},status=400)   
                  
        return JsonResponse({},status=400)
        
class OvertimeDetailView(PermissionMixin, View):
 
    def get(self, request, *args, **kwargs):
        try:
            overtime = Overtime.objects.get(
                id=request.GET.get('id')
            )
                    
            det_overtime = OvertimeDetail.objects.filter(
             overtime_id=overtime.id)
            # model_to_dict(overtime)
            lista=[]
            for det in  det_overtime:
                lista.append({"id":det.item.id,"des":det.item.name_short,
                        "fac":det.item.value,"nh":det.number_hours,
                        "vh":det.value})
                
            return JsonResponse({'overtime':{'id':overtime.id,
                                             'calendar':overtime.calendar.codigo_rol,
                                             'empleado':overtime.employee.get_full_name(),
                                             'sucursal':overtime.sucursal.name,
                                             'value_hour':overtime.value_hour,
                                             'total':overtime.total,
                                             'proceso':overtime.processed,
                                           
                                             },
                                 "detail":lista},status=200)
            
        except Exception as ex:
                return JsonResponse({"message":ex},status=400)   
                  
        

        

