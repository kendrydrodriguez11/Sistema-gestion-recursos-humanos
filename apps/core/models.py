import json
from django.db import models
from crum import get_current_user
from django.forms import model_to_dict
from rrhhs import utils

class ModelBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    created_by = models.CharField(max_length=100, blank=True,null=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True,null=True)
    update_by = models.CharField(max_length=100,blank=True,null=True,editable=False)

    @property
    def created_at_format(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def updated_at_format(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
      

    def save(self, *args, **kwargs):
        try:
            user = get_current_user()
            if self._state.adding:
                self.created_by = user.username
            else:
                self.update_by = user.username
        except:
            pass

        models.Model.save(self)

    class Meta:
        abstract = True

class Country(ModelBase):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    active = models.BooleanField(verbose_name='Activo', default=True)
  
    def __str__(self):
        return self.name

    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        ordering = ['-name']

class City(ModelBase):
    country = models.ForeignKey(Country,on_delete=models.PROTECT,verbose_name="Pais")
    name = models.CharField('Descripcion',max_length=100)
    active = models.BooleanField(verbose_name='Activo', default=True)
 
    def __str__(self):
        return self.name

    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['-name']

class Organization(ModelBase):
    name = models.CharField(
        verbose_name='Nombre de la organización',
        max_length=100,
        unique=True
    )
    country = models.ForeignKey(Country,on_delete=models.PROTECT,verbose_name='Pais')
    city = models.ForeignKey(City,on_delete=models.PROTECT,verbose_name='Ciudad')
    image = models.ImageField(
        verbose_name='Logo',
        upload_to='organization',
        max_length=500,
        null=True,
        blank=True
    )
    ruc = models.CharField("Ruc Empresa", max_length=15)
    direction = models.CharField("Dirección", max_length=100)
    phone = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    fax = models.CharField("Fax", max_length=50, blank=True, null=True)
    email = models.CharField("Correo", max_length=100)
    web = models.CharField("Página Web", max_length=100, blank=True, null=True)
    slogan = models.CharField("Eslogan", max_length=100, blank=True, null=True)
    ruc_representative = models.CharField(
        'Ruc Representante',
        max_length=15,
        blank=True,
        null=True
    )
    latitude = models.CharField("Latitud", max_length=100, blank=True, null=True)
    longitude = models.CharField("Longitud", max_length=100, blank=True, null=True)
    matriz = models.BooleanField(default=False)
    active = models.BooleanField(verbose_name='Activo', default=True)
 
    @staticmethod
    def get_organization_first():
        return Organization.objects.filter(matriz=True).order_by('id').first()

    # para trabajarlo como objeto en js
    def of_json_pure_to_dumps(self):
        return json.dumps(self.get_model_dict())

    def get_model_dict(self):
        item = model_to_dict(self)
        item['image_url'] = self.get_image_url()
        return item

    def get_image_url(self):
        return utils.get_image(self.image)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ('-id',)


