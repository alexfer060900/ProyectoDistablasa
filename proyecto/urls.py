from django.contrib import admin
from django.urls import path, include  
from django.conf import settings  
from django.conf.urls.static import static
from clientes import views as clientes_views

urlpatterns = [
    # Administración
    path('admin/', admin.site.urls),
    
    # Página principal (Tienda Virtual)
    path('', clientes_views.pagina_cliente, name='pagina_cliente'),
    
    # Rutas de Control de Inventario (Bodeguero)
    path('inventario/', include('controlinventario.urls')),
    
    # Rutas de Cliente (Tienda Virtual)
    path('clientes/', include('clientes.urls')),
]

# Archivos estáticos y media en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
