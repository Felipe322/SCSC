from django.urls import path
from . import views

urlpatterns = [
    path('', views.AreaList.as_view(), name="lista_area"),
    path('crear/', views.AreaCrear.as_view(), name="crear_area"),
    path('editar/<int:pk>', views.AreaEditar.as_view(), name='editar_area'),
    path('eliminar/<int:pk>', views.elimina_area, name='eliminar_area'),
]
