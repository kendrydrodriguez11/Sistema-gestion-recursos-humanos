from django.db import models
from apps.core.models import ModelBase

from apps.personal_file.models import Employee
 # weekday() devuelve un número donde 0 representa el lunes y 6 representa el domingo.
 # numero_dia =  fecha.weekday()

dias = ((0,"Lunes"),(1,"Martes"),(2,"Miercoles"),(3,"Jueves"),(4,"Viernes"),(5,"Sabado"),(6,"Domingo"))

class Jornada(ModelBase):
    descripcion = models.CharField("Jornada",max_length=200)
    dia_desde = models.IntegerField(choices=dias,default=[0][0])
    dia_hasta = models.IntegerField(choices=dias,default=[4][0])
    hora_entrada = models.TimeField()
    hora_salida_lunch = models.TimeField()
    hora_entrada_lunch = models.TimeField()
    hora_salida = models.TimeField()
    horas_trabajo=models.IntegerField("Horas Trabajadas",default=8)
    
    def __str__(self):
        return self.descripcion
    
class MarcadaReloj(ModelBase):
    empleado = models.ForeignKey(Employee, on_delete=models.CASCADE)
    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_entrada = models.TimeField(blank=True, null=True)
    hora_salida_lunch = models.TimeField(blank=True, null=True)
    hora_entrada_lunch = models.TimeField(blank=True, null=True)
    hora_salida = models.TimeField(blank=True, null=True)
    horas_trabajadas = models.IntegerField("Horas Trabajadas",default=0)
    
    def __str__(self):
        return f"{self.empleado} - {self.fecha}"