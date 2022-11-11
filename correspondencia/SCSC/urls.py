from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from usuarios.views import Login
from ficha.views import home, correspondencia, pdf_correspondencia
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('', home, name="home"),
    path('fichas/', include('ficha.urls_ficha')),
    path('areas/', include('ficha.urls_area')),
    path('dependencias/', include('ficha.urls_dependencia')),
    path('correspondencia/', correspondencia, name="correspondencia"),
    path('correspondencia/pdf', pdf_correspondencia, name="pdf_correspondencia"),
    path('usuarios/', include('usuarios.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)