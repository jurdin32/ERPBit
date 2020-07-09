from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from CONFIGURACION.models import Permiso, Items
from CONFIGURACION.views import funciones_usuario
from INVENTARIO.models import Producto, Bodega, Categoria
from USERS.models import myUsuario


def ReporteProductos(request):
    user = myUsuario.objects.get(usuario= request.user)
    permiso = Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario':request.user,
        'empresa': user.empresa,
        'permisos':permiso,
        'funciones': funciones_usuario(permiso),
        'items': Items.objects.all().order_by('prioridad'),
        'bodegas': Bodega.objects.filter(empresa=user.empresa),
        'categorias':Categoria.objects.filter(empresa=user.empresa),

    }
    return render(request, 'Reportes/reporteProductos.html', contexto)


def ConsulatProductos(request):
    user = myUsuario.objects.get(usuario=request.user)
    if request.POST:
        print(request.POST)
        bodega = request.POST['bodega']
        categoria = request.POST['categoria']
        fecha1 = request.POST['fecha1']
        fecha2 = request.POST['fecha2']

        if bodega == Bodega.objects.filter(empresa=user.empresa, id=bodega):
           producto = Producto.objects.filter(bodega_id=bodega, categoria_id= categoria)
           print(producto)

    return HttpResponse("No hay consulta")
