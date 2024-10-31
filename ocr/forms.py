from django import forms
from .models import ResultadosOCR, Categoria, Paginas
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget

# Formulario para el OCR
class OCRForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Muestra un calendario
        label="Fecha"
    )
    categoria = forms.ChoiceField(
        choices=Categoria.CATEGORIAS_CHOICES,
        label="Categoría",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ResultadosOCR
        fields = ['nombre_archivo', 'descripcion', 'npaginas', 'fecha', 'categoria']  # Incluye todos los campos necesarios

# Formulario para editar el texto extraído
class EditOCRForm(forms.Form):
    texto_extraido = forms.CharField(
        widget=CKEditorWidget(),
        label="Texto Extraído"
    )
