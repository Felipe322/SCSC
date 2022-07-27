from django.shortcuts import render, redirect


from .forms import FichaForm
from .models import Ficha
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
# from django_weasyprint import WeasyTemplateResponseMixin
# from django_weasyprint.views import WeasyTemplateResponse

from django.conf import settings


# @login_required(login_url="home")
def home(request):
    fichas = Ficha.objects.all().order_by("-id_ficha") #TODO Order by time and priority.
    paginator = Paginator(fichas, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        fichas = paginator.page(page_number)
    except PageNotAnInteger:
        fichas = paginator.page(1)
    except EmptyPage:
        fichas = paginator.page(paginator.num_pages)
    context = {'fichas':fichas, 'page_obj':page_obj}
    return render(request, 'home.html', context)

# Muestra el listado de las Fichas en la BD.
def lista(request):
    fichas = Ficha.objects.all().order_by("-id_ficha") #TODO Order by time and priority.
    paginator = Paginator(fichas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'fichas':fichas, 'page_obj':page_obj}
    return render(request, 'ficha/lista_fichas.html', context)

# @login_required(login_url="home")
def crear(request):
    form = FichaForm()
    if request.method == 'POST':
        form = FichaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'ficha/crear_ficha.html', {'form':form})

class FichaModificar(UpdateView):
    model = Ficha
    form_class = FichaForm
    template_name = 'ficha/editar_ficha.html'
    success_url = reverse_lazy('lista')

# class FichaPDF(ListView):
#     model = Ficha
#     template_name = 'ficha/pdf_ficha.html'

# class VideojuegoPDF(WeasyTemplateResponseMixin, FichaPDF):
#     # pdf_stylesheets = [
#     #     settings.STATICFILES_DIRS[0] + 'css/portal.css',
#     # ]
#     pdf_attachment = False
#     pdf_filename = 'ficha.pdf'