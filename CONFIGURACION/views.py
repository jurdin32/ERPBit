#-**- encode: utf-8 -**-
import datetime
from time import time
import time
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Sum
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from CLIENTES.models import *
from DOCUMENTOS_ELECTRONICOS.models import Factura, DetallesFactura, Retencion, GuiaRemision, DetallesRetencion
from ERPBit import settings
from INVENTARIO.models import *
from CONFIGURACION.models import *
from INVENTARIO.reportes import render_to_pdf, render_to_pdf_factura
from TALENTO_HUMANO.models import Anio
from USERS.models import myUsuario

@login_required(login_url='/login')
def IndexView(request):
    usuario = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=usuario.grupo)
    empresa=None

    todasventas=None
    totales=None

    try:
        empresa=usuario.empresa
    except:
        pass
    if request.POST:
        fecha1=request.POST['fecha1']
        fecha2 = request.POST['fecha2']
        totales=total_ventas(request,fecha1,fecha2)
        todasventas=ventas_generales(request,fecha1,fecha2)
    else:
        totales = total_ventas(request)
        todasventas = ventas_generales(request)

    contexto={
        'usuario':request.user,
        'user':usuario.is_admin,
        'clientes': Cliente.objects.filter(empresa=usuario.empresa).count(),
        'productos': Producto.objects.filter(empresa=usuario.empresa).count(),
        'usuarios': myUsuario.objects.filter(empresa=usuario.empresa).count(),
        'proveedores': Proveedor.objects.filter(empresa=usuario.empresa).count(),
        'empresa':empresa,
        'permisos':permisos,
        'funciones':funciones_usuario(permisos),#Funciones.objects.all().order_by("id"),
        'items':Items.objects.all().order_by("prioridad"),
        'user2': usuario.is_admin,
        'lista':todasventas,
        'totales':totales,

     }
    return render(request, 'base.html',contexto)

def total_ventas(request,fecha1="",fecha2=""):
    facturas=Factura.objects.filter(usuario=request.user, ambiente=2,estado="AUTORIZADO")
    if fecha1 and fecha2:
        return facturas.filter(fecha__range=(fecha1, fecha2)).aggregate(Sum('total'))
    elif fecha1:
        print("Viene la fecha1", fecha1)
        return facturas.filter(fecha__range=(fecha1,fecha1)).aggregate(Sum('total'))
    elif fecha2:
        print("Viene la fecha1", fecha2)
        return facturas.filter(fecha__range=(fecha2, fecha2)).aggregate(Sum('total'))
    return facturas.aggregate(Sum('total'))


def ventas_generales(request,fecha1="",fecha2=""):
    lista = []
    ventas = Factura.objects.filter(usuario=request.user, ambiente=2,estado="AUTORIZADO")
    if fecha1 and fecha2:
        ventas = ventas.filter(fecha__range=(fecha1, fecha2)).order_by('fecha')
    elif fecha1:
        ventas = ventas.filter(fecha__range=(fecha1, fecha1)).order_by('fecha')
    elif fecha2:
        ventas = ventas.filter(fecha__range=(fecha2, fecha2)).order_by('fecha')

    for venta in ventas:
        valor=ventas.filter(fecha=venta.fecha).aggregate(Sum("total"))
        lista.append({'fecha':str(venta.fecha.day)+'/'+str(venta.fecha.month),'valor':valor})


    lista=[i for n, i in enumerate(lista) if i not in lista[n + 1:]]
    print(lista, "contador:", len(lista))
    return lista

def funciones_usuario(permisos):
    lista=[]
    funciones=Funciones.objects.all()
    for funcion in funciones:
        for permiso in permisos:
            if permiso.item.funcion == funcion:
                lista.append(funcion)
    return set(lista)


#
# Autentificarce por medio de Usuario y Contrasena
#
def LoginView(request):
    contexto = {
        'usuario':None,
        'empresa':None,
    }
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(username=username, password=password,is_active=True)
            login(request,user)
            contexto['usuario'] = request.usuario
        except Exception as error:
            print(error)
            contexto = {'error': 'Crendenciales invalidas'}
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    return render(request, 'login.html', contexto)

#
# Terminar la secion con Logout
#
@login_required(login_url='/login')
def LogoutView(request):
    logout(request)
    response=HttpResponse()
    response.delete_cookie('empresa')
    return HttpResponseRedirect('/')

#
# Vista para presentar todos los usuarios registrados
#
@login_required(login_url='/login')
def UsuarioView(request):
    user=myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuarios':myUsuario.objects.filter(empresa=user.empresa).order_by('id'),
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request, 'Configuracion/usuarios.html', contexto)

#
# Presentar formulario para registro de nuevo Usuario
#
@login_required(login_url='/login')
def RegistroUserView(request):
    user2=myUsuario.objects.get(usuario=request.user)
    empresa = user2.empresa
    mensaje = ""
    error = -1
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        passwordConf = request.POST['passwordConf']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        contexto = {
            'username': request.POST['username'],
            'password': request.POST['password'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'mensaje': mensaje,
            'error': error,
            'usuario': request.user,
            'permisos': Permiso.objects.filter(grupo=user2.grupo),
            'user2': user2.is_admin,
        }
        if (password != passwordConf):
            contexto['mensaje'] = "Contrasena no coinciden"
            contexto['error'] = 2
            contexto['usuario'] = request.user,

        else:
            try:
                user = User(username=username,first_name=first_name, last_name=last_name, email=email)
                user.save()
                user.set_password(request.POST['password'])
                user.save()

                myUsuario(usuario=user,empresa=empresa,grupo_id=request.POST['grupo']).save()
                contexto['mensaje'] = "El registro fue creado con exito!"
                contexto['error'] = 0
                contexto['usuario'] = request.user,
            except:
                contexto['mensaje'] = "No se puede crear un usuario dos veces"
                contexto['error'] = 1
                contexto['usuario'] = request.user,
    permisos=Permiso.objects.filter(grupo=user2.grupo)
    contexto = {
        'usuario': request.user,
        'empresa': empresa,
        'users': None,
        'grupos': Grupo.objects.filter(empresa=user2.empresa),
        'mensaje':mensaje,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user2.is_admin,
    }

    return render(request, 'Configuracion/registroUser.html', contexto)

#
# Editar usuario por medio del ID y enviar a Guardar
#
@login_required(login_url='/login')
def EditarUserView(request, id):
    user = myUsuario.objects.get(usuario=request.user)
    usuario = User.objects.get(id=id)
    mensaje = ""
    error = ""
    if request.POST:
        try:
            usuario.username = request.POST['username']
            usuario.first_name = request.POST['first_name']
            usuario.last_name = request.POST['last_name']
            usuario.email = request.POST['email']
            usuario.is_active = True
            usuario.save()
            user2= myUsuario.objects.get(usuario=usuario)
            user2.grupo=Grupo.objects.get(id=request.POST['grupo'])
            user2.save()
            mensaje = "El registro fue editado con exito!"
        except Exception as error:
            mensaje ="Error: "+str(error)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'user':usuario,
        'error': error,
        'empresa': user.empresa,
        'usuario': request.user,
        'grupos': Grupo.objects.filter(empresa=user.empresa),
        'mensaje':mensaje,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,

    }
    return  render(request, 'Configuracion/registroUser.html', contexto)

#
# DESHABILIAR LAS OPCIONES DEL USUARIO (Activo - staff - superUsuer)
#
@login_required(login_url='/login')
def DeshabilitarUserView(request, id):
    mensaje=""
    usuario = User.objects.get(id=id)
    if usuario.is_active:
        usuario.is_active = False
        usuario.is_superuser = False
        usuario.is_staff = False
        usuario.save()
        mensaje="El Usuario ha sido deshabilitado, a partir de este momento ya no tendra acceso al sistema"
    else:
        usuario.is_active = True
        usuario.is_superuser = False
        usuario.is_staff = True
        usuario.save()
        mensaje = "El Usuario ha sido habilitado, a partir de este momento ya tendra acceso al sistema"

    user = myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuarios': myUsuario.objects.filter(empresa=user.empresa).order_by('id'),
        'usuario': request.user,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request, 'Configuracion/usuarios.html', contexto)

@login_required(login_url='/login')
def CambiarClaveView(request, id):
    user=myUsuario.objects.get(usuario=request.user)
    usuario = User.objects.get(id=id)
    mensaje = ""
    error = ""
    if request.POST:
        print(request.POST)
        if request.POST['clave'] == request.POST['cambiarClave']:
            usuario.set_password(request.POST['clave'])
            usuario.save()
            mensaje = "El registro fue editado con exito!"
        else:
            error = "Las contrasena no coinciden"
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'user': usuario,
        'error': error,
        'mensaje':mensaje,
        'usuario': request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,

    }
    return render(request, 'Configuracion/CambiarContrasenia.html', contexto)


#
# Vista para presentar las empresas que estan registradas en la BD
#
@login_required(login_url='/login')
def EmpresaView(request):
    usuario=myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=usuario.grupo)
    contexto = {
        'empresa': usuario.empresa,
        'usuario': request.user,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': usuario.is_admin,
    }
    return render(request, 'Configuracion/empresa.html', contexto)

#
# Registro de la Empresa
#
@login_required(login_url='/login/')
def RegistroEmpresaView(request):
    user=myUsuario.objects.get(usuario=request.user)
    empresa=None
    print()
    try:
        empresa = user.empresa
    except:
        empresa=None
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario': request.user,
        'empresa':empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    if request.POST and not empresa:
        try:
            razonSocial = request.POST['razonSocial']
            nombreComercial = request.POST['nombreComercial']
            ruc = request.POST['ruc']
            direccionMatriz = request.POST['direccionMatriz']
            telefono = request.POST['telefono']
            convencional = request.POST['convencional']
            email = request.POST['email']
            logo=None
            if request.FILES:
                logo = request.FILES['logo']
            empresa = DatosEmpresa(usuario=request.user,razonSocial=razonSocial, nombreComercial=nombreComercial, ruc=ruc,
                                   direccionMatriz=direccionMatriz,
                                   telefono=telefono, convencional=convencional, email=email, logo=logo, estado=True)
            empresa.save()
            user.empresa=empresa
            user.save()
        except Exception as error:
            print(error)

    return render(request, 'Configuracion/registroEmpresa.html',contexto)

@login_required(login_url='/login')
def EditarEmpresaView(request, id):
    empresa = DatosEmpresa.objects.get(id=id)
    user=myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    print(user.empresa.logo)
    if request.POST:
        empresa.razonSocial = request.POST['razonSocial']
        empresa.nombreComercial = request.POST['nombreComercial']
        empresa.ruc = request.POST['ruc']
        empresa.direccionMatriz = request.POST['direccionMatriz']
        empresa.telefono = request.POST['telefono']
        empresa.convencional = request.POST['convencional']
        empresa.email = request.POST['email']
        empresa.estado = request.POST['estado']
        if int(request.POST['estado']) == 1:
            empresa.estado = True
        else:
            empresa.estado = False
        if request.FILES:
            print(request.FILES)
            empresa.logo = request.FILES['logo']
        empresa.save()

    contexto = {
        'empresa':empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request, 'Configuracion/registroEmpresa.html', contexto)

@login_required(login_url='/login')
def DeshabilitarEmpresaView(request, id):
    empresa = DatosEmpresa.objects.get(id=id)
    empresa.estado = False
    empresa.save()
    return HttpResponseRedirect('/configuracion/empresa/')

@login_required(login_url='/login')
def DerpartamentoView(request):
    user=myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'departamentos': Departamento.objects.filter(empresa=user.empresa),
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request, 'Configuracion/departamentos.html', contexto)

@login_required(login_url='/login')
def RegistroDerpartamentoView(request):
    user=myUsuario.objects.get(usuario=request.user)
    empresa = user.empresa
    permisos=Permiso.objects.filter(grupo=user.grupo)
    if request.POST:
        departamento = Departamento( empresa=user.empresa,
                     empresa_id =request.POST['empresa'],
                     nombre =request.POST['nombre'],
                     descripcion =request.POST['descripcion'],
                     estado = True)
        departamento.save()
    contexto = {
        'usuario': request.user,
        'empresas': empresa,
        'empresa': DatosEmpresa.objects.get(usuario=user.usuario),
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request,'Configuracion/registroDepartamento.html',contexto)

@login_required(login_url='/login')
def EditarDerpartamentoView(request, id):
    departamento = Departamento.objects.get(id=id)
    user = myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    if request.POST:
        departamento.empresa_id = request.POST['empresa']
        departamento.nombre = request.POST['nombre']
        departamento.descripcion = request.POST['descripcion']
        departamento.estado = request.POST['estado']

        if int(request.POST['estado'])== 1:
            departamento.estado = True
        else:
            departamento.estado = False

        departamento.save()
    contexto = {
        'usuario': request.user,
        'empresa': user.empresa,
        'nombre': departamento.nombre,
        'descripcion': departamento.descripcion,
        'estado': departamento.estado,
        'empresas': DatosEmpresa.objects.filter(usuario=request.user),
        'permisos': permisos,
        'funciones':funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request, 'Configuracion/registroDepartamento.html', contexto)

@login_required(login_url='/login')
def DeshabilitarDepartamentoView(request, id):
    departamento = Departamento.objects.get(id=id)
    departamento.estado = False
    departamento.save()
    return HttpResponseRedirect('/configuracion/departamentos/')


#
# VISTA PARA LLENAR PAIS- PROVINCIA- CIUDAD Y PARROQUIA DEL EMPLEADO
#

def Lugar(request, Id):
    # Optiene las provincias a travez del pais
    ubicacion = Lugares.objects.filter(lugar_id=Id)
    cadena =""
    for p in ubicacion:
        cadena+= '''<option value = "%s"> %s </option>'''%(p.id, p.nombre)
    return HttpResponse(cadena)



#
# VISTA PARA MOSTRAR LOS GRUPOS QUE EXISTEN EN LA BASE DE DATOS
#

@login_required(login_url='/login')
def GrupoView(request):
    user=myUsuario.objects.get(usuario=request.user)
    empresa = user.empresa
    funciones = funciones_usuario(Permiso.objects.filter(grupo=user.grupo))
    contexto={
        'grupos':Grupo.objects.filter(empresa=empresa),
        'usuario':request.user,
        'empresa':empresa,
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones,
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request, 'Configuracion/grupos.html',contexto)

@login_required(login_url='/login')
def RegistroGrupoView(request):
    user = myUsuario.objects.get(usuario=request.user)
    empresa = user.empresa
    if request.POST:
        print(request.POST)
        grupo=Grupo(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],empresa=user.empresa)
        grupo.save()
        for i in request.POST:
            print(request.POST)
            try:
                permiso=Permiso(grupo_id=grupo.id,item_id=i)
                permiso.save()
            except:
                print(request.POST)
    funciones = funciones_usuario(Permiso.objects.filter(grupo=user.grupo))
    contexto={
        'usuario':request.user,
        'empresa':empresa,
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones,
        'funciones2':funciones,
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request, 'Configuracion/registroGrupo.html',contexto)

@login_required(login_url='/login')
def modificarGrupo(request,id):
    user = myUsuario.objects.get(usuario=request.user)
    empresa = user.empresa
    grupo=Grupo.objects.get(id=id)
    permisos = Permiso.objects.filter(grupo_id=id)
    if request.POST:
        permisos.delete()
        grupo.nombre=request.POST['nombre']
        grupo.descripcion=request.POST['descripcion']
        grupo.empresa=user.empresa
        grupo.save()
        print(len(request.POST))
        for i in request.POST:
            try:
                permiso = Permiso(grupo_id=grupo.id, item_id=i)
                permiso.save()
            except:
                print('error porque no es un numero')
    funciones = funciones_usuario(Permiso.objects.filter(grupo=user.grupo))
    contexto={
        'usuario': request.user,
        'empresa':empresa,
        'grupo':grupo,
        'permisos':Permiso.objects.filter(grupo=user.grupo),
        'items': Items.objects.all().order_by("prioridad"),
        'funciones':funciones,
        'perm':permisos,
        'user2': user.is_admin,
    }
    print(grupo.nombre,permisos)
    return render(request, 'Configuracion/registroGrupo.html',contexto)

@login_required(login_url='/login')
def configuracionReportes(request):
    user = myUsuario.objects.get(usuario=request.user)
    empresa = user.empresa
    reporte=Reportes.objects.filter(empresa=empresa).last()
    permisos = Permiso.objects.filter(grupo=user.grupo)
    if request.POST:
        act=None
        if 'encabezado' in request.FILES:
            reporte.encabezado = request.FILES['encabezado']
            act=request.FILES['encabezado']
        try:
            reporte.color_texto=request.POST['color_texto']
            reporte.color_fondo=request.POST['color_fondo']
            reporte.color_lineas=request.POST['color_lineas']
            reporte.color_encabezados_tablas=request.POST['color_encabezados_tablas']
            reporte.color_encabezados_tablas_texto=request.POST['color_encabezados_tablas_texto']
            reporte.ruta_imagenes=request.POST['ruta_imagenes']
            reporte.save()
        except Exception as error:
            print(error)
            rep=Reportes(empresa=empresa,color_texto=request.POST['color_texto'],color_fondo=request.POST['color_fondo'],color_lineas=request.POST['color_lineas'],
                         color_encabezados_tablas=request.POST['color_encabezados_tablas'],color_encabezados_tablas_texto=request.POST['color_encabezados_tablas_texto'],
                         ruta_imagenes=request.POST['ruta_imagenes'],encabezado=act)
            rep.save()
    contexto={
        'usuario':request.user,
        'reporte':Reportes.objects.filter(empresa=empresa).last(),
        'empresa':empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request,'Configuracion/configuracionReportes.html',contexto)

@login_required(login_url='/login')
def ReporteUsuarios(request):
    user=myUsuario.objects.get(usuario=request.user)
    usuarios = myUsuario.objects.filter(empresa=user.empresa)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        "formatedDay":time.strftime("%x %X"),
        'usuarios': usuarios,
        'reporte': Reportes.objects.filter(empresa=user.empresa).last(),
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,

    }
    return render_to_pdf('Configuracion/reporteUsuarios.html', contexto)

#registro de lugares:
def lugares(request):
    lugares=Lugares.objects.filter(lugar=None)
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    mensaje=""
    if request.POST:
        lugar=Lugares(nombre=request.POST['nombre'],pais=True)
        lugar.save()
        mensaje="El registro se ha creado exitosamente..!!"
    contexto={
        'lugares':lugares,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'usuario':request.user,
        'empresa': user.empresa,
        'mensaje':mensaje,
        'user2': user.is_admin,

    }
    return render(request,'Configuracion/lugares.html',contexto)

def registroProvinciasCantonParroquia(request,id,s):
    lugares = Lugares.objects.filter(lugar_id=id).order_by('nombre')
    user = myUsuario.objects.get(usuario=request.user)
    mensaje = ""
    permisos = Permiso.objects.filter(grupo=user.grupo)
    if request.POST:
        if s=="pro":
            lugar=Lugares(nombre=request.POST['nombre'],provincia=True, lugar_id=id)
            lugar.save()
        elif s=="ciu":
            lugar = Lugares(nombre=request.POST['nombre'], ciudad=True,lugar_id=id)
            lugar.save()
        else:
            lugar = Lugares(nombre=request.POST['nombre'], parroquia=True,lugar_id=id)
            lugar.save()

        mensaje="El registro se ha creado exitosamente..!!"
    contexto = {
        'lugares': lugares,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'usuario': request.user,
        'empresa': user.empresa,
        'mensaje': mensaje,
        'lugar':Lugares.objects.get(id=id),
        'user2': user.is_admin,
    }
    return render(request,'Configuracion/lugaresProvincias.html',contexto)

def editarProvinciasCantonParroquia(request,id):
    user = myUsuario.objects.get(usuario=request.user)
    mensaje = ""
    permisos = Permiso.objects.filter(grupo=user.grupo)
    lugar=Lugares.objects.get(id=id)
    if request.POST:
        lugar.nombre=request.POST['nombref']
        lugar.save()
        mensaje = "El registro se ha modificado exitosamente..!!"
        return HttpResponseRedirect("/configuracion/lugares/"+str(lugar.lugar.id)+"/pro/")
    contexto = {
        'lugares': Lugares.objects.filter(lugar_id=id).order_by('nombre'),
        'permisos':permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'usuario': request.user,
        'empresa': user.empresa,
        'mensaje': mensaje,
        'lugar': Lugares.objects.get(id=id),
        'user2': user.is_admin,
    }
    return render(request, 'Configuracion/lugaresProvincias.html', contexto)

def annios(request,id=0):
    user = myUsuario.objects.get(usuario=request.user)
    mensaje=""
    error=""
    permisos=Permiso.objects.filter(grupo=user.grupo)
    anio=None
    if request.POST:
        try:
            if id==0:
                anio=Anio(anio = request.POST['annio'],empresa=user.empresa,sueldoBasico=request.POST['sbu'].replace(",","."),diasLaborables=request.POST['dannio'],
                          diasMensuales=request.POST['dmes'],horasmensuales=request.POST['hmes'],diasSemanales= request.POST['dsemana'],horassemanales=request.POST['hsemana'],
                          horasdiarias=request.POST['hdias'])
                anio.save()
                mensaje="El registro se ha creado exitosamente..!!"
            else:
                anio=Anio.objects.get(id=id)
                anio.anio = request.POST['annio']
                anio.empresa = user.empresa
                anio.sueldoBasico = request.POST['sbu'].replace(",",".")
                anio.diasLaborables =request.POST['dannio']
                anio.diasMensuales = request.POST['dmes']
                anio.horasmensuales = request.POST['hmes']
                anio.horassemanales = request.POST['hsemana']
                anio.horasdiarias = request.POST['hdias']
                anio.diasSemanales= request.POST['dsemana']
                anio.save()
                mensaje = "El registro se ha actualizado exitosamente..!!"
        except:
            error="El periodo '%s' ya esta registrado..!!"%anio.anio

    contexto={
        'annios':Anio.objects.filter(empresa=user.empresa).order_by('id'),
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'usuario': request.user,
        'empresa': user.empresa,
        'mensaje': mensaje,
        'error':error,
        'user2': user.is_admin,
    }
    return render(request,'Configuracion/annios.html',contexto)

def activarAnnio(request,id):
    user=myUsuario.objects.get(usuario=request.user)
    for anio in Anio.objects.filter(empresa=user.empresa):
        if anio.id ==id:
            if anio.activado:
                anio.activado=False
            else:
                anio.activado = True
        else:
            anio.activado = False
        anio.save()
    return HttpResponseRedirect("/configuracion/annios/")

def documentacion(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'usuario': request.user,
        'empresa': user.empresa,
        'temas':Helpers.objects.all().order_by('id'),
        'user2': user.is_admin,
    }
    return render(request, 'Configuracion/docs.html',contexto)

def documentacionDetalles(request,id):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'usuario': request.user,
        'empresa': user.empresa,
        'tema': Helpers.objects.get(id=id),
        'detalles':HelpersDetalles.objects.filter(helper_id=id).order_by('id'),
        'user2': user.is_admin,
    }
    return render(request, 'Configuracion/docsDetail.html',contexto)


def ConsultaDocumentos(request):
    contexto = {
        'facturas': Factura.objects.filter(contado=False).order_by("-id"),
    }
    return render(request, 'consultaDocumentos.html', contexto)

def ListarDocumentos(request):
    if request.POST:
        print(request.POST)
        identificacion = request.POST['identificacion']
        documento = request.POST['documento']
        if documento == 'FACTURA':
            facturas = Factura.objects.filter(tipo=documento, cliente__ruc= identificacion, estado='AUTORIZADO',ambiente='2').order_by("-id")
            print('Facturas :', facturas)
            return render(request, 'Configuracion/Consultas/listarDocumentos.html', {'facturas':facturas})
        elif documento == 'RETENCION':
            retenciones = Retencion.objects.filter(tipo=documento, proveedor__ruc= identificacion, estado='AUTORIZADO')
            return render(request, 'Configuracion/Consultas/listarDocumentosRetenciones.html', {'retenciones': retenciones})
        elif documento == 'GUIA_REMISION':
            guia_remison = GuiaRemision.objects.filter(tipo=documento, factura__cliente__ruc= identificacion, estado='AUTORIZADO')
            return render(request, 'Configuracion/Consultas/listarDocumentosGuias.html', {'guias': guia_remison})

    return  HttpResponse('No hay nada')

def obtenerXMLClaves(request,clave,tipo):
    if tipo==1:
        archivo=open(clave+".xml")
        return 0
    return ''

def ConsultaDocumentoPdf(request, idFactura):
    factura = Factura.objects.get(id=idFactura)
    reporte = Reportes.objects.filter(empresa=factura.empresa).last()
    contexto = {
        'factura': factura,
        'detalles': DetallesFactura.objects.filter(factura_id=idFactura),
        'reporte':reporte,
    }
    return render_to_pdf_factura('Docuementos_Electronicos/repFactura.html', contexto, factura)

def ConsultaDocumentoPdfRetencion(request, idRetencion):
    retencion = Retencion.objects.get(id= idRetencion)
    reporte = Reportes.objects.filter(empresa=retencion.empresa).last()
    contexto = {
        'retencion':retencion,
        'detalles': DetallesRetencion.objects.filter(retencion=retencion),
        'reporte':reporte,
    }
    return render_to_pdf('Docuementos_Electronicos/repRetencion.html', contexto)

def ConsultaDocumentoPdfGuia(request, idGuia):
    guia= GuiaRemision.objects.get(id=idGuia)
    contexto = {
        'guia': guia,
        'detalles': DetallesFactura.objects.filter(factura=guia.factura),
        'reporte': Reportes.objects.filter(empresa=guia.factura.empresa).last(),
    }
    return render_to_pdf('Docuementos_Electronicos/repGuiaRemision.html',contexto)

def usuariosActivos(request):
    logins=User.objects.filter(last_login=datetime.datetime.now())
    print(logins)
    return HttpResponse(logins)