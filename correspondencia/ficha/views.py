from django.shortcuts import render

from .models import Ficha

def home(request):
    fichas = Ficha.objects.all()
    context = {'fichas':fichas}
    return render(request, 'ficha/ficha.html', context)