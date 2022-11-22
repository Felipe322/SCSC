from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from ficha.views import ajustes
from usuarios.forms import AjustesForm, UsuarioForm
from usuarios.models import Ajustes, Usuario

from .token import token_activacion


class Login(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm

#CRUD de usuarios.
class UsuarioLista(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'usuarios.view_usuario'
    model = Usuario
    paginate_by = 5
    template_name = 'usuarios/lista_usuarios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context

class UsuarioCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('usuarios.view_usuario', 'usuarios.add_usuario')
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/crear_usuarios.html'
    success_url = reverse_lazy('usuarios:lista')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.is_staff = True
        user.save()

        ajustes = Ajustes.objects.filter()[:1].get()
        logo_email = ajustes.logo_email

        dominio = get_current_site(self.request)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = token_activacion.make_token(user)
        mensaje = render_to_string('confirmar_cuenta.html',
            {
                'usuario': user,
                'dominio': dominio,
                'uid': uid,
                'token': token,
                'logo_email': logo_email
            }
        )
        asunto = 'Activación de cuenta'
        to = user.email
        email = EmailMessage(
            asunto,
            mensaje,
            to=[to]
        )
        email.content_subtype = 'html'
        email.send()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context

class UsuarioEditar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('usuarios.view_usuario', 'usuarios.change_usuario')
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/editar_usuarios.html'
    success_url = reverse_lazy('usuarios:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context

class UsuarioEliminar(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('usuarios.view_usuario', 'usuarios.delete_usuario')
    model = Usuario
    success_url = reverse_lazy('usuarios:lista')

class ActivarCuenta(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(kwargs['uid64'])
            token = kwargs['token']
            user = Usuario.objects.get(id=uid)
        except:
            user = None

        if user and token_activacion.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(self.request, 'Cuenta activada con éxito')
        else:
            messages.error(self.request, 'Token inválido, contacta al administrador')

        return redirect('login')

@login_required(login_url="login")
@permission_required(["usuarios.change_ajustes", "usuarios.delete_ajustes", "usuarios.view_ajustes", "usuarios.add_ajustes"])
def editar_ajustes(request, id):
    ajustes_elemento = get_object_or_404(Ajustes, id=id)
    form = AjustesForm(instance=ajustes_elemento)
    if request.method == 'POST':
        form = AjustesForm(request.POST, request.FILES, instance=ajustes_elemento)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    context.update(ajustes())
    return render(request, 'editar_ajustes.html', context)
