from django import forms
import os
from django.conf import settings
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'familia', 'largo', 'ancho', 'grosor', 'existencias', 'imagen']
        labels = {
            'nombre': 'Nombre',
            'familia': 'Familia',
            'largo': 'Largo (m)',
            'ancho': 'Ancho (m)',
            'grosor': 'Grosor (mm)',
            'existencias': 'Existencias',
            'imagen': 'Imagen del producto',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'familia': forms.TextInput(attrs={'class': 'form-control'}),
            'largo': forms.NumberInput(attrs={'class': 'form-control'}),
            'ancho': forms.NumberInput(attrs={'class': 'form-control'}),
            'grosor': forms.NumberInput(attrs={'class': 'form-control'}),
            'existencias': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # Campo personalizado para seleccionar imágenes desde la carpeta static/imgProductos
    imagen = forms.ChoiceField(
        choices=[
            (f'imgProductos/{file}', file)  # Ruta relativa y nombre del archivo
            for file in os.listdir(os.path.join(settings.BASE_DIR, 'controlinventario/static/imgProductos'))
            if file.endswith(('.png', '.jpg', '.jpeg'))  # Solo incluye imágenes
        ],
        required=False,
        label="Seleccionar imagen",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'imagen-select'  # Añadimos un ID para facilitar el JavaScript
        })
    )
