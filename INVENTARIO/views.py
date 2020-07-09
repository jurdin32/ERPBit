# -*- coding: utf-8 -*-
from http.client import HTTPResponse

from babel.dates import parse_date
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date



# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from CONFIGURACION.models import *
from CONFIGURACION.views import funciones_usuario
from DOCUMENTOS_ELECTRONICOS.models import Tarifas, DatosDocumentos
from INVENTARIO.models import *
from INVENTARIO.reportes import *
import time

from USERS.models import myUsuario


def ProductoView(request):
    usuario=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=usuario.grupo)
    contexto={
        'empresa':usuario.empresa,
        'usuario': request.user,
        'productos':Producto.objects.filter(empresa=usuario.empresa,tipo='PRODUCTO').order_by("-id"),
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': usuario.is_admin,

    }
    return render(request, 'Inventario/productos.html',contexto)

def RegistroProductosView(request):
    mensaje=""
    user = myUsuario.objects.get(usuario=request.user)
    tarifas = Tarifas.objects.filter(activo=True,usado_en_retencion=False)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    detalles=None
    if request.POST:
        producto=Producto(empresa=user.empresa,nombre=request.POST['nombre'].upper(),codigoBarra=request.POST['codigo'],peso=request.POST['peso'],
                          medida=request.POST['medida'],categoria_id=request.POST['categoria'],bodega_id=request.POST['bodega'],
                          estado=True,usuario=request.user.username,marca_id=request.POST['marca'],)
        producto.save()
        producto.cod_referencia=producto.categoria.categoria[0:3].upper()+"-"+str(str.zfill(str(producto.id),4))
        producto.save()
        try:
            print(request.POST['codigoIVA'],request.POST['codigoICE'],request.POST['codigoIBRPNR'])
            detalleProveedor = DetalleProProveedor()

            detalleProveedor.codigoIVA = request.POST['codigoIVA']
            detalleProveedor.codigoICE = request.POST['codigoICE']
            detalleProveedor.codigoIRBPNR = request.POST['codigoIBRPNR']
            detalleProveedor.producto = producto
            detalleProveedor.proveedor_id = request.POST['proveedor']
            detalleProveedor.precioProveedor = float(str(request.POST['precio']).replace(",", "."))
            detalleProveedor.porcentajeIVA=float(str(request.POST['porcentajeiva']).replace(",", "."))
            detalleProveedor.iva = float(str(request.POST['iva']).replace(",", "."))
            detalleProveedor.porcentajeICE = float(str(request.POST['porcentajeice']).replace(",", "."))
            detalleProveedor.ice=float(str(request.POST['ice']).replace(",", "."))
            detalleProveedor.porcentajeIRBPNR=float(str(request.POST['porcentajeirbpnr']).replace(",", "."))
            detalleProveedor.irbpnr=float(str(request.POST['irbpnr']).replace(",", "."))
            detalleProveedor.total = float(str(request.POST['total']).replace(",", "."))
            detalleProveedor.stockmax = float(str(request.POST['stockmax']))
            detalleProveedor.stockmin = float(str(request.POST['stockmin']))
            detalleProveedor.porcentajeGanancia = float(str(request.POST['porcentaje']).replace(",", "."))
            detalleProveedor.recargo = float(str(request.POST['recargo']).replace(",", "."))
            detalleProveedor.pvp = float(str(request.POST['nprecio']).replace(",", "."))
            detalleProveedor.ivapvp = float(str(request.POST['niva']).replace(",", "."))
            detalleProveedor.icepvp = float(str(request.POST['nice']).replace(",", "."))
            detalleProveedor.totalpvp = float(str(request.POST['ntotal']).replace(",", "."))
            detalleProveedor.save()
            print("no hay datos en el detalle, crearemos uno nuevo")
        except Exception as error:
            print(error)
        mensaje="El producto se ha creado con exito."
    contexto = {
        'usuario':request.user,
        'categorias':Categoria.objects.filter(estado=True,empresa=user.empresa),
        'bodegas':Bodega.objects.filter(estado=True,empresa=user.empresa),
        'proveedores':Proveedor.objects.filter(estado=True,empresa=user.empresa),
        'marcas':Marcas.objects.filter(estado=True,empresa=user.empresa),
        'ivas': tarifas.filter(impuesto__nombre="IVA").order_by('-porcentaje'),
        'irbpnr': tarifas.filter(impuesto__nombre="IRBPNR").order_by('-porcentaje'),
        'ices': tarifas.filter(impuesto__nombre="ICE").order_by('porcentaje'),
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request,'Inventario/registroProductos.html',contexto)

def ProductoEditarView(request,id,idDet):
    producto=Producto.objects.get(id=id)
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    tarifas = Tarifas.objects.filter(activo=True,usado_en_retencion=False)
    mensaje=""
    det = None
    if request.POST:
        producto.nombre=request.POST['nombre'].upper()
        producto.codigoBarra=request.POST['codigo']
        producto.peso=request.POST['peso'].upper()
        producto.medida=request.POST['medida'].upper()
        producto.categoria_id = request.POST['categoria']
        producto.bodega_id = request.POST['bodega']
        producto.marca_id=request.POST['marca']
        if int(request.POST['estado']) == 1:
            producto.estado = True
        else:
            producto.estado=False
        producto.save()
        if idDet>0 and int(request.POST['proveedor'])>0:
            detalleProveedor=DetalleProProveedor.objects.get(id=idDet)
            detalleProveedor.proveedor_id = request.POST['proveedor']
            detalleProveedor.precioProveedor = float(str(request.POST['precio']).replace(",", "."))
            detalleProveedor.porcentajeIVA = float(str(request.POST['porcentajeiva']).replace(",", "."))
            detalleProveedor.iva = float(str(request.POST['iva']).replace(",", "."))
            detalleProveedor.porcentajeICE = float(str(request.POST['porcentajeice']).replace(",", "."))
            detalleProveedor.ice = float(str(request.POST['ice']).replace(",", "."))
            detalleProveedor.porcentajeIRBPNR = float(str(request.POST['porcentajeirbpnr']).replace(",", "."))
            detalleProveedor.irbpnr = float(str(request.POST['irbpnr']).replace(",", "."))
            detalleProveedor.total = float(str(request.POST['total']).replace(",", "."))
            detalleProveedor.stockmax = float(str(request.POST['stockmax']))
            detalleProveedor.stockmin = float(str(request.POST['stockmin']))
            detalleProveedor.porcentajeGanancia = float(str(request.POST['porcentaje']).replace(",", "."))
            detalleProveedor.recargo = float(str(request.POST['recargo']).replace(",", "."))
            detalleProveedor.pvp = float(str(request.POST['nprecio']).replace(",", "."))
            detalleProveedor.ivapvp = float(str(request.POST['niva']).replace(",", "."))
            detalleProveedor.icepvp = float(str(request.POST['nice']).replace(",", "."))
            detalleProveedor.totalpvp = float(str(request.POST['ntotal']).replace(",", "."))
            detalleProveedor.codigoIVA = request.POST['codigoIVA']
            detalleProveedor.codigoICE = request.POST['codigoICE']
            detalleProveedor.codigoIRBPNR = request.POST['codigoIBRPNR']
            detalleProveedor.save()
            det=detalleProveedor
            print("actualizar detalles")
        else:
            if int(request.POST['proveedor'])>0:
                detalleProveedor=DetalleProProveedor()
                detalleProveedor.producto_id=id
                detalleProveedor.proveedor_id = request.POST['proveedor']
                detalleProveedor.precioProveedor = float(str(request.POST['precio']).replace(",", "."))
                detalleProveedor.porcentajeIVA = float(str(request.POST['porcentajeiva']).replace(",", "."))
                detalleProveedor.iva = float(str(request.POST['iva']).replace(",", "."))
                detalleProveedor.porcentajeICE = float(str(request.POST['porcentajeice']).replace(",", "."))
                detalleProveedor.ice = float(str(request.POST['ice']).replace(",", "."))
                detalleProveedor.porcentajeIRBPNR = float(str(request.POST['porcentajeirbpnr']).replace(",", "."))
                detalleProveedor.irbpnr = float(str(request.POST['irbpnr']).replace(",", "."))
                detalleProveedor.total = float(str(request.POST['total']).replace(",", "."))
                detalleProveedor.porcentajeGanancia = float(str(request.POST['porcentaje']).replace(",", "."))
                detalleProveedor.recargo = float(str(request.POST['recargo']).replace(",", "."))
                detalleProveedor.pvp = float(str(request.POST['nprecio']).replace(",", "."))
                detalleProveedor.ivapvp = float(str(request.POST['niva']).replace(",", "."))
                detalleProveedor.icepvp = float(str(request.POST['nice']).replace(",", "."))
                detalleProveedor.totalpvp = float(str(request.POST['ntotal']).replace(",", "."))
                detalleProveedor.codigoIVA = request.POST['codigoIVA']
                detalleProveedor.codigoICE = request.POST['codigoICE']
                detalleProveedor.codigoIRBPNR = request.POST['codigoIBRPNR']
                detalleProveedor.save()
                det=detalleProveedor
                print("actualizar detalles")
                det = detalleProveedor
                print("no hay datos en el detalle, crearemos uno nuevo")
        mensaje = "El registro se ha modificado con exito..!!"
    if idDet>0:
        det=DetalleProProveedor.objects.get(id=idDet)
    contexto={
        'producto':producto,
        'categorias':Categoria.objects.filter(estado=True,empresa=user.empresa),
        'bodegas': Bodega.objects.filter(estado=True),
        'proveedores': Proveedor.objects.filter(estado=True,empresa=user.empresa),
        'detalle':DetalleProProveedor.objects.filter(producto_id=id).order_by('id'),
        'det':det,
        'marcas':Marcas.objects.filter(estado=True),
        'ivas': tarifas.filter(impuesto__nombre="IVA").order_by('-porcentaje'),
        'irbpnr': tarifas.filter(impuesto__nombre="IRBPNR").order_by('-porcentaje'),
        'ices': tarifas.filter(impuesto__nombre="ICE").order_by('porcentaje'),
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos':permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request,'Inventario/registroProductos.html',contexto)


def EliminarProductoView(request,id):
    usuario=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=usuario.grupo)
    producto=Producto.objects.get(id=id)
    producto.estado=False
    producto.save()
    mensaje="El registro fue desactivado..!!"
    contexto={
        'empresa':usuario.empresa,
        'usuario': request.user,
        'productos':Producto.objects.filter(empresa=usuario.empresa,tipo='PRODUCTO').order_by("-id"),
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'user2': usuario.is_admin,

    }
    return render(request, "Inventario/productos.html", contexto)

def EliminarDetalleProducto(request,id):
    det=DetalleProProveedor.objects.get(id=id)
    producto_id=det.producto_id
    det.delete()
    return HttpResponseRedirect('/inventario/producto/edit/'+str(producto_id)+'/0/')

def EliminarDetalleServicio(request,id):
    det=DetalleProProveedor.objects.get(id=id)
    producto_id=det.producto_id
    det.delete()
    return HttpResponseRedirect('/inventario/servicios/edit/'+str(producto_id)+'/0/')

def ServicioView(request):
    usuario=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=usuario.grupo)
    contexto={
        'empresa':usuario.empresa,
        'usuario': request.user,
        'productos':Producto.objects.filter(empresa=usuario.empresa,tipo='SERVICIO').order_by('nombre'),
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': usuario.is_admin,
    }
    return render(request, 'Inventario/servicios.html',contexto)


def registroServicios(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    tarifas = Tarifas.objects.filter(activo=True, usado_en_retencion=False)
    mensaje=error=""
    if request.POST:
        producto=Producto(empresa=user.empresa,
                          nombre=request.POST['nombre'].upper(),
                          categoria_id=request.POST['categoria'],
                          estado=True,
                          usuario=request.user.username,
                          tipo="SERVICIO")
        producto.save()
        producto.cod_referencia=producto.categoria.categoria[0:3].upper()+"-"+str(str.zfill(str(producto.id),4))
        producto.save()
        try:
            detalleProveedor = DetalleProProveedor()
            detalleProveedor.detalles=request.POST['detalle']
            detalleProveedor.codigoIVA = request.POST['codigoIVA']
            detalleProveedor.codigoICE = request.POST['codigoICE']
            detalleProveedor.codigoIRBPNR = request.POST['codigoIBRPNR']
            detalleProveedor.producto = producto
            detalleProveedor.proveedor_id = request.POST['proveedor']
            detalleProveedor.precioProveedor = float(str(request.POST['precio']).replace(",", "."))
            detalleProveedor.porcentajeIVA=float(str(request.POST['porcentajeiva']).replace(",", "."))
            detalleProveedor.iva = float(str(request.POST['iva']).replace(",", "."))
            detalleProveedor.porcentajeICE = float(str(request.POST['porcentajeice']).replace(",", "."))
            detalleProveedor.ice=float(str(request.POST['ice']).replace(",", "."))
            detalleProveedor.porcentajeIRBPNR=float(str(request.POST['porcentajeirbpnr']).replace(",", "."))
            detalleProveedor.irbpnr=float(str(request.POST['irbpnr']).replace(",", "."))
            detalleProveedor.total = float(str(request.POST['total']).replace(",", "."))
            detalleProveedor.porcentajeGanancia = float(str(request.POST['porcentaje']).replace(",", "."))
            detalleProveedor.recargo = float(str(request.POST['recargo']).replace(",", "."))
            detalleProveedor.pvp = float(str(request.POST['nprecio']).replace(",", "."))
            detalleProveedor.ivapvp = float(str(request.POST['niva']).replace(",", "."))
            detalleProveedor.icepvp = float(str(request.POST['nice']).replace(",", "."))
            detalleProveedor.totalpvp = float(str(request.POST['ntotal']).replace(",", "."))
            detalleProveedor.save()
            print("no hay datos en el detalle, crearemos uno nuevo")
        except Exception as error:
            print(error)
        mensaje = "El servicio fue creado con exito."
    contexto={
        'usuario':request.user,
        'categorias':Categoria.objects.filter(estado=True,empresa=user.empresa),
        'proveedores':Proveedor.objects.filter(estado=True,empresa=user.empresa),
        'ivas': tarifas.filter(impuesto__nombre="IVA").order_by('-porcentaje'),
        'irbpnr': tarifas.filter(impuesto__nombre="IRBPNR").order_by('-porcentaje'),
        'ices': tarifas.filter(impuesto__nombre="ICE").order_by('porcentaje'),
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'user2': user.is_admin,

    }
    return render(request, 'Inventario/registroServicios.html',contexto)

def ServicioEditarView(request,id,idDet):
    producto=Producto.objects.get(id=id)
    user = myUsuario.objects.get(usuario=request.user)
    tarifas = Tarifas.objects.filter(activo=True,usado_en_retencion=False)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    mensaje=""
    det = None
    if request.POST:
        producto.nombre=request.POST['nombre'].upper()
        producto.categoria_id = request.POST['categoria']
        if int(request.POST['estado']) == 1:
            producto.estado = True
        else:
            producto.estado=False
        producto.usuario=request.user.username
        producto.save()
        detalleProveedor=None
        if idDet>0 and int(request.POST['proveedor'])>0:
            detalleProveedor = DetalleProProveedor.objects.get(id=idDet)
            print("va a actualizar")
        elif int(request.POST['proveedor'])>0:
            detalleProveedor = DetalleProProveedor()
            print("va a crear un registro nuevo")
        try:
            detalleProveedor.producto = producto
            detalleProveedor.detalles = request.POST['detalle']
            detalleProveedor.proveedor_id = request.POST['proveedor']
            detalleProveedor.precioProveedor = float(str(request.POST['precio']).replace(",", "."))
            detalleProveedor.porcentajeIVA = float(str(request.POST['porcentajeiva']).replace(",", "."))
            detalleProveedor.iva = float(str(request.POST['iva']).replace(",", "."))
            detalleProveedor.porcentajeICE = float(str(request.POST['porcentajeice']).replace(",", "."))
            detalleProveedor.ice = float(str(request.POST['ice']).replace(",", "."))
            detalleProveedor.porcentajeIRBPNR = float(str(request.POST['porcentajeirbpnr']).replace(",", "."))
            detalleProveedor.irbpnr = float(str(request.POST['irbpnr']).replace(",", "."))
            detalleProveedor.total = float(str(request.POST['total']).replace(",", "."))
            detalleProveedor.porcentajeGanancia = float(str(request.POST['porcentaje']).replace(",", "."))
            detalleProveedor.recargo = float(str(request.POST['recargo']).replace(",", "."))
            detalleProveedor.pvp = float(str(request.POST['nprecio']).replace(",", "."))
            detalleProveedor.ivapvp = float(str(request.POST['niva']).replace(",", "."))
            detalleProveedor.icepvp = float(str(request.POST['nice']).replace(",", "."))
            detalleProveedor.totalpvp = float(str(request.POST['ntotal']).replace(",", "."))
            detalleProveedor.codigoIVA = request.POST['codigoIVA']
            detalleProveedor.codigoICE = request.POST['codigoICE']
            detalleProveedor.codigoIRBPNR = request.POST['codigoIBRPNR']
            detalleProveedor.save()
            det=detalleProveedor
        except Exception as error:
            print("error, el usuario olvido elegir el proveedor -:",error)
        mensaje="El Servicio se ha modificado correctamente..!!"

    if idDet>0:
        det=DetalleProProveedor.objects.get(id=idDet)
    contexto={
        'producto':producto,
        'categorias':Categoria.objects.filter(estado=True,empresa=user.empresa),
        'bodegas': Bodega.objects.filter(estado=True),
        'proveedores': Proveedor.objects.filter(estado=True,empresa=user.empresa),
        'detalle':DetalleProProveedor.objects.filter(producto_id=id).order_by('id'),
        'det':det,
        'marcas':Marcas.objects.filter(estado=True),
        'ivas': tarifas.filter(impuesto__nombre="IVA").order_by('-porcentaje'),
        'irbpnr': tarifas.filter(impuesto__nombre="IRBPNR").order_by('-porcentaje'),
        'ices': tarifas.filter(impuesto__nombre="ICE").order_by('porcentaje'),
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request,'Inventario/registroServicios.html',contexto)

def EliminarServicioView(request,id):
    usuario=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=usuario.grupo)
    producto=Producto.objects.get(id=id)
    producto.estado=False
    producto.save()
    mensaje="El registro fue desactivado..!!"
    contexto={
        'empresa':usuario.empresa,
        'usuario': request.user,
        'productos':Producto.objects.filter(empresa=usuario.empresa,tipo='SERVICIO').order_by("-id"),
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'user2': usuario.is_admin,

    }
    return render(request, "Inventario/servicios.html", contexto)


def ProveedorView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'proveedores': Proveedor.objects.filter(empresa=user.empresa),
        'empresa': user.empresa,
        'usuario': request.user,
        'permisos':permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request, 'Inventario/proveedores.html', contexto)

def RegistroProveedorView(request):
    user = myUsuario.objects.get(usuario=request.user)
    error = mensaje = ''
    permisos = Permiso.objects.filter(grupo=user.grupo)
    if request.POST:
        estado = request.POST['estado']
        if int(estado) == 1:
            estado= True
        else:
            estado= False
        if Proveedor.objects.filter(ruc=request.POST['ruc'],empresa=user.empresa):
            error='Esta cédula o RUC de este proveedor ya existe, intente con otra..!!'
        else:
            if len(request.POST['verificar']) <= 0:
                proveedores = Proveedor(empresa=user.empresa,
                                        tipo_identificacion_id=request.POST['tipoIdentificacion'],
                                        ruc=request.POST['ruc'],
                                        razonSocial=request.POST['razonSocial'].upper(),
                                        nombreComercial=request.POST['nombreComercial'].upper(),
                                        sector=request.POST['sector'].upper(),
                                        actividad=request.POST['actividad'].upper(),
                                        telefono=request.POST['telefono'],
                                        convencional=request.POST['convencional'],
                                        web=request.POST['web'],
                                        parroquia_id=request.POST['parroquia'],
                                        direccion=request.POST['direccion'].upper(),
                                        email=request.POST['email'].lower(),
                                        estado=estado)

                proveedores.save()
                mensaje = 'Se registro corectamente.'
            else:
                error = "Hay un problema con la cedula ingresada"
    contexto = {
        'empresa': user.empresa,
        'usuario': request.user,
        'tipos_identificacion': TipoIndentificacion.objects.all(),
        'paises': Lugares.objects.filter(lugar=None),
        'permisos':permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mesaje': mensaje,
        'error': error,
        'user2': user.is_admin,
    }
    return render(request, 'Inventario/registroProveedores.html',contexto)

def EditarProveedorView(request, id):
    user=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    proveedor = Proveedor.objects.get(id=id)
    mensaje=error=""
    if request.POST:
        if len(request.POST['verificar']) <= 0:
            proveedor.tipo_identificacion = TipoIndentificacion.objects.get(id=request.POST['tipoIdentificacion'])
            proveedor.ruc = request.POST['ruc']
            proveedor.razonSocial = request.POST['razonSocial'].upper()
            proveedor.nombreComercial = request.POST['nombreComercial'].upper()
            proveedor.sector = request.POST['sector'].upper()
            proveedor.actividad = request.POST['actividad'].upper()
            proveedor.telefono = request.POST['telefono']
            proveedor.convencional = request.POST['convencional']
            proveedor.web = request.POST['web']
            proveedor.parroquia = Lugares.objects.get(id=request.POST['parroquia'])
            proveedor.direccion = request.POST['direccion'].upper()
            proveedor.email = request.POST['email']
            proveedor.estado = request.POST['estado']
            if int(proveedor.estado) == 1:
                proveedor.estado= True
            else:
                proveedor.estado= False
            proveedor.save()
            mensaje='El proveedor se edito con éxito.'
        else:
            error = "Hay un problema con la cedula ingresada"

    contexto= {
        'tipo': proveedor.tipo_identificacion,
        'ruc': proveedor.ruc,
        'razonSocial': proveedor.razonSocial,
        'nombreComercial': proveedor.nombreComercial,
        'sector': proveedor.sector,
        'actividad': proveedor.actividad,
        'telefono': proveedor.telefono,
        'convencional': proveedor.convencional,
        'web': proveedor.web,
        'parroquia': proveedor.parroquia,
        'direccion': proveedor.direccion,
        'email': proveedor.email,
        'estado': proveedor.estado,
        'tipos_identificacion': TipoIndentificacion.objects.all(),
        'usuario': request.user,
        'paises': Lugares.objects.filter(lugar=None),
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'error':error,
        'user2': user.is_admin,
    }
    return render(request, 'Inventario/registroProveedores.html', contexto)

def DeshabilitarProveedorView(request, id):
    user=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    proveedor = Proveedor.objects.get(id=id)
    proveedor.estado = False
    proveedor.save()
    contexto = {
        'proveedores': Proveedor.objects.filter(empresa=user.empresa),
        'empresa': user.empresa,
        'usuario': request.user,
        'tipos_identificacion': TipoIndentificacion.objects.all(),
        'paises': Lugares.objects.filter(lugar=None),
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje': "El Proveedor fue deshabilitado..!!",
        'user2': user.is_admin,
    }
    return render(request, 'Inventario/proveedores.html', contexto)

def BodegaView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'empresa': user.empresa,
        'usuario': request.user,
        'bodegas':Bodega.objects.filter(empresa=user.empresa).order_by('id'),
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request, 'Inventario/bodegas.html',contexto)

def registroBodegasView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    mensaje=""
    if request.POST:
        bodega=Bodega(empresa=user.empresa,bodega=request.POST['bodega'].upper(),descripcion=request.POST['descripcion'].upper(),estado=True)
        bodega.save()
        mensaje= 'La bodega se guardo con éxito.'
    contexto = {
        'usuario': request.user,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request,'Inventario/registroBodegas.html',contexto)

def editarBodegaView(request,id):
    bodega=Bodega.objects.get(id=id)
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    mensaje=""
    if request.POST:
        bodega.bodega=request.POST['bodega'].upper()
        bodega.descripcion=request.POST['descripcion'].upper()

        if int(request.POST['estado']) == 1:
            bodega.estado= True
        else:
            bodega.estado= False
        bodega.save()
        mensaje='La bodega se edito con éxito.'
    contexto={
        'bodega':bodega,
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request, 'Inventario/registroBodegas.html', contexto)


def eliminarBodega(request,id):
    bodega=Bodega.objects.get(id=id)
    bodega.estado=False
    bodega.save()
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'empresa': user.empresa,
        'usuario': request.user,
        'bodegas': Bodega.objects.filter(empresa=user.empresa).order_by('id'),
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':"La bodega fue deshabilitada..!!",
        'user2': user.is_admin,
    }
    return render(request, 'Inventario/bodegas.html', contexto)


def productosPaginado(request):
    productos = DetalleProProveedor.objects.filter(producto__estado=True).order_by('producto')#lista de todos los objetos
    paginator = Paginator(productos,20)# el numero indica la cantidad de datos a mostrar
    page = request.GET.get('page')#obtiene las paginas
    productos = paginator.get_page(page)#devuelve un diccionario con informacion de las paginas
    return productos


def existenciasIngresosEgresos(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'usuario':request.user,
        'productos':DetalleProProveedor.objects.filter(producto__empresa=user.empresa, producto__tipo="PRODUCTO"),
        'empresa':user.empresa,
        'permisos':permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request,'Inventario/registroExistenciasIngresosEgresos.html',contexto)

def registroExistencias(request,id):
    detalles=DetalleProProveedor.objects.get(id=id)
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    mensaje=""
    if request.POST:
        if int(request.POST['cantidad'])>0:
            kard=Kardex(detalle=detalles,tipo=request.POST['tipo'],
                       cantidad=request.POST['cantidad'],
                       descripcion=request.POST['descripcion'])
            kard.save()
            if kard.tipo=="I":
                mensaje="Se ha registrado el %s, con la cantidad de: %s"%("Ingreso",str(kard.cantidad))
            else:
                mensaje = "Se ha registrado el %s, con la cantidad de: %s" % ("Egreso", str(kard.cantidad))
    contexto = {
        'producto': detalles,
        'usuario': request.user,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request,'Inventario/registroExistencias.html',contexto)

def kardexGeneral(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'usuario':request.user,
        'productos':DetalleProProveedor.objects.filter(producto__empresa=user.empresa, producto__tipo="PRODUCTO"),
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request,'Inventario/kardex.html',contexto)

def reporteIngresosR(request,id):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'detalle':DetalleProProveedor.objects.get(id=id),
        'kardex':Kardex.objects.filter(detalle_id=id),
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request,'Inventario/lienzoReporteIngreso.html',contexto)

def reporteIngresos(request,id,f1='',f2=''):
    print("Fecha1:",len(f1),f1)
    print("Fecha2:",len(f2),f1)
    if len(f1)>1 and len(f2)>1:
        contexto = {
            'detalle': DetalleProProveedor.objects.get(id=id),
            'kardex': Kardex.objects.filter(detalle_id=id,fechaCreacion__range=(f1,f2)),
            'configuracion': Reportes.objects.first(),
            'desde':f1,
            'hasta':f2,
            'pie':False,
        }
    else:
        contexto = {
            'detalle': DetalleProProveedor.objects.get(id=id),
            'kardex': Kardex.objects.filter(detalle_id=id),
            'configuracion': Reportes.objects.first(),
            'pie':True,
        }
    return render_to_pdf('Inventario/reporteIngresos.html',contexto)

def reporteEgresosR(request,id):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'detalle':DetalleProProveedor.objects.get(id=id),
        'kardex':Kardex.objects.filter(detalle_id=id),
        'configuracion': Reportes.objects.first(),
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request,'Inventario/lienzoReporteEgreso.html',contexto)

def reporteEgresos(request,id,f1="",f2=""):
    print("Fecha1:", len(f1), f1)
    print("Fecha2:", len(f2), f1)
    if len(f1) > 1 and len(f2) > 1:
        contexto = {
            'detalle': DetalleProProveedor.objects.get(id=id),
            'kardex': Kardex.objects.filter(detalle_id=id, fechaCreacion__range=(f1, f2)),
            'configuracion': Reportes.objects.first(),
            'desde': f1,
            'hasta': f2,
            'pie': False,
        }
    else:
        contexto = {
            'detalle': DetalleProProveedor.objects.get(id=id),
            'kardex': Kardex.objects.filter(detalle_id=id),
            'configuracion': Reportes.objects.first(),
            'pie': True,
        }
    return render_to_pdf('Inventario/reporteEgresos.html',contexto)


def reporteTotalR(request,id):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'detalle':DetalleProProveedor.objects.get(id=id),
        'kardex':Kardex.objects.filter(detalle_id=id),
        'configuracion': Reportes.objects.first(),
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,

    }
    return render(request,'Inventario/lienzoReporteTotal.html',contexto)

def reporteTotal(request,id,f1="",f2=""):
    user=myUsuario.objects.get(usuario=request.user)
    print("Fecha1:", len(f1), f1)
    print("Fecha2:", len(f2), f1)
    if len(f1) > 1 and len(f2) > 1:
        contexto = {
            'detalle': DetalleProProveedor.objects.get(id=id),
            'kardex': Kardex.objects.filter(detalle_id=id, fechaCreacion__range=(f1, f2)),
            'configuracion': Reportes.objects.first(),
            'desde': f1,
            'hasta': f2,
            'pie': False,
            'user2': user.is_admin,
        }
    else:
        contexto = {
            'detalle': DetalleProProveedor.objects.get(id=id),
            'kardex': Kardex.objects.filter(detalle_id=id),
            'configuracion': Reportes.objects.filter(empresa=user.empresa).last(),
            'pie': True,
            'user2': user.is_admin,
        }
    #return render(request,'inventario/reporteIngresos.html',contexto)
    return render_to_pdf('Inventario/reporteTotal.html',contexto)

def MarcasView(request):
    user=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'usuario':request.user,
        'marcas':Marcas.objects.filter(empresa=user.empresa),
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,

    }
    return render(request,'Inventario/marcas.html',contexto)

def registroMarcas(request):
    user=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    mensaje=error=""
    if request.POST:
        try:
            marca=Marcas.objects.filter(empresa=user.empresa)
            print(marca)
            error = "La Marca: %s ya exite, intente con otro nombre...!!"%(marca.nombre)
        except:
            marca = Marcas(empresa=user.empresa, nombre=request.POST['marca'].upper(),
                           descripcion=request.POST['descripcion'].upper(), estado=True)
            marca.save()
            mensaje = "La marca se guardo con éxito...!!"

    contexto={
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'error':error,
        'user2': user.is_admin,
    }
    return render(request,'Inventario/registroMarcas.html',contexto)

def editarMarcas(request,id):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    marca=Marcas.objects.get(id=id)
    mensaje=error=""
    if request.POST:
        try:
            marca.nombre=request.POST['marca'].upper()
            marca.descripcion=request.POST['descripcion'].upper()
            if int(request.POST['estado']) == 1:
                marca.estado= True
            else:
                marca.estado= False
            marca.save()
            mensaje="La Marca se ha modificado Correctamente..!!"
        except:
            error="No hemos podido actualizar el registro revise la informacion proporcionada..!!"

    contexto = {
        'usuario': request.user,
        'marca':marca,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'error':error,
        'user2': user.is_admin,
    }
    return render(request, 'Inventario/registroMarcas.html', contexto)

def EliminarMarcasView(request,id):
    user = myUsuario.objects.get(usuario=request.user)
    marcas=Marcas.objects.filter(empresa=user.empresa)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    marca=marcas.get(id=id, empresa=user.empresa)
    marca.estado=False
    marca.save()
    contexto={
        'usuario':request.user,
        'marcas':marcas,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':"La marca se ha deshabilitado correctamente..!!",
        'user2': user.is_admin,
    }
    return render(request,'Inventario/marcas.html',contexto)

def Categorias(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'usuario':request.user,
        'categorias':Categoria.objects.filter(empresa=user.empresa).order_by("-id"),
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request,'Inventario/categorias.html',contexto)

def registrarCategoria(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    mensaje=""
    if request.POST:
        categoria=Categoria(empresa=user.empresa,categoria=request.POST['categoria'].upper(),descripcion=request.POST['descripcion'].upper(),estado=True)
        categoria.save()
        mensaje="La categoria se guardo con éxito."
    contexto = {
        'usuario': request.user,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request,'Inventario/registroCategorias.html',contexto)

def editarCategoria(request,id):
    user = myUsuario.objects.get(usuario=request.user)
    categoria=Categoria.objects.get(id=id)
    permisos= Permiso.objects.filter(grupo=user.grupo)
    mensaje=""
    estado=False
    if request.POST:
        if int(request.POST['estado']) ==1:
            estado=True
        else:
            estado=False
        categoria.categoria=request.POST['categoria'].upper()
        categoria.descripcion=request.POST['descripcion'].upper()
        categoria.estado=estado
        categoria.save()
        mensaje="La categoria se editó con éxito."
    contexto = {
        'usuario': request.user,
        'categoria': categoria,
        'empresa':user.empresa,
        'permisos':permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request,'Inventario/registroCategorias.html',contexto)

def EliminarCategoriaView(request,id):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    categorias=Categoria.objects.filter(empresa=user.empresa).order_by("-id")
    categoria=categorias.get(id=id)
    categoria.estado=False
    categoria.save()
    mensaje="La Categoría ha sido desactivada..!!"
    contexto={
        'usuario':request.user,
        'categorias':categorias,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request,'Inventario/categorias.html',contexto)

def ComprasView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto ={
        'compras': Compra.objects.filter(usuario__empresa=user.empresa).order_by("-id"),
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request, 'Inventario/compras.html', contexto)

@csrf_exempt
def RegistroComprasView(request, n):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    try:
        proveedor = Proveedor.objects.get(id=n)
        productos = DetalleProProveedor.objects.filter(producto__estado=True, proveedor_id=n)
        if request.POST:
            contado = request.POST['tipoventa']
            if contado == "CONTADO":
                contado = True
            else:
                contado = False
            print(request.POST)
            fecha_emision = parse_date(request.POST['fechaEmision'])
            try:
                compra = Compra(contado=contado,diasPlazo=request.POST['dias'],
                                usuario=user,
                                empresa=user.empresa,
                                tipo=request.POST['tipo'],
                                proveedor_id=request.POST['proveedor'],
                                subtotal_0=request.POST['sutotal0'],
                                subtotal_iva=request.POST['subtotal12'],
                                subtotal=request.POST['subtotal'],
                                descuento=0, iva=request.POST['iva'],
                                ice=request.POST['ice'],
                                irbpnr=request.POST['irbpnr'],
                                total=request.POST['total'],
                                fecha_emision=fecha_emision,
                                clave_acceso=request.POST['autorizacion'],
                                secuencial=request.POST['secuencial']
                                )
                compra.save()
                return HttpResponse(compra.id)
            except Exception as error:
                print(error)
                return HttpResponse(-1)
    except Exception as error:
        print(error)
        productos= None
        proveedor = None
    contexto = {
        'productos': productos,
        'proveedor': proveedor,
        'proveedores': Proveedor.objects.filter(estado=True,empresa=user.empresa),
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }

    return render(request, 'Inventario/registroCompra.html', contexto)


@csrf_exempt
def detallesCompra(request, idCompra):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    if request.POST:
        try:
            detalle = DetalleCompra(compra_id=idCompra,
                                    producto_id=request.POST['producto'],
                                    cantidad=request.POST['cantidad'],
                                    subtotal_0=float(request.POST['sub0']),
                                    subtotal_iva=float(request.POST['sub12']),
                                    subtotal=float(request.POST['sub']),
                                    descuento=0,
                                    iva=float(request.POST['iva']),
                                    ice=float(request.POST['ice']),
                                    irbpnr=float(request.POST['Irbpnr']),
                                    total=float(request.POST['total'].replace(",", ".")))
            detalle.save()
            return HttpResponse("ok")
        except Exception as error:
            print(error)
            compra = Compra.objects.get(id=idCompra)
            compra.delete()
            return HttpResponse("no")
    else:
        contexto = {
            'compra': Compra.objects.get(id=idCompra),
            'detalles': DetalleCompra.objects.filter(factura_id=idCompra),
            'reporte': Reportes.objects.all().last(),
            'usuario':request.user,
            'empresa':user.empresa,
            'permisos': permisos,
            'funciones': funciones_usuario(permisos),
            'items': Items.objects.all().order_by('prioridad'),
            'user2': user.is_admin,
        }
        return render(request, contexto)

def ver_compras(request,idCompra):
    compra=Compra.objects.get(id=idCompra)
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    detalles=DetalleCompra.objects.filter(compra=compra)
    contexto={
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
        'compra':compra,
        'detalles':detalles,
        'empresa': user.empresa,
    }
    return render(request, 'Inventario/ver_compras.html',contexto)


def ReporteProveedor(request):
    user=myUsuario.objects.get(usuario=request.user)
    proveedor = Proveedor.objects.filter(empresa=user.empresa)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        "formatedDay":time.strftime("%x %X"),
        'proveedores': proveedor,
        'reporte': Reportes.objects.all().last(),
        'configuracion': Reportes.objects.all().last(),
        'permisos': permisos,
        'funciones':  funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
        'empresa': user.empresa,
    }
    return render_to_pdf('Inventario/reporteProveedores.html', contexto)


