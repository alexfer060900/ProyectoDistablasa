from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import ClienteRegistroForm
from controlinventario.models import Producto
from .models import Cliente
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404


# Registro de cliente
def registro_cliente(request):
    if request.method == 'POST':
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cliente.objects.create(
                user=user,
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                telefono=form.cleaned_data['telefono'],
                correo_electronico=form.cleaned_data['correo_electronico']
            )
            # Asignar al grupo Cliente
            group, created = Group.objects.get_or_create(name='Cliente')
            user.groups.add(group)
            login(request, user)
            return redirect('pagina_cliente')
    else:
        form = ClienteRegistroForm()
    return render(request, 'pages/registro.html', {'form': form})


# Inicio de sesión para Cliente
def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.groups.filter(name='Cliente').exists():
                login(request, user)
                return redirect('pagina_cliente')
            else:
                return render(
                    request,
                    'pages/iniciarsesion.html',
                    {'error': 'No tienes permisos para acceder como Cliente'}
                )
        else:
            return render(
                request,
                'pages/iniciarsesion.html',
                {'error': 'Credenciales incorrectas'}
            )
    return render(request, 'pages/iniciarsesion.html')


# Cerrar sesión para Cliente
def cerrar_sesion(request):
    logout(request)
    return redirect('pagina_cliente')  # Redirige a la Tienda Virtual con botones visibles


# Página principal de la tienda virtual
def pagina_cliente(request):
    productos = Producto.objects.all()
    return render(request, 'pages/tiendavirtual.html', {'productos': productos})


@login_required
def compra_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    descripcion = 'Madera premium, antiagua, larga durabilidad.'
    grosores = [2, 3, 5]

    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        grosor = request.POST.get('grosor', '2')
        
        # Validar si hay suficiente inventario
        if cantidad > producto.existencias:
            messages.error(request, 'No hay suficiente stock disponible.')
        else:
            # Restar del inventario
            producto.existencias -= cantidad
            producto.save()
            messages.success(request, f'Compra exitosa: {cantidad} unidades de {producto.nombre}.')
            return redirect('pagina_cliente')  # Redirigir a la tienda

    return render(request, 'pages/compra.html', {
        'producto': producto,
        'grosores': grosores,
        'descripcion': descripcion
    })