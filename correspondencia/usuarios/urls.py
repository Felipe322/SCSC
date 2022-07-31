from django.urls import path
from . import views


app_name = 'usuarios'


urlpatterns = [
    path('', views.UsuarioLista.as_view(), name="lista"),
    path('crear/', views.UsuarioCrear.as_view(), name="crear"),
    path('editar/<int:pk>', views.UsuarioEditar.as_view(), name="editar"),
    path('eliminar/<int:pk>', views.UsuarioEliminar.as_view(), name='eliminar'),

    path('ajustes/<int:id>', views.editar_ajustes, name='ajustes'),
]
