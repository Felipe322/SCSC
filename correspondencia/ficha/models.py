from django.db import models
from datetime import datetime

class Ficha(models.Model):

    readonly_fields=('resolucion')

    PRIORIDAD_CHOICES = (("1", "Alta"),("2", "Media"),("3", "Baja"))
    ESTATUS_CHOICES = (("1", "Atendido"),("2", "Sin atender"))

    id_ficha = models.IntegerField(primary_key=True, verbose_name="No. de Ficha")
    fecha = models.DateField(default=datetime.now, verbose_name="Fecha")
    num_documento = models.CharField(max_length=200, verbose_name="Número del Documento")
    fecha_documento = models.DateField(default=datetime.now, verbose_name="Fecha del Documento")
    dependencia = models.ForeignKey("ficha.Dependencia", on_delete=models.CASCADE, verbose_name="Dependencia Procedente")
    nombre_firma = models.CharField(max_length=350, verbose_name="Nombre de quien firma")
    asunto = models.CharField(max_length=500, verbose_name="Asunto")
    area_turnada = models.ForeignKey("ficha.Area", on_delete=models.CASCADE, verbose_name="Area a la que se turna")
    instruccion = models.TextField(max_length=800, verbose_name="Instrucción")
    prioridad = models.CharField(max_length=6, choices=PRIORIDAD_CHOICES, verbose_name="Prioridad de la ficha", default="3")
    resolucion = models.TextField(max_length=800, verbose_name="Resolución", default="Sin resolución")
    fecha_recibido = models.DateField(default=datetime.now, verbose_name="Fecha de ficha firmada")
    estatus = models.CharField(max_length=12, choices=ESTATUS_CHOICES, default="2")
    pdf_dependencia = models.FileField(upload_to='pdfs/', verbose_name="PDF de la dependencia", blank=True, null=True)

    def asunto_muestra(self):
        asunto_temp = self.asunto
        if len(asunto_temp) > 20:
            asunto_temp = asunto_temp[0:20] + '...'
        return asunto_temp

    def __str__(self):
        return str(self.id_ficha)

class Dependencia(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre", unique=True)
    siglas = models.CharField(max_length=20, verbose_name="Siglas", unique=True)

    def __str__(self):
        return self.nombre + ' (' + self.siglas +')'

class Area(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre", unique=True)
    siglas = models.CharField(max_length=20, verbose_name="Siglas", unique=True)

    def __str__(self):
        return self.nombre 