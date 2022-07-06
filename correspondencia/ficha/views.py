from multiprocessing import context
from django.shortcuts import render, redirect

from .forms import FichaForm
from .models import Ficha

# @login_required(login_url="home")
def home(request):
    fichas = Ficha.objects.all()
    context = {'fichas':fichas}
    return render(request, 'ficha/ficha.html', context)

# @login_required(login_url="home")
def crear(request):
    form = FichaForm()

    if request.method == 'POST':
        form = FichaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('crear_ficha')
    context = {'form':form}
    return render(request, 'ficha/post_ficha.html', context)
