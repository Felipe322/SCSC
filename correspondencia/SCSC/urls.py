from django.contrib import admin
from django.urls import path, include
from ficha.views import ajustes, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('fichas/', include('ficha.urls_ficha')),
    path('areas/', include('ficha.urls_area')),
    path('usuarios/', include('usuarios.urls')),
]
