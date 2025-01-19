from django.urls import path
from . import views

urlpatterns = [
    # Inicio y Cierre de Sesión
    path('', views.inicio_sesion, name='login_bodeguero'),
    path('login/', views.inicio_sesion, name='login_bodeguero'),
    path('logout/', views.cerrar_sesion, name='logout_bodeguero'),
    
    # Gestión de Inventario
    path('productos/', views.listado_productos, name='listado_productos'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('historial/', views.historial_cambios, name='historial_cambios'),
]
