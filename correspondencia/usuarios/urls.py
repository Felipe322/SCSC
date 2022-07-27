from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginUsuario.as_view(), name="usuarios"),
    path('usuarios/', views.usuarios, name="usuarios")
]
