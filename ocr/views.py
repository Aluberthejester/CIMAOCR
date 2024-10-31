from django.shortcuts import render, redirect, get_object_or_404
from .models import ResultadosOCR, Paginas, Categoria  
from .forms import OCRForm, EditOCRForm
import pytesseract
from PIL import Image
from django.conf import settings
import os
import urllib.parse
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.utils.http import quote  # Importa la función quote para codificar el texto

# Redirige a la página de error 403 cuando el usuario no tiene autorización
def error_403_view(request, exception=None):
    return render(request, '403.html', status=403)

# Función para verificar si el usuario es gestor
def is_gestor(user):
    return user.groups.filter(name='Gestor').exists()

# Redirige a la página adecuada según si el usuario está autenticado
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('welcome')

# Renderiza la página de bienvenida
def welcome(request):
    return render(request, 'welcome.html')

# Vista de Login personalizada
class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

# Vista para Logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('welcome')

# Función para realizar el OCR en una imagen
def realizar_ocr(imagen):
    img = Image.open(imagen)
    texto = pytesseract.image_to_string(img)
    return texto

# Vista para manejar el proceso OCR
@login_required
#@user_passes_test(is_gestor, login_url='403')
def ocr_view(request):
    if request.method == 'POST':
        form = OCRForm(request.POST, request.FILES)
        if form.is_valid():
            resultado_ocr = form.save(commit=False)
            resultado_ocr.id_usuario = request.user
            resultado_ocr.save()

            categoria = form.cleaned_data['categoria']
            Categoria.objects.create(resultado=resultado_ocr, categoria=categoria)

            imagenes = request.FILES.getlist('imagenes')
            texto_concatenado = ""
            if imagenes:
                for imagen in imagenes:
                    Paginas.objects.create(resultado=resultado_ocr, imagen=imagen)
                    texto_extraido = realizar_ocr(imagen)
                    texto_concatenado += texto_extraido + "\n"
                resultado_ocr.texto_extraido = texto_concatenado
                resultado_ocr.save()

                # Usar quote para codificar el texto extraído
                texto_codificado = quote(texto_concatenado)

                # Redirigir a editar_ocr con resultado_id y texto codificado
                return redirect('editar_ocr', resultado_id=resultado_ocr.id)
    else:
        form = OCRForm()

    return render(request, 'ocr/ocr_form.html', {
        'form': form,
    })

# Vista para editar resultados OCR
@login_required
def editar_ocr(request, resultado_id):
    resultado = get_object_or_404(ResultadosOCR, id=resultado_id)
    texto_decodificado = resultado.texto_extraido  # Obtiene el texto directamente de la base de datos

    if request.method == 'POST':
        if 'nueva_imagen' in request.FILES:
            nueva_imagen = request.FILES['nueva_imagen']
            Paginas.objects.create(resultado=resultado, imagen=nueva_imagen)
            nuevo_texto_extraido = realizar_ocr(nueva_imagen)
            texto_decodificado += f"\n{nuevo_texto_extraido}"

            nombre_archivo_txt = f"{resultado.nombre_archivo}.txt"
            ruta_txt = os.path.join(settings.MEDIA_ROOT, 'textos', nombre_archivo_txt)
            with open(ruta_txt, 'w') as file:
                file.write(texto_decodificado)

            resultado.texto_extraido = texto_decodificado  # Guarda el texto actualizado
            resultado.save()
            return redirect('editar_ocr', resultado_id=resultado.id)
        else:
            form = EditOCRForm(request.POST)
            if form.is_valid():
                texto_modificado = form.cleaned_data.get('texto_extraido', '')
                resultado.texto_extraido = texto_modificado
                resultado.save()

                nombre_archivo_txt = f"{resultado.nombre_archivo}.txt"
                ruta_txt = os.path.join(settings.MEDIA_ROOT, 'textos', nombre_archivo_txt)
                with open(ruta_txt, 'w') as file:
                    file.write(texto_modificado)
                return redirect('ocr')
    else:
        form = EditOCRForm(initial={'texto_extraido': texto_decodificado})

    imagenes = Paginas.objects.filter(resultado=resultado)

    return render(request, 'ocr/editar_ocr.html', {
        'form': form,
        'resultado': resultado,
        'imagenes': imagenes,
    })

# Vista para ver resultados OCR
@login_required
@user_passes_test(is_gestor, login_url='403')
 # Redirige a 'home' si el usuario no tiene permiso
def ver_ocr(request, resultado_id):
    resultado = get_object_or_404(ResultadosOCR, id=resultado_id)
    imagenes = resultado.paginas.all()

    return render(request, 'ocr/ver_ocr.html', {
        'resultado': resultado,
        'imagenes': imagenes,
    })

# Vista de la página principal
@login_required
def home(request):
    return render(request, 'home.html')

# Vista de la página "Proformas"
@login_required
@user_passes_test(is_gestor, login_url='403')
 # Redirige a 'home' si el usuario no tiene permiso
def proformas(request):
    query = request.GET.get('q', '')
    resultados = ResultadosOCR.objects.filter(categorias__categoria='proforma')
    if query:
        resultados = resultados.filter(Q(nombre_archivo__icontains=query) | Q(texto_extraido__icontains=query))
    return render(request, 'proformas.html', {'resultados': resultados, 'query': query})

# Vista de la página "Informes"
@login_required
@user_passes_test(is_gestor, login_url='403')
 # Redirige a 'home' si el usuario no tiene permiso
def informes(request):
    query = request.GET.get('q', '')
    resultados = ResultadosOCR.objects.filter(categorias__categoria='informe')
    if query:
        resultados = resultados.filter(Q(nombre_archivo__icontains=query) | Q(texto_extraido__icontains=query))
    return render(request, 'informes.html', {'resultados': resultados, 'query': query})

# Vista de la página "Cartas Recibidas"
@login_required
@user_passes_test(is_gestor, login_url='403')
 # Redirige a 'home' si el usuario no tiene permiso
def cartas_r(request):
    query = request.GET.get('q', '')
    resultados = ResultadosOCR.objects.filter(categorias__categoria='carta_recibida')
    if query:
        resultados = resultados.filter(Q(nombre_archivo__icontains=query) | Q(texto_extraido__icontains=query))
    return render(request, 'cartas_r.html', {'resultados': resultados, 'query': query})

# Vista de la página "Cartas enviadas"
@login_required
@user_passes_test(is_gestor, login_url='403')
 # Redirige a 'home' si el usuario no tiene permiso
def cartas_e(request):
    query = request.GET.get('q', '')
    resultados = ResultadosOCR.objects.filter(categorias__categoria='carta_enviada')
    if query:
        resultados = resultados.filter(Q(nombre_archivo__icontains=query) | Q(texto_extraido__icontains=query))
    return render(request, 'cartas_e.html', {'resultados': resultados, 'query': query})

# Vista de la página "Certificaciones"
@login_required
@user_passes_test(is_gestor, login_url='403')
 # Redirige a 'home' si el usuario no tiene permiso
def certificaciones(request):
    query = request.GET.get('q', '')
    resultados = ResultadosOCR.objects.filter(categorias__categoria='certificacion')
    if query:
        resultados = resultados.filter(Q(nombre_archivo__icontains=query) | Q(texto_extraido__icontains=query))
    return render(request, 'certificaciones.html', {'resultados': resultados, 'query': query})

# Vista de la página "Adquisiciones"
@login_required
@user_passes_test(is_gestor, login_url='403')
 # Redirige a 'home' si el usuario no tiene permiso
def adquisiciones(request):
    query = request.GET.get('q', '')
    resultados = ResultadosOCR.objects.filter(categorias__categoria='adquisicion')
    if query:
        resultados = resultados.filter(Q(nombre_archivo__icontains=query) | Q(texto_extraido__icontains=query))
    return render(request, 'adquisiciones.html', {'resultados': resultados, 'query': query})

# Vista de la página "Compras"
@login_required
@user_passes_test(is_gestor, login_url='403')
 # Redirige a 'home' si el usuario no tiene permiso
def compras(request):
    query = request.GET.get('q', '')
    resultados = ResultadosOCR.objects.filter(categorias__categoria='compra')
    if query:
        resultados = resultados.filter(Q(nombre_archivo__icontains=query) | Q(texto_extraido__icontains=query))
    return render(request, 'compras.html', {'resultados': resultados, 'query': query})

# Vista de la página "Miscelanea"
@login_required
@user_passes_test(is_gestor, login_url='403')
 # Redirige a 'home' si el usuario no tiene permiso
def miscelanea(request):
    query = request.GET.get('q', '')
    resultados = ResultadosOCR.objects.filter(categorias__categoria='miscelanea')
    if query:
        resultados = resultados.filter(Q(nombre_archivo__icontains=query) | Q(texto_extraido__icontains=query))
    return render(request, 'miscelanea.html', {'resultados': resultados, 'query': query})

@login_required
def busqueda_general(request):
    query = request.GET.get('q', '')
    
    # Filtra si hay una consulta de búsqueda; de lo contrario, muestra todos los resultados
    if query:
        resultados = ResultadosOCR.objects.filter(
            Q(nombre_archivo__icontains=query) | Q(texto_extraido__icontains=query)
        )
    else:
        resultados = ResultadosOCR.objects.all()
        
    return render(request, 'busqueda_g.html', {
        'query': query,
        'resultados': resultados,
    })

