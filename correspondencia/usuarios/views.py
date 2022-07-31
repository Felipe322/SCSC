from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from ficha.views import ajustes
from usuarios.forms import AjustesForm, UsuarioForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from usuarios.models import Ajustes, Usuario


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
class UsuarioCrear(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/crear_usuarios.html'
    success_url = reverse_lazy('usuarios:lista')

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