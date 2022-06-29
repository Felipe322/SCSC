from django.db import models
from datetime import datetime

class Ficha(models.Model):
    id_ficha = models.CharField(max_length=10, primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    num_documento = models.CharField(max_length=200)
    fecha_documento = models.DateTimeField(default=datetime.now)
    dependencia = models.ForeignKey("ficha.Dependencia", verbose_name="Dependencia", on_delete=models.CASCADE)
    nombre_firma = models.CharField(max_length=350)
    asunto = models.CharField(max_length=500)
    area_turnada = models.ForeignKey("ficha.Area", verbose_name="Area", on_delete=models.CASCADE)
    instruccion = models.TextField(max_length=800)
    resolucion = models.TextField(max_length=800)
    fecha_recibido = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.num_documento

class Dependencia(models.Model):
    nombre = models.CharField(max_length=200)
    siglas = models.CharField(max_length=20)
    #encargado.

    def __str__(self):
        return self.nombre + ' (' + self.siglas +')'

class Area(models.Model):
    nombre = models.CharField(max_length=200)
    siglas = models.CharField(max_length=20)
    encargado = models.CharField(max_length=80)
    puesto = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre + ' (' + self.siglas +')'
