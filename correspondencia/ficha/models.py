from django.db import models
from datetime import datetime

class Ficha(models.Model):
    id_ficha = models.CharField(max_length=10, primary_key=True, verbose_name="No. de Ficha")
    fecha = models.TimeField(auto_now_add=True, verbose_name="Fecha")
    num_documento = models.CharField(max_length=200, verbose_name="Número del Documento")
    fecha_documento = models.TimeField(default=datetime.now, verbose_name="Fecha del Documento")
    dependencia = models.ForeignKey("ficha.Dependencia", on_delete=models.CASCADE, verbose_name="Dependencia Procedente")
    nombre_firma = models.CharField(max_length=350, verbose_name="Nombre de quien firma")
    asunto = models.CharField(max_length=500, verbose_name="Asunto")
    area_turnada = models.ForeignKey("ficha.Area", on_delete=models.CASCADE, verbose_name="Area a la que se turna")
    instruccion = models.TextField(max_length=800, verbose_name="Instrucción")
    resolucion = models.TextField(max_length=800, verbose_name="Resolución")
    fecha_recibido = models.TimeField(default=datetime.now, verbose_name="Fecha y firma de quien recibe")

    def __str__(self):
        return self.num_documento

class Dependencia(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    siglas = models.CharField(max_length=20, verbose_name="Siglas")
    #encargado.

    def __str__(self):
        return self.nombre + ' (' + self.siglas +')'

class Area(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    siglas = models.CharField(max_length=20, verbose_name="Siglas")
    encargado = models.CharField(max_length=80, verbose_name="Encargado")
    puesto = models.CharField(max_length=100, verbose_name="Puesto")

    def __str__(self):
        return self.nombre + ' (' + self.siglas +')'
