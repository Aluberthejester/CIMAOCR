from django.urls import path, include  # Importar las funciones necesarias
from . import views  # Importar las vistas
from django.conf.urls.static import static  # Para servir archivos estáticos
from django.conf import settings  # Para obtener configuraciones
from django.contrib.auth import views as auth_views  # Importar vistas de autenticación
from .views import CustomLoginView, welcome, logout_view

# Definir las URL de la aplicación
urlpatterns = [
    path('', views.home_redirect, name='home_redirect'),  # Redirige según autenticación
    path('welcome/', views.welcome, name='welcome'),  # Página de bienvenida
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Página de Login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Página de Logout
    path('ocr/', views.ocr_view, name='ocr'),  # Página de OCR
    path('403/', views.error_403_view, name='403'),  # Página principal
    path('home/', views.home, name='home'),  # Página principal
    path('busqueda_g/', views.busqueda_general, name='busqueda_g'),  # Busqueda general
    path('proformas/', views.proformas, name='proformas'),  # Página de Proformas
    path('informes/', views.informes, name='informes'),  # Página de Informes
    path('cartas_r/', views.cartas_r, name='cartas_r'),  # Página de cartas_r
    path('cartas_e/', views.cartas_e, name='cartas_e'),  # Página de cartas_e
    path('certificaciones/', views.certificaciones, name='certificaciones'),  # Página de certificaciones
    path('adquisiciones/', views.adquisiciones, name='adquisiciones'),  # Página de adquisiciones
    path('compras/', views.compras, name='compras'),  # Página de Informes
    path('miscelanea/', views.miscelanea, name='miscelanea'),  # Página de Informes
    #path('ocr/editar/<int:resultado_id>/<str:texto>/', views.editar_ocr, name='editar_ocr'),  # Editar OCR
    path('ocr/editar/<int:resultado_id>/', views.editar_ocr, name='editar_ocr'),
    path('ocr/ver/<int:resultado_id>/', views.ver_ocr, name='ver_ocr'),  # Ver OCR
    path('ckeditor/', include('ckeditor_uploader.urls')),  # URL para CKEditor
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Servir archivos estáticos en modo de desarrollo

handler403 = 'ocr.views.error_403_view'
