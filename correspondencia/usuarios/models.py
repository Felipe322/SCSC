from django.contrib.auth.models import User
from django.db import models
from ficha.models import Area


class Usuario(User):
    area = models.OneToOneField(Area, on_delete=models.CASCADE, verbose_name="Area")
    puesto = models.CharField(max_length=100, verbose_name="Puesto")

    def __str__(self):
        return self.last_name + ' ' + self.first_name

class Ajustes(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título")
    subtitulo = models.CharField(max_length=100, verbose_name="Subtitulo")
    logo = models.ImageField("Logo de institución", help_text="*Logotipos con altura de 120px y ancho de 300px*", upload_to="logo/", blank=True, null=True)
    logo_email = models.ImageField("Logo que se mostrará en correos", help_text="*Logotipos con altura de 120px y ancho de 300px*", upload_to="logo/", blank=True, null=True)

    def __str__(self):
        return self.titulo