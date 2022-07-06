from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('crear_ficha/', views.crear, name="crear_ficha")
]
