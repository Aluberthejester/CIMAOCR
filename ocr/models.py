from django.db import models  # Importar el módulo de modelos de Django
from django.contrib.auth.models import User  # Importar el modelo de Usuario

# Modelo para almacenar los resultados de OCR

class ResultadosOCR(models.Model):
    nombre_archivo = models.CharField(max_length=255)
    texto_extraido = models.TextField(blank=True)
    descripcion = models.TextField(null=True, blank=True)
    npaginas = models.IntegerField()
    fecha_registro = models.DateField(auto_now_add=True)  # Generado automáticamente cuando se crea
    fecha = models.DateField(null=True, blank=True)  # Editable solo si se quiere
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'resultadosocr'

    def __str__(self):
        return self.nombre_archivo

# Modelo para almacenar las categorías
class Categoria(models.Model):
    CATEGORIAS_CHOICES = [
        ('informe', 'Informe'),
        ('carta_recibida', 'Carta Recibida'),
        ('carta_enviada', 'Carta Enviada'),
        ('proforma', 'Proforma'),
        ('adquisicion', 'Adquisición'),
        ('compra', 'Compra'),
        ('certificacion', 'Certificación'),
        ('miscelanea', 'Miscelánea'),
    ]
    resultado = models.ForeignKey(ResultadosOCR, related_name='categorias', on_delete=models.CASCADE)  # Relación con ResultadosOCR
    categoria = models.CharField(max_length=20, choices=CATEGORIAS_CHOICES)  # Campo de categoría con opciones

    class Meta:
        db_table = 'categoria'  # Define el nombre de la tabla

    def __str__(self):
        return f"{self.categoria} para {self.resultado.nombre_archivo}"  # Representación del objeto

# Modelo para almacenar las imágenes procesadas
class Paginas(models.Model):
    resultado = models.ForeignKey(ResultadosOCR, related_name='paginas', on_delete=models.CASCADE)  # Relación con ResultadosOCR
    imagen = models.ImageField(upload_to='paginas/')  # Campo para almacenar la imagen

    class Meta:
        db_table = 'paginasocr'  # Define el nombre de la tabla

    def __str__(self):
        return f"Página para {self.resultado.nombre_archivo}"  # Representación del objeto
