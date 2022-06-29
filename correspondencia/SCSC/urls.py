from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ficha.urls')),
    path('usuarios/', include('usuarios.urls')),
]
