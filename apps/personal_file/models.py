import datetime
from django.db import models
from django.forms import model_to_dict
#from apps.biometric_clock.models import Jornada
from apps.core.models import City, Country, ModelBase, Organization
from rrhhs import utils
from rrhhs.const import EMPLOYEE_CLASS, FREQUENCY_ROL
from django.utils.timezone import now


class KinshipType(ModelBase):
    kinship = models.CharField(verbose_name='Parentesco', max_length=100, unique=True)
    age_limit = models.IntegerField(verbose_name="Edad Limite",default=18)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def __str__(self):
        return f'{self.kinship}'
    
    class Meta:
        verbose_name = 'Parentesco'
        verbose_name_plural = ' Parentescos'
        ordering = ('-id',)
        
class MaritalStatus(ModelBase):
    estado_civil = models.CharField(verbose_name='Estado civil', max_length=50, unique=True)
    state = models.BooleanField(verbose_name='Activo', default=True)
  
    def __str__(self):
        return self.estado_civil

    class Meta:
        verbose_name = 'Estado civil'
        verbose_name_plural = 'Estado civil'
        ordering = ['-id']

class Post(ModelBase):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    profile = models.TextField(verbose_name='Perfil')
    studies = models.TextField(verbose_name='Estudios', max_length=200)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['-name']

class Category(ModelBase):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    salary = models.DecimalField(verbose_name="Sueldo", decimal_places=2,max_digits=18)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['-name']
# docente, administrativo, obrero
class TypeEmployee(ModelBase):
    name = models.CharField(verbose_name='Descripcion', max_length=50, unique=True)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item
 
    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Tipo Empleado'
        verbose_name_plural = 'Tipo Empelados'
        ordering = ['-name']

# indefinido, eventual, ocacional
class TypeContract(ModelBase):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo Contrato'
        verbose_name_plural = 'Tipo Contratos'
        ordering = ['-name']

# codigo trabajo, loes, losep
class TypeRegime(ModelBase):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo Regimen'
        verbose_name_plural = 'Tipo Regimens'
        ordering = ['-name']

# gerencia, direccion, departamento, seccion
class TypeArea(ModelBase):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def __str__(self):
        return self.name

    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo Area'
        verbose_name_plural = 'Tipo Areas'
        ordering = ['-name']
# area de trabajo
class Area(ModelBase):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    type_area=models.ForeignKey(TypeArea,on_delete=models.PROTECT,verbose_name='type_area')
    sucursal = models.ForeignKey(Organization,on_delete=models.PROTECT,verbose_name='Sucursal')
    predecessor = models.ForeignKey("self",on_delete=models.PROTECT,verbose_name='Predecesor',blank=True,null=True)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        ordering = ['-name']


class Employee(ModelBase):
    QR = models.ImageField("QR", upload_to='qrcodes/', blank=True, null=True)
    firts_name = models.CharField(verbose_name='Nombres',max_length=50,)
    last_name = models.CharField(verbose_name='Apellidos',max_length=50,)
    login = models.CharField(verbose_name='login',max_length=50,blank=True,null=True)
    image = models.ImageField(verbose_name='Foto',upload_to='empleado',max_length=500,null=True,blank=True)
    dni = models.CharField(verbose_name="Dni", max_length=50)
    phone = models.CharField(verbose_name="Teléfono", max_length=50, blank=True, null=True)
    email = models.CharField(verbose_name="Correo", max_length=100)
    country = models.ForeignKey(Country,on_delete=models.PROTECT,verbose_name='Pais')
    city = models.ForeignKey(City,on_delete=models.PROTECT,verbose_name='Ciudad', blank=True, null=True)
    direction = models.CharField(verbose_name="Dirección", max_length=100)
    latitude = models.CharField(verbose_name="Latitud", max_length=100, blank=True, null=True)
    longitude = models.CharField(verbose_name="Longitud", max_length=100, blank=True, null=True)
    sucursal = models.ForeignKey(Organization,on_delete=models.PROTECT,verbose_name='Sucursal', blank=True, null=True)
    marital_status = models.ForeignKey(MaritalStatus,on_delete=models.PROTECT,verbose_name='Estado Civil', blank=True, null=True)
    date_admission = models.DateTimeField(verbose_name="Fecha Ingreso",default=now)
    post = models.ForeignKey(Post,on_delete=models.PROTECT,verbose_name='Cargo', blank=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,verbose_name='Categoria', blank=True, null=True)
    area = models.ForeignKey(Area,on_delete=models.PROTECT,verbose_name='Area', blank=True, null=True)
    employee_class = models.IntegerField(verbose_name="Clase Empleado", choices=EMPLOYEE_CLASS,default=EMPLOYEE_CLASS[1][0])
    type_regime = models.ForeignKey(TypeRegime,on_delete=models.PROTECT,verbose_name='Tipo Regimen', blank=True, null=True)
    type_employee = models.ForeignKey(TypeEmployee,on_delete=models.PROTECT,verbose_name='Tipo Empleado', blank=True, null=True)
    type_contract = models.ForeignKey(TypeContract,on_delete=models.PROTECT,verbose_name='Tipo Contrato', blank=True, null=True)
    number_iess = models.CharField(verbose_name="Numero Iess", max_length=50,blank=True,null=True)
    date_membership = models.DateField(verbose_name="Fecha Iess",default=now)
    sueldo = models.DecimalField(verbose_name="Sueldo", decimal_places=2,max_digits=18)
    rol= models.BooleanField(verbose_name="Pago Rol", default=True)
    frequency_rol = models.IntegerField(verbose_name="Frecuencia Rol", choices=FREQUENCY_ROL,default=FREQUENCY_ROL[1][0],blank=True,null=True)
    #jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE)
    active = models.BooleanField(verbose_name="Activo", default=False)
  
    def get_full_name(self):
        return f'{self.last_name} {self.firts_name}'

    def get_model_dict(self):
        item = model_to_dict(self)
        item['image_url'] = self.get_image_url()
        return item

    def get_image_url(self):
        return utils.get_image(self.image)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ('-id',)
        
#modelo cargafamiliar
class Dependent(ModelBase):
    
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,verbose_name='Empleado Responsable')
    kinship= models.ForeignKey(KinshipType,on_delete=models.PROTECT,verbose_name='Parentesco')
    marital_status= models.ForeignKey(MaritalStatus,on_delete=models.PROTECT,verbose_name='Estado Civil')
    name = models.CharField(
        verbose_name='Nombres',
        max_length=100,
    )
    lastname = models.CharField(
        verbose_name='Apellidos',
        max_length=100,
    )
    fecha_nacimiento = models.DateTimeField(verbose_name='Fecha de nacimiento', default=now)
    country = models.ForeignKey(Country,on_delete=models.PROTECT,verbose_name='Pais')
    city = models.ForeignKey(City,on_delete=models.PROTECT,verbose_name='Ciudad')
    image = models.ImageField(
        verbose_name='Foto',
        upload_to='dependents',
        max_length=500,
        null=True,
        blank=True
    )
    direction = models.CharField("Dirección", max_length=100)
    phone = models.CharField("Teléfono", max_length=50)
    cedula= models.CharField("Cedula", max_length=50, unique=True)

    def get_model_dict(self):
        item = model_to_dict(self)
        item['image_url'] = self.get_image_url()
        return item

    def get_image_url(self):
        return utils.get_image(self.image)

    def __str__(self):
        return f'{self.name} {self.lastname}'

    class Meta:
        verbose_name = 'Carga Familiar'
        verbose_name_plural = 'Cargas Familiares'
        ordering = ('-id',)
        
class Medicaldata(ModelBase):
    empleado = models.ForeignKey(Employee,verbose_name='Empleado', on_delete=models.CASCADE)
    tipo_sangre = models.CharField(verbose_name='Tipo de sangre', max_length=10)
    alergias = models.TextField(verbose_name='Alergias', blank=True)
    enfermedades = models.TextField(verbose_name='Enfermedades',blank=True)
    peso = models.CharField(verbose_name='Peso(kg)',max_length=10)
    altura = models.CharField(verbose_name='Altura(m)',max_length=10)
    Ultima_revision = models.DateField(verbose_name='Ultima revision', default=now)
    discapacidad = models.BooleanField(verbose_name="Discapacidad", default=False)
    des_discapacidad = models.TextField(verbose_name='descripcion de Discapacidad',blank=True)

    def __str__(self):
        return f'{self.empleado.firts_name} {self.empleado.last_name}'

    class Meta:
        verbose_name = 'Dato Medico'
        verbose_name_plural = 'Dato Medicos'
        ordering = ('-id',)