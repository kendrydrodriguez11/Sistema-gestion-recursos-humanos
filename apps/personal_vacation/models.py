from django.db import models
from apps.core.models import ModelBase

from apps.personal_file.models import Employee

class CalendarVacation(ModelBase):
    anio = models.IntegerField(unique=True)
    num_empleados = models.IntegerField()
    status= models.IntegerField(choices=((1,"Generado"),(2,"Pendientes Procesar"),(3,"Procesado")))

    class Meta:
        verbose_name = 'Calendario Vacacion'
        verbose_name_plural = 'Calendario Vacaciones'
        ordering = ('-id',)
    
    def __str__(self):
        return f"{self.anio}"

class Vacation(ModelBase):
    empleado = models.ForeignKey(Employee, on_delete=models.CASCADE)
    calendario = models.ForeignKey(CalendarVacation, on_delete=models.CASCADE)
    mes = models.IntegerField()
    # si los ias < 8 desde=1 del mes al 15 del mes sino del 16 al ...
    desde = models.DateField("Fecha desde")
    hasta = models.DateField("Fecha Hasta")
    dias_menos_por_permiso = models.IntegerField(default=0)
    # añoCalendario - añoIngreso > 3 se aumenta 1 dia mas a los 15 dias normales  
    dias_vacacion = models.IntegerField()
    # sueldo/30*dias_vacacion
    sueldo = models.DecimalField(verbose_name="Sueldo",decimal_places=2,max_digits=10)
    status= models.IntegerField(choices=((1,"Sin tomar"),(2,"Gozado")))
    
    class Meta:
        verbose_name = 'Vacacion'
        verbose_name_plural = 'Vacaciones'
        ordering = ('-id',)
    
    def __str__(self):
        return f"Vacaciones de {self.empleado} para {self.calendario}"

class ChangeVacation(ModelBase):
    empleado = models.ForeignKey(Employee, on_delete=models.CASCADE)
    fecha_pedido = models.DateField(verbose_name='Fecha Pedido')
    mes = models.IntegerField()
    reason = models.CharField(verbose_name='Reason',max_length=200,null=True,blank=True)
    approved = models.BooleanField(verbose_name='Aprobado',default=False)
    active = models.BooleanField(verbose_name='Active',default=False)
    
    class Meta:
        verbose_name = 'Cambio Vacacion'
        verbose_name_plural = 'Cambio Vacaciones'
        ordering = ('-id',)
    
    def __str__(self):
        return f"{self.empleado.get_full_name()}"

    
    