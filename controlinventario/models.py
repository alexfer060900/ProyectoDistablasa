from django.db import models
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage

class Producto(models.Model):
    codigo = models.CharField(max_length=30, unique=True, blank=True)
    nombre = models.CharField(max_length=100)
    familia = models.CharField(max_length=100)
    largo = models.DecimalField(max_digits=5, decimal_places=2)
    ancho = models.DecimalField(max_digits=5, decimal_places=2)
    grosor = models.DecimalField(max_digits=5, decimal_places=2)
    existencias = models.PositiveIntegerField()
    imagen = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = f"{self.nombre[0].lower()}{str(Producto.objects.count() + 1).zfill(4)}{int(self.grosor)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.codigo}"


class HistorialCambios(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=50)  
    producto = models.CharField(max_length=100)
    motivo = models.TextField(blank=True, null=True)  
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.producto} - {self.motivo} - {self.fecha_hora}"
