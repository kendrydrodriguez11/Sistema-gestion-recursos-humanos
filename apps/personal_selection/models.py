from django.db import models
from django.forms import model_to_dict

from apps.core.models import ModelBase, Organization
from apps.personal_file.models import Area, TypeContract
from rrhhs import utils

class Offer(ModelBase):
    #number_of_employees = models.IntegerField(max_length=10, blank=True, null=True, verbose_name='Numero de Empleados')
    
    name_offer = models.CharField( verbose_name='Nombre Oferta', max_length=1000, null=True)
    offer_description = models.CharField( verbose_name='Descripcion Oferta', max_length=1000, null=True)
    
    #requirements = models.CharField( verbose_name='Requisito', max_length=1000, null=True)
    requirements = models.FileField(
        upload_to='requirements/',
        verbose_name='Requisitos',
        null=True,
        blank=True
    )  

    salary = models.DecimalField( verbose_name="Salario", decimal_places=2, max_digits=18)
    publication_date = models.DateField(verbose_name='Fecha de publicacion', auto_now_add=True, null=True)  
    deadline = models.DateField(verbose_name='Fecha de Cierre')
    is_activate = models.BooleanField(verbose_name='Activo',default= True)
    vacancy_numbers = models.IntegerField(verbose_name='Vacantes disponibles')
    department=models.ForeignKey(Area,on_delete=models.PROTECT,verbose_name='Departamento', null=True)

    
    def __str__(self):
        # Utiliza el valor ya formateado de self.publication_date
        return f"{self.name_offer}"
        

    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'
        ordering = ('-id',)



class Candidate(ModelBase):
    #number_of_employees = models.IntegerField(max_length=10, blank=True, null=True, verbose_name='Numero de Empleados')    )
    first_name = models.CharField(
        verbose_name='Nombres',
        max_length=50,
        null=True
    )
    last_name = models.CharField(
        verbose_name='Apellidos',
        max_length=50,
        null=True
    )
    image = models.ImageField(
        verbose_name='Foto',
        upload_to='empleado',
        max_length=500,
        null=True,
        blank=True
    )
    email = models.EmailField(verbose_name='Email', blank=True, null=True)

    direction = models.CharField("Dirección", max_length=100, null=True,)   
    phone = models.IntegerField(verbose_name='Telefono', null=True)
    curriculum = models.FileField(
        upload_to='curriculum/',
        verbose_name='Curriculum',
        null=True,
        blank=True,
        help_text='Sube tu Curriculum en formato PDF.'
    )    
    
    presentation_letter = models.FileField(
        upload_to='cartas_presentacion/',
        verbose_name='Carta de Presentación',
        null=True,
        blank=True,
        help_text='Sube tu carta de presentación en formato PDF.'
    )
    
    is_activate = models.BooleanField(verbose_name='Estado',default= True)
    name_offer = models.ForeignKey(Offer,on_delete=models.PROTECT,verbose_name='Cargo a postular', null=True)



    def get_full_name(self):
        return f'{self.last_name}{self.first_name}'

    def get_model_dict(self):
        item = model_to_dict(self)
        item['image_url'] = self.get_image_url()
        return item
        
    def get_image_url(self):
        return utils.get_image(self.image)

    def activation_status(self):
        return "✅" if self.is_activate else "❎"

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'
        ordering = ('-id',)

class Entrevista(ModelBase):
    TIPOS_ENTREVISTA = [
        ('inicial', 'Entrevista Inicial'),
        ('final', 'Entrevista Final'),
    ]
    oferta = models.ForeignKey(Offer,on_delete=models.PROTECT,verbose_name='Oferta', null=True)
    tipo = models.CharField(max_length=10, choices=TIPOS_ENTREVISTA)
    fecha = models.DateField()
    hora = models.TimeField()
    candidato = models.ForeignKey(Candidate, on_delete=models.CASCADE) 
    entrevistador = models.CharField(max_length=200)
    comentarios = models.TextField(blank=True, null=True)
  
    def __str__(self):
        return f"{self.tipo} - {self.candidato} - {self.fecha}"


class PruebaTecnica(ModelBase):
    oferta = models.ForeignKey(Offer,on_delete=models.PROTECT,verbose_name='Oferta', null=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    requerimiento = models.FileField(
        upload_to='prueba_tecnica/',
        verbose_name='prueba_tecnica',
        null=True,
        blank=True,
        help_text='Sube tu prueba_tecnica en formato PDF.'
    )
    fecha_limite = models.DateField()
    def __str__(self):
        return self.titulo

class AsignacionPrueba(ModelBase):
    prueba_tecnica = models.ForeignKey(PruebaTecnica, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidate,on_delete=models.CASCADE) 
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    descripcion_entrega = models.TextField()
    archivo_prueba= models.FileField(
        upload_to='entrega_prueba/',
        verbose_name='entrega_prueba',
        null=True,
        blank=True,
        help_text='Sube tu entrega_prueba en formato PDF,rar.'
    )    
    estado = models.IntegerField(choices=((1,'Pendiente'),(2,'incompleta'),(3,'Satisfactoria')))
  
    def __str__(self):
        return f"{self.candidato.get_full_name()}"
    

class Resultado(ModelBase):
    candidato = models.ForeignKey(Candidate, on_delete=models.CASCADE)  # Ajusta 'tu_app' al nombre de tu aplicación
    fecha_resultado = models.DateField()
    resultado = models.CharField(max_length=100, choices=[('Excelente', 'Excelente'), ('Bueno', 'Bueno'), ('Regular', 'Regular'), ('Deficiente', 'Deficiente')])
    nota= models.DecimalField(max_digits=5, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)
    ganador = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.candidato.get_full_name()}"
    
class Contract(ModelBase):
    customer = models.ForeignKey(Candidate,on_delete=models.PROTECT,verbose_name='Candidato', null=True)
    sucursal = models.ForeignKey(Organization, on_delete=models.PROTECT)
    numero_contrato = models.CharField(max_length=100, unique=True, verbose_name='Número de Contrato')
    contract_date = models.DateField(verbose_name='Fecha del Contrato',auto_now_add=True, null=True)
    start_date_of_work=models.DateField(verbose_name='Inicio del Contrato',null=True)
    finish_date_of_work=models.DateField(verbose_name='Final del Contrato',null=True)
    type_contract = models.ForeignKey(TypeContract,on_delete=models.PROTECT,verbose_name='Tipo Contrato', blank=True, null=True)
    oferta = models.ForeignKey(Offer,on_delete=models.PROTECT,verbose_name='Oferta', null=True)
    

    #type_of_contract = 
   
    # def __str__(self):
    #     return self.start_date
 
    def save(self, *args, **kwargs):
        if not self.numero_contrato:
            # Obtener el último contrato existente
            last_contract = Contract.objects.order_by('-id').first()

            print(f'last_contract: {last_contract}')

            # Inicializar el número de contrato en 1 si no hay contratos existentes
            numero_contrato = 1

            # Si hay un contrato existente, incrementar su número de contrato
            if last_contract and last_contract.numero_contrato:
                numero_contrato = int(last_contract.numero_contrato) + 1

            # Generar el nuevo número de contrato
            self.numero_contrato = str(numero_contrato)

            print(f'new numero_contrato: {self.numero_contrato}')

        super().save(*args, **kwargs)

   
    class Meta:
        verbose_name = 'Contract'
        verbose_name_plural = 'contracts'
        ordering = ('-id',)


class Clause(ModelBase):
    contrato = models.ForeignKey(Contract, on_delete=models.CASCADE)
    titulo_clausula = models.CharField(max_length=255)
    contenido = models.TextField()
    
    def __str__(self):
        return self.titulo
    
