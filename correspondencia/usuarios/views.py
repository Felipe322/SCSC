from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from ficha.views import ajustes
from usuarios.forms import AjustesForm, UsuarioForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from usuarios.models import Ajustes, Usuario
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .token import token_activacion
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages


class Login(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm

#CRUD de usuarios.
@method_decorator(login_required, name='dispatch')
class UsuarioLista(ListView):
    model = Usuario
    paginate_by = 5
    template_name = 'usuarios/lista_usuarios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context

@method_decorator(login_required, name='dispatch')
class UsuarioCrear(LoginRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/crear_usuarios.html'
    success_url = reverse_lazy('usuarios:lista')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        dominio = get_current_site(self.request)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = token_activacion.make_token(user)
        mensaje = render_to_string('confirmar_cuenta.html',
            {
                'usuario': user,
                'dominio': dominio,
                'uid': uid,
                'token': token
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

@method_decorator(login_required, name='dispatch')
class UsuarioEditar(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/editar_usuarios.html'
    success_url = reverse_lazy('usuarios:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context

@method_decorator(login_required, name='dispatch')
class UsuarioEliminar(DeleteView):
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
def editar_ajustes(request, id):
    ajustes = get_object_or_404(Ajustes, id=id)
    form = AjustesForm(instance=ajustes)
    if request.method == 'POST':
        form = AjustesForm(request.POST, instance=ajustes)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    # context.update(ajustes())
    return render(request, 'editar_ajustes.html', context)
