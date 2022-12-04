from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from usuarios.views import Login, info
from ficha.views import home, correspondencia, pdf_correspondencia
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login y Logout
    path('login/', Login.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),

    # Inicio
    path('', home, name="home"),

    # Fichas
    path('fichas/', include('ficha.urls_ficha')),

    # Areas
    path('areas/', include('ficha.urls_area')),

    # Dependencias
    path('dependencias/', include('ficha.urls_dependencia')),

    # Correspondencia
    path('correspondencia/', correspondencia, name="correspondencia"),
    path('correspondencia/pdf', pdf_correspondencia, name="pdf_correspondencia"),

    # Usuarios
    path('usuarios/', include('usuarios.urls')),

    # Password reset
    path('reset-password/',
        auth_views.PasswordResetView.as_view(
            template_name="usuarios/password_reset.html",
            html_email_template_name = 'usuarios/password_reset_email.html'
        ),
        name="reset_password",
    ),
    path('reset-password-sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="usuarios/password_reset_sent.html"
        ),
        name="password_reset_done"
    ),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="usuarios/password_reset_form.html"
        ),
        name="password_reset_confirm"
    ),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="usuarios/password_reset_done.html"
        ),
        name="password_reset_complete"
    ),

    # Info page
    path('info/', info, name='info'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)