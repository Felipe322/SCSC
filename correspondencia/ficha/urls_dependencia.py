from django.urls import path
from . import views

urlpatterns = [
    path('', views.DependenciaList.as_view(), name="lista_dependencia"),
    path('crear/', views.DependenciaCrear.as_view(), name="crear_dependencia"),
    path('editar/<int:pk>', views.DependenciaEditar.as_view(), name='editar_dependencia'),
    path('eliminar/<int:pk>', views.elimina_dependencia, name='eliminar_dependencia'),
]