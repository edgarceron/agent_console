from django.db import models

# Create your models here.
class DatosPersonales(models.Model):
    nombres = models.CharField(max_length=100, verbose_name="Nombres", null=False)
    primer_apellido = models.CharField(max_length=50, verbose_name="Primer Apellido", null=False)
    segundo_apellido = models.CharField(max_length=50, verbose_name="Segundo Apellido", null=False)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    tipo_documento = models.CharField(max_length=50, verbose_name="Tipo de documento", null=False)
    identificacion = models.CharField(max_length=50, verbose_name="Identificación", null=False)
    telefono = models.CharField(max_length=50, verbose_name="Teléfono", null=False)
    email = models.EmailField(max_length=100, verbose_name="Identificación", null=False)
    direccion = models.CharField(max_length=100, verbose_name="Dirección", null=True)
    departamento = models.CharField(max_length=100, verbose_name="Departamento", null=True)
    barrio = models.CharField(max_length=100, verbose_name="Barrio", null=True)
    municipio = models.CharField(max_length=100, verbose_name="Municipio", null=True)
    tipo_servicio = models.CharField(max_length=100, verbose_name="Tipo de servicio", null=True)

class Solicitud(models.Model):
    solicitante = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, null=False)
    fecha_recepcion = models.DateTimeField(verbose_name="Tipo de documento", null=False)
    empresa = models.CharField(max_length=100, verbose_name="Empresa que registra")
    quien_registra = models.CharField(max_length=100, verbose_name="Agente que registra")
    informacion = models.TextField(verbose_name="Información adicional")
    tipo_servicio = models.CharField(max_length=100, verbose_name="Tipo de servicio", null=False)
    motivo_llamada = models.CharField(max_length=100, verbose_name="Motivo llamada", null=False)

