from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Cliente

class ClienteRegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=15)
    correo_electronico = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'nombre', 'apellido', 'telefono', 'correo_electronico']
