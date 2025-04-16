from django.http import JsonResponse
from django.urls import reverse_lazy
from apps.gestion_venta.forms.factura import FacturaForm
from apps.gestion_venta.models import Factura, DetalleFactura, Producto, Cliente
from apps.security.mixins.mixins import ListViewMixin,CreateViewMixin,UpdateViewMixin,DeleteViewMixin,PermissionMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
import json
from django.db.models import Q
from datetime import datetime
from django.views import View
from rrhhs import utils
from django.shortcuts import get_object_or_404, redirect

class FacturaListView(PermissionMixin,ListViewMixin,ListView):
    model = Factura
    template_name = 'facturas/list.html'
    context_object_name = 'facturas'
    permission_required="view_factura"
    # paginate_by = 3
    # query=None
    
    def get_queryset(self):
        self.query=Q()
        q1 = self.request.GET.get('q1') # ver
        if q1 is not None:
            self.query.add(Q(cliente__name__icontains=q1), Q.AND) 
        return self.model.objects.filter(self.query).order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Facturas'
        context['create_url'] = reverse_lazy('gestion_venta:factura_create')
        context['permission_add'] = context['permissions'].get('add_factura','')
        return context
    
class FacturaCreateView(PermissionMixin,CreateViewMixin,CreateView,):
    model = Factura
    template_name = 'facturas/form.html'
    form_class = FacturaForm
    success_url = reverse_lazy('gestion_venta:factura_list')
    permission_required="add_factura"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Factura'
        context['back_url'] = self.success_url
        context['productos'] = Producto.objects.all().order_by('id')
        context['detail_producto'] =[]
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            print("form:",form.errors) 
            return JsonResponse({},status=400)
        data = request.POST
        cliente_id = data['cliente']
        fecha = data['fecha']
        subtotal = data['subtotal']
        iva = data['iva']
        total = data['total']
        cabecera = Factura.objects.create(
            cliente_id=cliente_id,
            fecha=datetime.strptime(fecha, '%d/%m/%Y').strftime('%Y-%m-%d'),
            subtotal=subtotal,
            iva=iva,
            total=total,
        )
        details = json.loads(request.POST['detail'])
        for detail in details:
            DetalleFactura.objects.create(
                factura_id=cabecera.id,
                producto_id=detail['id_producto'],
                cantidad=detail['cant'],
                precio=detail['prec'],
                subtotal=detail['subtotal']
            )
        producto = Producto.objects.filter(id=detail['id_producto'])
        stock = producto.get().stock - detail['cant']
        producto.update(stock=stock)

        utils.generate_pdf(
                'facturas/report.html',
                {
                    'cliente': Cliente.objects.get(id=data['cliente']).get_full_name(),
                    'fecha': data['fecha'],
                    'subtotal': data['subtotal'],
                    'iva': data['iva'],
                    'total': data['total'],
                    'detalle': list(DetalleFactura.objects.filter(factura_id=cabecera.id).values(
                        'producto_id',
                        'producto__name',
                        'cantidad',
                        'precio',
                        'subtotal'
                    ))
                },
                "facturas/factura-{}.pdf".format(cabecera.id)
        )
        return JsonResponse({'id':cabecera.id})
    
class FacturaUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = Factura
    template_name = 'facturas/form.html'
    form_class = FacturaForm
    success_url = reverse_lazy('gestion_venta:factura_list')
    permission_required="change_factura"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Factura'
        context['back_url'] = self.success_url
        context['productos'] = Producto.objects.all().order_by('id')
        detFactura = list(DetalleFactura.objects.filter(factura_id=self.object.id).values(
            'producto_id',
            'producto__name',
            'cantidad',
            'precio',
            'subtotal'
        ))
        lista=[]
        for det in  detFactura:
            lista.append({
                'id':det['producto_id'],
                'des':det['producto__name'],
                'cant':float(det['cantidad']),
                'prec':float(det['precio']),
                'subtotal':float(det['subtotal'])
            })
            
        context['detail_producto'] = json.dumps(lista)
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        #data = form.save(commit=False)
        if not form.is_valid():
            print("form:",form.errors) 
            return JsonResponse({},status=400)
        data = request.POST
        cliente_id = data['cliente']
        fecha = data['fecha']
        subtotal = data['subtotal']
        iva = data['iva']
        total = data['total']
        cabecera = Factura.objects.filter(id=self.kwargs['pk']).update(
            cliente_id=cliente_id,
            fecha=datetime.strptime(fecha, '%d/%m/%Y').strftime('%Y-%m-%d'),
            subtotal=subtotal,
            iva=iva,
            total=total,
        )
        DetalleFactura.objects.filter(factura_id=self.kwargs['pk']).delete()
        details = json.loads(request.POST['detail'])
        for detail in details:
            DetalleFactura.objects.create(
                factura_id=self.kwargs['pk'],
                producto_id=detail['id_producto'],
                cantidad=detail['cant'],
                precio=detail['prec'],
                subtotal=detail['subtotal']
            )
        producto = Producto.objects.filter(id=detail['id_producto'])
        stock = producto.get().stock - detail['cant']
        producto.update(stock=stock)

        utils.generate_pdf(
                'facturas/report.html',
                {
                    'cliente': Cliente.objects.get(id=data['cliente']).get_full_name(),
                    'fecha': data['fecha'],
                    'subtotal': data['subtotal'],
                    'iva': data['iva'],
                    'total': data['total'],
                    'detalle': list(DetalleFactura.objects.filter(factura_id=self.kwargs['pk']).values(
                        'producto_id',
                        'producto__name',
                        'cantidad',
                        'precio',
                        'subtotal'
                    ))
                },
                "facturas/factura-{}.pdf".format(self.kwargs['pk'])
            )
        return JsonResponse({'id':self.kwargs['pk']})
    
class FacturaDeleteView(PermissionMixin,DeleteViewMixin,DeleteView):
    model = Factura
    template_name = 'facturas/delete.html'
    success_url = reverse_lazy('gestion_venta:factura_list')
    permission_required="delete_factura"
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar factura'
        context['description'] = f"¿Desea Eliminar La Factura: {self.object.cliente.get_full_name()} - {self.object.fecha}?"
        context['back_url'] = self.success_url
        return context
    

class FacturaDetailsView(PermissionMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            factura = Factura.objects.get(
                id=request.GET.get('id'))
            
            return JsonResponse({'factura':{
                'cliente': factura.cliente.get_full_name(),
                'fecha': factura.fecha,
                'subtotal': factura.subtotal,
                'iva': factura.iva,
                'total': factura.total,
                'detalle': list(DetalleFactura.objects.filter(factura_id=factura.id).values(
                    'producto_id',
                    'producto__name',
                    'cantidad',
                    'precio',
                    'subtotal'
                ))
            }}, status=200)
        except Factura.DoesNotExist:
            return JsonResponse({'error': 'No existe la factura'}, status=400)
        

class FacturaReportView(PermissionMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            id = self.kwargs['pk']
            factura = get_object_or_404(Factura, id=id)
            pdf_url = '/media/facturas/factura-{}.pdf'.format(id)
            return redirect(pdf_url)
        except Factura.DoesNotExist:
            return JsonResponse({'error': 'No existe la factura'}, status=400)