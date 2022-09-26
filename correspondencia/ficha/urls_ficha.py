from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name="lista"),
    path('crear', views.crear, name="crear"),
    path('editar/<str:pk>', views.FichaModificar.as_view(), name="editar"),
    path('eliminar/<str:pk>', views.elimina_ficha, name='eliminar'),
    path('pdf/<str:pk>', views.fichaPDF, name='pdf'),
]
