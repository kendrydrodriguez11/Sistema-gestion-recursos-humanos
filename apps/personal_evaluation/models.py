from django.db import models
from apps.core.models import ModelBase

from apps.personal_file.models import Employee


class Encuesta(ModelBase):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    anio = models.IntegerField()
    fecha_encuesta = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField()
    tiempo_duracion = models.IntegerField()
    active = models.BooleanField(default=False)

class Pregunta(ModelBase):
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    enunciado = models.TextField()
    respuesta = models.TextField
    
   
class Respuesta(ModelBase):
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Employee, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto_respuesta = models.TextField()
    estado = models.IntegerField(choices=((1,'Sobresaliente'),(2,'Muy bueno'),(3,'Bueno'),(4,'Regular'),(5,'Malo')))
    
class Tarea(ModelBase):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    requerimiento = models.FileField(
        upload_to='requerimiento/',
        verbose_name='requerimiento',
        null=True,
        blank=True,
        help_text='Sube tu requerimiento en formato PDF.'
    )
    fecha_limite = models.DateField()
    def __str__(self):
        return self.titulo

class AsignacionTarea(ModelBase):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Employee,on_delete=models.CASCADE) 
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    descripcion_entrega = models.TextField()
    acta_entrega = models.FileField(
        upload_to='acta_entrega/',
        verbose_name='acta_entrega',
        null=True,
        blank=True,
        help_text='Sube tu acta_entrega en formato PDF.'
    )    
    entrega_tarea= models.FileField(
        upload_to='entrega_tarea/',
        verbose_name='entrega_tarea',
        null=True,
        blank=True,
        help_text='Sube tu entrega_tarea en formato PDF.'
    )    
    estado = models.IntegerField(choices=((1,'Pendiente'),(2,'Devuelta'),(3,'Terminada')))
  
    def __str__(self):
        return f"{self.tarea} - {self.empleado.get_full_name()}"
    

class Evaluacion(ModelBase):
    empleado = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Ajusta 'tu_app' al nombre de tu aplicación
    fecha_evaluacion = models.DateField()
    resultado = models.CharField(max_length=100, choices=[(1, 'Excelente'), (2, 'Muy Bueno'), (3, 'Bueno'), (4, 'Regular'), (5, 'Deficiente')])
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.empleado.get_full_name()} - {self.fecha_evaluacion}"
    