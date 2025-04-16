from django.db import models
from django.forms import model_to_dict

from apps.core.models import ModelBase
from apps.payment_role.models import Item
from apps.personal_file.models import Employee

class Credit(ModelBase):
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,verbose_name='Empleado')
    item = models.ForeignKey(Item,on_delete=models.PROTECT,verbose_name='Tipo Descuento')
    date_credit = models.DateTimeField(verbose_name='Fecha desde')
    date_initial = models.DateTimeField(verbose_name='Fecha hasta')
    value = models.DecimalField(verbose_name="Interes(%)", decimal_places=2,max_digits=10)
    interest = models.DecimalField(verbose_name="Valor Interes", decimal_places=2,max_digits=10)
    value_interest = models.DecimalField(verbose_name="Valor Prestamo", decimal_places=2,max_digits=10)
    nume_quota = models.IntegerField("Numero Cuotas",blank=True,null=True)
    balance = models.DecimalField(verbose_name="Saldo", decimal_places=2,max_digits=10)
    status = models.BooleanField(verbose_name="Procesado",default=False)
    reason = models.CharField(verbose_name="Observacion",max_length=200,blank=True,null=True)
    active = models.BooleanField(verbose_name='Activo', default=True)
    calendar_processed = models.IntegerField("Calendario Procesado",blank=True,null=True)
    status_processed = models.BooleanField(verbose_name='Activo Procesado', default=False)
    balance_processed = models.DecimalField(verbose_name="Saldo Procesado", decimal_places=2,max_digits=10)
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return f'${self.item.description} - ${self.employee.get_full_name()}'

    class Meta:
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuentos'
        ordering = ['id']

class CreditsDetail(ModelBase):
    credit = models.ForeignKey(Credit,on_delete=models.PROTECT,verbose_name='Descuento')
    date_discount = models.DateTimeField(verbose_name='Fecha Descuento')
    quota = models.IntegerField("Numero Cuota",default=0)
    status = models.BooleanField(verbose_name="Procesado",choices=((1,'pendiente'),(2,'Rol'),(3,'Comprobante')),  default=1)
    balance_quota = models.DecimalField(verbose_name="Saldo Cuota", decimal_places=2,max_digits=10)
    calendar_quota_processed = models.IntegerField("Calendario Procesado",blank=True,null=True)
    status_quota_processed = models.BooleanField(verbose_name='Activo Procesado', default=False)
    balance_quota_processed = models.DecimalField(verbose_name="Saldo Procesado cuots", decimal_places=2,max_digits=10)
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return f'${self.date_discount} - ${self.quota}'

    class Meta:
        verbose_name = 'Prestamo Detalle'
        verbose_name_plural = 'Prestamos Detalles'
        ordering = ['id']

