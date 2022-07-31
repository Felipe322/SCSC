from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

from ficha.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('', home, name="home"),
    path('fichas/', include('ficha.urls_ficha')),
    path('areas/', include('ficha.urls_area')),
    path('usuarios/', include('usuarios.urls')),
]
