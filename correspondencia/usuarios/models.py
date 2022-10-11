from django.contrib.auth.models import User
from django.db import models
from ficha.models import Area


class Usuario(User):
    foto = models.ImageField("Foto de perfil", blank=True, null=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name="Area")
    puesto = models.CharField(max_length=100, verbose_name="Puesto")

class Ajustes(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título")
    subtitulo = models.CharField(max_length=100, verbose_name="Subtitulo")
    logo = models.ImageField("Logo de institución",upload_to="logo/", blank=True, null=True)

    def subtitulo_to_str(self):
        return self.subtitulo

    def __str__(self):
        return self.titulo