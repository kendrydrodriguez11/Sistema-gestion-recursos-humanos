from django.db import models
from crum import get_current_user
from django.forms import model_to_dict
from apps.core.models import ModelBase, Organization
from apps.personal_file.models import Employee
from django.core.validators import FileExtensionValidator
from django.shortcuts import get_object_or_404
from rrhhs import utils

class Supplier(ModelBase):
    name = models.CharField("Nombre", max_length=100)
    address = models.CharField("Dirección", max_length=100)
    phone = models.CharField("Telefono", max_length=20,blank=True,null=True)
    email = models.EmailField("Correo", blank=True,null=True)
    website = models.CharField("Pagina web", max_length=100,blank=True,null=True)
    description = models.TextField("Descripcion", blank=True,null=True)
    state = models.BooleanField("Activo", default=True)

    def __str__(self):
        return self.name

    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['name']
        ordering = ('-id',)


class Course(ModelBase):
    name = models.CharField("Nombre", max_length=100)
    description = models.TextField("Descripcion", blank=True,null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT,verbose_name='Proveedor')
    fecha_inicio = models.DateField("Fecha de inicio", blank=True,null=True)
    fecha_fin = models.DateField("Fecha de fin", blank=True,null=True)
    state = models.BooleanField("Activo", default=True)

    def __str__(self):
        return self.name

    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['name']
        ordering = ('-id',)
        permissions = (
            (
                "training_modify_supplier",
                f"Colocar proveedor {verbose_name}"
            ),
            (
                "training_modify_dates",
                f"Colocar fechas {verbose_name}"
            )
        )
        

class Application(ModelBase):
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,verbose_name='Empleado')
    course = models.ForeignKey(Course, on_delete=models.PROTECT,verbose_name='Curso')
    sucursal = models.ForeignKey(Organization,on_delete=models.PROTECT,verbose_name='Sucursal', blank=True, null=True)
    description = models.CharField("Descripcion", max_length=500)
    year = models.IntegerField(verbose_name="Año Curso")
    fecha_inicio = models.DateField("Fecha de inicio", blank=True,null=True)
    fecha_fin = models.DateField("Fecha de fin", blank=True,null=True)
    approved_boss = models.BooleanField("Aprobado jefe", default=False)
    approved_commission = models.BooleanField("Aprobado Comision", default=False)
    cost = models.DecimalField(verbose_name="Costo Curso", decimal_places=2,max_digits=18, null=True, blank=True)
    state = models.BooleanField("Activo", default=False)

    def __str__(self):
        return self.employee.get_full_name() + ' - ' + self.course.name

    def save(self, *args, **kwargs):
        self.sucursal = self.employee.sucursal
        self.year = self.course.fecha_inicio.year
        self.fecha_inicio = self.course.fecha_inicio
        self.fecha_fin = self.course.fecha_fin

        if self.approved_boss and self.approved_commission and self.cost is not None:
            self.state = True

            pdf = utils.generate_pdf(
                'applications/report.html',
                {
                    'employee': self.employee.get_full_name(),
                    'course': self.course.name,
                    'description': self.description,
                    'start_date': self.fecha_inicio,
                    'end_date': self.fecha_fin,
                    'sucursal': self.sucursal.name,
                },
                "applications/{}-{}-{}.pdf".format(self.employee.get_full_name(), self.course.name, self.year)
            )

            utils.send_email(
                self.employee.email,
                f'Solicitud del curso {self.course.name} aprobada',
                'Su solicitud de curso ha sido aprobada',
                pdf
            )
        super().save(*args, **kwargs)

    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        ordering = ('-id',)
        permissions = (
            (
                "application_approve_boss",
                f"Aprobar solicitud por jefe {verbose_name}"
            ),
            (
                "application_approve_commission",
                f"Aprobar solicitud por comision {verbose_name}"
            ),
            (
                "application_add_cost",
                f"Colocar costo de la solicitud {verbose_name}"
            )
        )

class Certificate(ModelBase):
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,verbose_name='Empleado')
    course = models.ForeignKey(Course, on_delete=models.PROTECT,verbose_name='Curso')
    note = models.IntegerField("Nota", blank=True)
    certificado_pdf = models.FileField(upload_to='certificados/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def __str__(self):
        return self.employee.get_full_name() + ' - ' + self.course.name

    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        current_user = get_current_user()
        if current_user and current_user.username is not None:
            employee = get_object_or_404(Employee, login=current_user.username)
            self.employee = employee
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'
        ordering = ('-id',)
        permissions = (
            (
                "certificate_view_pdf",
                f"Ver certificado {verbose_name}"
            ),
        )