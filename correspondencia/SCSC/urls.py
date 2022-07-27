from django.contrib import admin
from django.urls import path, include
from ficha.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('fichas/', include('ficha.urls')),
    path('', include('usuarios.urls')),
]
