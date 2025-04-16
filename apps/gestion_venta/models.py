from django.db import models
from django.forms import model_to_dict
from datetime import date
from rrhhs import utils
from django.conf import settings

class Categoria(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    description = models.TextField(verbose_name="Descripción")
    state = models.BooleanField(verbose_name = 'Activo', default=True)
    def __str__(self):
        return self.name
    
    def get_model_to_dict(self):
        item= model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural ='Categorias'
        ordering =['-name']


class Producto(models.Model):
    name = models.CharField(verbose_name='Nombre de los productos', max_length=50, unique=True)
    description = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    stock = models.PositiveIntegerField(verbose_name='Stock disponible', default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL,  null=True, verbose_name='Categoría a la que pertenece')
    
    def __str__(self):
        return self.name
    
    def get_model_to_dict(self):
        item= model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural ='Productos'
        ordering =['-name']


class Cliente (models.Model): 
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    apellido = models.CharField(verbose_name='Apellido', max_length=50)
    correo = models.EmailField(verbose_name='Correo Electrónico', unique=True)
    direccion = models.CharField(verbose_name='Dirección', max_length=255, blank=True, null=True)
    telefono = models.CharField(verbose_name='Número de Teléfono', max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_full_name(self):
        return self.name + ' ' + self.apellido

    def get_model_to_dict(self):
        item= model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural ='Clientes'
        ordering =['-name']


class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL,  null=True, verbose_name='Cliente')
    fecha = models.DateField(verbose_name='Fecha de la factura', default=date.today)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    iva = models.IntegerField(verbose_name='Iva', default=12)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def __str__(self):
        return str(self.id)
    
    def get_model_to_dict(self):
        item= model_to_dict(self)
        return item
            
    def save(self, *args, **kwargs):
        super(Factura, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural ='Facturas'
        ordering =['-id']

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, verbose_name='Factura')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad', default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def __str__(self):
        return str(self.id)
    
    def get_model_to_dict(self):
        item= model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = 'Detalle de la factura'
        verbose_name_plural ='Detalles de la factura'
        ordering =['-id']