from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.models import User, Group
from .models import Producto, HistorialCambios
from .forms import ProductoForm
import os


# 🔒 Función para verificar si el usuario es Bodeguero
def es_bodeguero(user):
    return user.groups.filter(name='Bodeguero').exists()


# 📜 Función para registrar cambios
def registrar_cambio(usuario, accion, producto, motivo=None):
    descripcion = f"{accion} - {producto}"
    if motivo:
        descripcion += f" (Motivo: {motivo})"
    HistorialCambios.objects.create(
        usuario=usuario,
        accion=accion,
        producto=producto,
        motivo=motivo,
    )


# 🔑 Inicio de sesión (Bodeguero)
def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and es_bodeguero(user):
            login(request, user)
            return redirect('listado_productos') 
        else:
            return render(
                request, 
                'pages/login.html', 
                {'error': 'Credenciales incorrectas o no tiene acceso como Bodeguero'}
            )
    return render(request, 'pages/login.html')


# 🔒 Cerrar sesión (Bodeguero)
@login_required
@user_passes_test(es_bodeguero)
def cerrar_sesion(request):
    logout(request)
    return redirect('login_bodeguero')  # Redirige al login de Bodeguero


# 📦 Listado de productos (solo Bodegueros)
@login_required
@user_passes_test(es_bodeguero)
def listado_productos(request):
    productos = Producto.objects.all()
    return render(request, 'pages/inventario.html', {
        'productos': productos,
        'seccion_activa': 'inventario',
    })


# ➕ Agregar producto (solo Bodegueros)
@login_required
@user_passes_test(es_bodeguero)
def agregar_producto(request):
    imagenes_disponibles = []
    img_path = 'controlinventario/static/imgProductos'
    
    if os.path.exists(img_path):
        imagenes_disponibles = [
            f'imgProductos/{file}'
            for file in os.listdir(img_path)
            if file.endswith(('.png', '.jpg', '.jpeg'))
        ]
    
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            registrar_cambio(request.user, 'Agregar', producto.nombre)
            return JsonResponse({'success': True, 'message': 'Producto agregado exitosamente.'})
        else:
            return JsonResponse({'success': False, 'message': 'Error al agregar el producto. Verifica los datos.'})
    else:
        form = ProductoForm()
    
    return render(request, 'pages/inventario.html', {
        'form': form,
        'productos': Producto.objects.all(),
        'imagenes_disponibles': imagenes_disponibles,
        'seccion_activa': 'agregar_producto',
    })


# ✏️ Editar producto (solo Bodegueros)
@login_required
@user_passes_test(es_bodeguero)
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    imagenes_disponibles = []
    img_path = 'controlinventario/static/imgProductos'
    
    if os.path.exists(img_path):
        imagenes_disponibles = [
            f'imgProductos/{file}'
            for file in os.listdir(img_path)
            if file.endswith(('.png', '.jpg', '.jpeg'))
        ]
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        motivo = request.POST.get('motivo', '').strip()
        if form.is_valid() and motivo:
            form.save()
            registrar_cambio(request.user, 'Editar', producto.nombre, motivo)
            return JsonResponse({'success': True, 'message': f'Producto "{producto.nombre}" editado. Motivo: {motivo}'})
        else:
            return JsonResponse({'success': False, 'message': 'Error al editar el producto. Motivo requerido.'})
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'pages/inventario.html', {
        'form': form,
        'producto': producto,
        'imagenes_disponibles': imagenes_disponibles,
        'seccion_activa': 'editar_producto',
    })


# 🗑️ Eliminar producto (solo Bodegueros)
@login_required
@user_passes_test(es_bodeguero)
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        motivo = request.POST.get('motivo', '').strip()
        if motivo:
            registrar_cambio(request.user, 'Eliminar', producto.nombre, motivo)
            producto.delete()
            return JsonResponse({'success': True, 'message': f'Producto "{producto.nombre}" eliminado. Motivo: {motivo}'})
        else:
            return JsonResponse({'success': False, 'message': 'Motivo requerido para eliminar el producto.'})
    
    return render(request, 'pages/inventario.html', {
        'producto': producto,
        'seccion_activa': 'eliminar_producto',
    })


# 📜 Historial de cambios (solo Bodegueros)
@login_required
@user_passes_test(es_bodeguero)
def historial_cambios(request):
    cambios = HistorialCambios.objects.all().order_by('-fecha_hora')
    return render(request, 'pages/inventario.html', {
        'cambios': cambios,
        'seccion_activa': 'historial_cambios',
    })
