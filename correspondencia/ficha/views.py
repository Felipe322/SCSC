import io
import os.path
from django.http import FileResponse
from reportlab.pdfgen import canvas

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib.units import cm
from reportlab.lib import colors

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from usuarios.models import Ajustes
from .forms import AreaForm, FichaForm, DependenciaForm
from .models import Area, Ficha, Dependencia
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from reportlab.lib.pagesizes import letter, landscape


def ajustes():
    ajustes = Ajustes.objects.filter()[:1].get()
    titulo = ajustes
    subtitulo = ajustes.subtitulo
    logo = ajustes.logo
    context = {'titulo':titulo, 'subtitulo':subtitulo, 'logo':logo}
    return context

@login_required(login_url="login")
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
    context.update(ajustes())
    return render(request, 'home.html', context)

#CRUD de Ficha

# Muestra el listado de las Fichas en la BD.
@login_required(login_url="login")
def lista(request):
    fichas = Ficha.objects.all().order_by("-id_ficha") #TODO Order by time and priority.
    paginator = Paginator(fichas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'fichas':fichas, 'page_obj':page_obj}
    context.update(ajustes())
    return render(request, 'ficha/lista_fichas.html', context)

@login_required(login_url="login")
def crear(request):
    form = FichaForm()
    if request.method == 'POST':
        form = FichaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    context.update(ajustes())
    return render(request, 'ficha/crear_ficha.html', context)

@method_decorator(login_required, name='dispatch')
class FichaModificar(UpdateView):
    model = Ficha
    form_class = FichaForm
    template_name = 'ficha/editar_ficha.html'
    success_url = reverse_lazy('lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context

def fichaPDF(request, pk):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    ficha = get_object_or_404(Ficha, id_ficha=pk)
    
    # Create the PDF object, using the buffer as its "file."
    pdf = canvas.Canvas(buffer)

    #Establecemos el tamaño de letra en 13 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 13)
    #Dibujamos una cadena en la ubicación X,Y especificada
    pdf.drawString(100, 720, u"FICHA DE CONTROL Y SEGUIMIENTO DE CORRESPONDENCIA")

    # Agrega imagen a PDF
    imagen = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static/images/logo-cozcyt.png')
    pdf.drawImage(imagen, 50, 725, width=170, preserveAspectRatio=True, mask='auto')

    #Creamos una tupla de encabezados para neustra tabla
    encabezados = ('                                   ', 'No. de ficha: ' + str(ficha.id_ficha))

    #Creamos una lista de tuplas que van a contener la tabla
    fecha = (['Fecha: \n', str(ficha.fecha) + '\n'])
    num_doc = ('Numero de Documento: \n', str(ficha.num_documento) + '\n')
    fecha_doc = ('Fecha del Documento: \n', str(ficha.fecha_documento) + '\n')
    dependencia = ('Dependencia Procedente:\n\n ', str(ficha.dependencia) + '\n\n')
    firma = ('Nombre de quién firma:\n ', str(ficha.nombre_firma) + '\n')
    asunto = ('Asunto:\n\n\n\n ', str(ficha.asunto) + '\n\n\n\n')
    area = ('Area del COZCYT a la que se turna: \n\n\n', str(ficha.area_turnada)+ '\n\n\n')
    instruccion = ('Instrucción: \n\n\n\n', str(ficha.instruccion) + '\n\n\n\n')
    resolucion = ('Resolucion:\n\n\n\n ', str(ficha.resolucion) + '\n\n\n\n')
    fecha_firma = ('Fecha y Firma de quién recibe:\n\n\n\n ', str(ficha.fecha_recibido)+ '\n\n\n\n')

    detalles = [fecha] + [num_doc] + [fecha_doc] + [dependencia] + [firma] + [asunto] + [area] + [instruccion] + [resolucion] + [fecha_firma]

    #Establecemos el tamaño de cada una de las columnas de la tabla
    detalle_orden = Table([encabezados] + detalles, colWidths=[6.3 * cm, 10 * cm])
    #Aplicamos estilos a las celdas de la tabla
    detalle_orden.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN',(0,0),(3,0),'CENTER'),
            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.black), 
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1), 10)
        ]
    ))
    # Establecemos el tamaño de la hoja que ocupará la tabla 
    detalle_orden.wrapOn(pdf, 80, 500)
    #Definimos la coordenada donde se dibujará la tabla
    detalle_orden.drawOn(pdf, 69, 190)

    # Close the PDF object cleanly, and we're done.
    pdf.showPage()
    pdf.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename= f'ficha_{pk}.pdf')

@method_decorator(login_required, name='dispatch')
class FichaDetalle(DetailView):
    model = Ficha
    template_name = 'ficha/detalle_ficha.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context

@login_required(login_url="login")
def elimina_ficha(request, pk):
    ficha = get_object_or_404(Ficha, id_ficha=pk)
    ficha.delete()
    return redirect('lista')

# CRUD  de Area

@method_decorator(login_required, name='dispatch')
class AreaList(ListView):
    model = Area
    paginate_by = 5
    template_name = 'area/list_area.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context

@method_decorator(login_required, name='dispatch')
class AreaCrear(CreateView):
    model = Area
    form_class = AreaForm
    template_name = 'area/crear_area.html'
    success_url = reverse_lazy('lista_area')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context

@method_decorator(login_required, name='dispatch')
class AreaEditar(UpdateView):
    model = Area
    form_class = AreaForm
    template_name = 'area/editar_area.html'
    success_url = reverse_lazy('lista_area')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context

@login_required(login_url="login")
def elimina_area(request, pk):
    area = get_object_or_404(Area, id=pk)
    area.delete()
    return redirect('lista_area')

@method_decorator(login_required, name='dispatch')
class AreaDetalle(DetailView):
    model = Area
    template_name = 'area/detalle_area.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context


# CRUD  de dependencia

@method_decorator(login_required, name='dispatch')
class DependenciaList(ListView):
    model = Dependencia
    paginate_by = 5
    template_name = 'dependencia/list_dependencia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context


@method_decorator(login_required, name='dispatch')
class DependenciaCrear(CreateView):
    model = Dependencia
    form_class = DependenciaForm
    template_name = 'dependencia/crear_dependencia.html'
    success_url = reverse_lazy('lista_dependencia')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context


@method_decorator(login_required, name='dispatch')
class DependenciaEditar(UpdateView):
    model = Dependencia
    form_class = DependenciaForm
    template_name = 'dependencia/editar_dependencia.html'
    success_url = reverse_lazy('lista_dependencia')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context


@method_decorator(login_required, name='dispatch')
class DependenciaDetalle(DetailView):
    model = Dependencia
    template_name = 'dependencia/detalle_dependencia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context


@login_required(login_url="login")
def elimina_dependencia(request, pk):
    dependencia = get_object_or_404(Dependencia, id=pk)
    dependencia.delete()
    return redirect('lista_dependencia')


# Listado de Correspondencia anual.

@login_required(login_url="login")
def correspondencia(request):
    dependencias = Dependencia.objects.all()
    fichas = Ficha.objects.all()
    context = {'dependencias': dependencias, 'fichas':fichas}
    context.update(ajustes())
    return render(request, 'correspondencia/list_correspondencia.html', context)

def pdf_correspondencia(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # dependencias = Dependencia.objects.all()
    fichas = Ficha.objects.all()
    
    # Create the PDF object, using the buffer as its "file."
    pdf = canvas.Canvas(buffer, pagesize=landscape(letter))

    #Establecemos el tamaño de letra en 13 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 20)
    #Dibujamos una cadena en la ubicación X,Y especificada
    pdf.drawString(250, 520, u"CORRESPONDENCIA 2022")

    # Agrega imagen a PDF
    imagen = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static/images/logo-cozcyt.png')
    pdf.drawImage(imagen, 30, 500, width=200, preserveAspectRatio=True, mask='auto')


    #Creamos una tupla de encabezados para neustra tabla
    encabezados = [(dependencia.nombre) for dependencia in Dependencia.objects.all()]
    #Creamos una lista de tuplas que van a contener a las personas
    sub_encabezado = (("No. Ficha:") for dependencia in Dependencia.objects.all())
    encabezados = [(dependencia.nombre) for dependencia in Dependencia.objects.all()]

    detalles = [sub_encabezado]

    #TODO NOT COMPLETED
    fichas_dep = []
    for dependencia in Dependencia.objects.all():
        for ficha in Ficha.objects.all():
            if dependencia.pk == ficha.dependencia.pk:
                fichas_dep.append([ficha.id_ficha])
        detalles += (fichas_dep)
        fichas_dep = []
    
    #Establecemos el tamaño de cada una de las columnas de la tabla
    detalle_orden = Table([encabezados] + detalles, colWidths=[3 * cm])
    #Aplicamos estilos a las celdas de la tabla
    detalle_orden.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN',(0,0),(3,0),'CENTER'),
            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.black), 
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1), 10)
        ]
    ))
    # Establecemos el tamaño de la hoja que ocupará la tabla 
    detalle_orden.wrapOn(pdf, 60, 390)
    #Definimos la coordenada donde se dibujará la tabla
    detalle_orden.drawOn(pdf, 60, 390)

    # Close the PDF object cleanly, and we're done.
    pdf.showPage()
    pdf.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename= f'correspondencia_2022.pdf')
