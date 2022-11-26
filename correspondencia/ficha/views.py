import io
import os.path

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

from usuarios.models import Ajustes, Usuario

from .forms import AreaForm, DependenciaForm, FichaForm, FichaUserForm
from .models import Area, Dependencia, Ficha

from .filters import FichaFilter, FichaFilterHome, FichaFilterUser


# Crea un Ajustes, solo se podrá modificar este.
def ajustes():

    if not Ajustes.objects.filter(id=1).exists():
        ajustes = Ajustes(titulo='Sistema de Control y Seguimiento de Correspondencias', subtitulo='Desarrollado por LABSOL')
        ajustes.save()

    ajustes = Ajustes.objects.filter()[:1].get()
    titulo = ajustes
    subtitulo = ajustes.subtitulo
    logo = ajustes.logo
    context = {'titulo':titulo, 'subtitulo':subtitulo, 'logo':logo}
    return context

@login_required(login_url="login")
def home(request):

    if request.user.is_superuser:
        fichas = Ficha.objects.all().order_by("-id_ficha").order_by("-estatus").order_by("prioridad")

        filtro = FichaFilterHome(request.GET, queryset=fichas)
        fichas = filtro.qs

        paginator = Paginator(fichas, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        try:
            fichas = paginator.page(page_number)
        except PageNotAnInteger:
            fichas = paginator.page(1)
        except EmptyPage:
            fichas = paginator.page(paginator.num_pages)
        context = {'fichas':fichas, 'page_obj':page_obj, 'filtro':filtro}
        context.update(ajustes())
        return render(request, 'home.html', context)
    else:
        usuario = Usuario.objects.get(username=request.user)
        area = Area.objects.get(nombre=usuario.area)
        fichas = Ficha.objects.filter(area_turnada_id=area.id).order_by("-id_ficha").order_by("estatus").order_by("prioridad")

        filtro = FichaFilterUser(request.GET, queryset=fichas)
        fichas = filtro.qs

        paginator = Paginator(fichas, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        try:
            fichas = paginator.page(page_number)
        except PageNotAnInteger:
            fichas = paginator.page(1)
        except EmptyPage:
            fichas = paginator.page(paginator.num_pages)
        context = {'fichas':fichas, 'page_obj':page_obj, 'filtro':filtro}
        context.update(ajustes())
        return render(request, 'home.html', context)

#CRUD de Ficha

# Muestra el listado de las Fichas en la BD.
@login_required(login_url="login")
@permission_required("ficha.views_ficha")
def lista(request):
    fichas = Ficha.objects.all().order_by("-id_ficha").order_by("estatus").order_by("prioridad")

    filtro = FichaFilter(request.GET, queryset=fichas)
    fichas = filtro.qs

    paginator = Paginator(fichas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'fichas':fichas, 'page_obj':page_obj, 'filtro':filtro}
    context.update(ajustes())
    return render(request, 'ficha/lista_fichas.html', context)

@login_required(login_url="login")
@permission_required(["ficha.views_ficha", "ficha.add_ficha"])
def crear(request):

    ultima_ficha = { "id_ficha": 1}
    if Ficha.objects.filter(id_ficha=1).exists():
        ultima_ficha = {
            "id_ficha": int(str(Ficha.objects.latest('id_ficha'))) + 1 
        }

    form = FichaForm(initial=ultima_ficha)
    
    if request.method == 'POST':

        form = FichaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            ## Enviar correo
            dominio = get_current_site(request)
            ficha = request.POST
            id_ficha = str(ficha['id_ficha'])
            ficha_fecha = ficha['fecha']
            ficha_asunto = ficha['asunto']
            ficha_instruccion = ficha['instruccion']
            dependencia = ficha['dependencia']
            area = ficha['area_turnada']
            usuario = Usuario.objects.get(area=area)
            mensaje = render_to_string('asignacion_ficha.html',
                {
                    'usuario': usuario,
                    'id_ficha': id_ficha,
                    'ficha_fecha': ficha_fecha,
                    'ficha_asunto': ficha_asunto,
                    'ficha_instruccion': ficha_instruccion,
                    'dependencia': dependencia,
                    'dominio' : dominio
                }
            )
            asunto = 'Nueva ficha asignada'
            to = usuario.email
            email = EmailMessage(
                asunto,
                mensaje,
                to=[to]
            )
            email.content_subtype = 'html'
            email.send()

            return redirect('home')
    context = {'form':form}
    context.update(ajustes())
    return render(request, 'ficha/crear_ficha.html', context)

@login_required(login_url="login")
def editar_ficha(request, pk):
    ficha = get_object_or_404(Ficha, id_ficha=pk)
    if request.user.is_superuser:
        form = FichaForm(instance=ficha)
        if request.method == 'POST':
            form = FichaForm(request.POST, instance=ficha)
            if form.is_valid():
                form.save()
                return redirect('lista')
    else:
        form = FichaUserForm(instance=ficha)
        if request.method == 'POST':
            form = FichaUserForm(request.POST, instance=ficha)    
            if form.is_valid():
                ficha.estatus = "1"
                ficha.save()
                request_ficha = request.POST
                id_ficha = str(request_ficha['id_ficha'])
                num_documento = request_ficha['num_documento']
                asunto_ficha = request_ficha['asunto']
                dominio = get_current_site(request)

                # Enviar correo de notificación de firmado.
                if request_ficha['resolucion'] != "" and request_ficha['resolucion'] != "Sin resolución" and request_ficha['fecha_recibido'] != None:
                    area = request_ficha['area_turnada']
                    usuario = Usuario.objects.get(area=area)
                    mensaje = render_to_string('ficha_recibida.html',
                        {
                            'usuario': usuario,
                            'dominio': dominio,
                            'num_documento': num_documento,
                            'asunto': asunto_ficha,
                            'id_ficha': id_ficha,
                        }
                    )
                    asunto = 'Se ha recibido la respuesta de la ficha ' + id_ficha
                    to = 'scsc.labsol@gmail.com' #Change that no static
                    email = EmailMessage(
                        asunto,
                        mensaje,
                        to=[to]
                    )
                    email.content_subtype = 'html'
                    email.send()
                form.save()
                return redirect('home')
    context = {'form': form }
    context.update(ajustes())
    return render(request, 'ficha/editar_ficha.html', context)



@login_required(login_url="login")
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

@login_required(login_url="login")
@permission_required(["ficha.views_ficha", "ficha.delete_ficha"])
def elimina_ficha(request, pk):
    ficha = get_object_or_404(Ficha, id_ficha=pk)
    ficha.delete()
    return redirect('lista')

# CRUD  de Area

class AreaList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'ficha.view_area'
    model = Area
    paginate_by = 5
    template_name = 'area/list_area.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context

class AreaCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('ficha.view_area', 'ficha.add_area')
    model = Area
    form_class = AreaForm
    template_name = 'area/crear_area.html'
    success_url = reverse_lazy('lista_area')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context

class AreaEditar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('ficha.view_area', 'ficha.change_area')
    model = Area
    form_class = AreaForm
    template_name = 'area/editar_area.html'
    success_url = reverse_lazy('lista_area')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context

@login_required(login_url="login")
@permission_required(["ficha.view_area", "ficha.delete_area"])
def elimina_area(request, pk):
    area = get_object_or_404(Area, id=pk)
    area.delete()
    return redirect('lista_area')


# CRUD  de dependencia

class DependenciaList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'ficha.view_dependencia'
    model = Dependencia
    paginate_by = 5
    template_name = 'dependencia/list_dependencia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context


class DependenciaCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('ficha.view_dependencia', 'ficha.add_dependencia')
    model = Dependencia
    form_class = DependenciaForm
    template_name = 'dependencia/crear_dependencia.html'
    success_url = reverse_lazy('lista_dependencia')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context


class DependenciaEditar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('ficha.view_dependencia', 'ficha.change_dependencia')
    model = Dependencia
    form_class = DependenciaForm
    template_name = 'dependencia/editar_dependencia.html'
    success_url = reverse_lazy('lista_dependencia')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(ajustes())
        return context

@login_required(login_url="login")
@permission_required(["ficha.view_dependencia", "ficha.delete_dependencia"])
def elimina_dependencia(request, pk):
    dependencia = get_object_or_404(Dependencia, id=pk)
    dependencia.delete()
    return redirect('lista_dependencia')


# Listado de Correspondencia anual.

@login_required(login_url="login")
@permission_required("ficha.view_dependencia")
def correspondencia(request):
    dependencias = Dependencia.objects.all()
    fichas = Ficha.objects.all()
    context = {'dependencias': dependencias, 'fichas':fichas}
    context.update(ajustes())
    return render(request, 'correspondencia/list_correspondencia.html', context)

@login_required(login_url="login")
@permission_required("ficha.view_dependencia")
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
