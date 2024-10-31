"""
URL configuration for exampleocr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # Importar la administración de Django
from django.urls import path, include  # Importar las funciones de rutas
from django.views.generic import RedirectView  # Para redireccionar
from django.conf import settings  # Importar la configuración de Django
from django.conf.urls.static import static  # Para servir archivos estáticos
from django.conf.urls import handler403  # Importación para el manejo de errores 403

urlpatterns = [
    path('admin/', admin.site.urls),  # URL para acceder a la administración de Django
    path('ocr/', include('ocr.urls')),  # Incluir las URLs de la app OCR
    path('', RedirectView.as_view(url='/ocr/', permanent=True)),  # Redirigir la URL raíz a /ocr/
]

if settings.DEBUG:  # Solo en modo DEBUG
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Servir archivos multimedia
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Agregar esta línea al final de urls.py para la vista personalizada 403
handler403 = 'ocr.views.error_403_view'
