from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_cliente, name='registro_cliente'),
    path('iniciarsesion/', views.inicio_sesion, name='inicio_sesion'),
    path('cerrarsesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('tienda/', views.pagina_cliente, name='pagina_cliente'),
    path('compra/<int:producto_id>/', views.compra_producto, name='compra_producto'),
]
