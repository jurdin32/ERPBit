# coding:utf-8
import json

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt

from CLIENTES.forms import UploadForm
from CLIENTES.models import Cliente, TipoIndentificacion
from CLIENTES.validarCedulasRuc import verificar_cedula
from CONFIGURACION.views import funciones_usuario
from ERPBit.settings import BASE_DIR
from INVENTARIO.reportes import render_to_pdf
import time
import openpyxl


# Create your views here.
from CONFIGURACION.models import DatosEmpresa, Reportes, Lugares, Permiso, Funciones, Items
from USERS.models import myUsuario
import datetime

def ClienteView(request):
    user=myUsuario.objects.get(usuario=request.user)
    contexto = {
        'clientes': Cliente.objects.filter(empresa=user.empresa).order_by('apellido'),
        'empresa':user.empresa,
        'usuario':request.user,
        'paises': Lugares.objects.filter(lugar=None),
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
        'items': Items.objects.all().order_by('prioridad'),
        'user': user.is_admin,
    }
    return render(request, 'Clientes/clientes.html', contexto)

def RegistroClienteView(request):
    user = myUsuario.objects.get(usuario=request.user)
    error = mensaje = ''
    if request.POST:
        if Cliente.objects.filter(ruc = request.POST['ruc'], empresa_id = user.empresa.id):
            error ="La cédula o ruc ingresado ya existe"
            try:
                valor = request.POST['Ext']
                print(valor)
                return HttpResponse('ya')
            except:
                pass

        else:
            if len(request.POST['verificar'])<=0:
                if int(request.POST['ruc']) > 0:
                    cliente = Cliente(empresa=user.empresa,ruc=request.POST['ruc'], nombre=request.POST['nombre'], apellido=request.POST['apellido'],
                                      razonSocial=request.POST['razonSocial'],parroquia_id=request.POST['parroquia'], direccion=request.POST['direccion'],
                                      telefono=request.POST['telefono'], email=request.POST['email'], estado=True,tipo_identificacion_id=request.POST['tipoIdentificacion'])
                    cliente.save()
                    mensaje = 'Se registro corectamente.'
                    try:
                        valor=request.POST['Ext']
                        print(valor)
                        return HttpResponse(cliente.id)
                    except:
                        pass
                else:
                    error = "Hay un problema con la cedula ingresada"
            else:
                error= "Hay un problema con la cedula ingresada"
                try:
                    valor=request.POST['Ext']
                    print(valor)
                    return HttpResponse("no")
                except:
                    pass
    contexto = {
        'usuario': request.user,
        'tipos_identificacion': TipoIndentificacion.objects.all(),
        'paises': Lugares.objects.filter(lugar=None),
        'empresa': user.empresa,
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
        'items': Items.objects.all(),
        'mensaje': mensaje,
        'error': error,
        'user': user.is_admin,
    }
    return render(request, 'Clientes/registroClientes.html',contexto)


def EditarClienteView(request, id):
    mensaje = ''
    error=""
    user = myUsuario.objects.get(usuario=request.user)
    cliente = Cliente.objects.get(id=id)
    if request.POST:
        if len(request.POST['verificar']) <= 0:
            cliente.tipo_identificacion=TipoIndentificacion.objects.get(id=request.POST['tipoIdentificacion'])
            cliente.ruc = request.POST['ruc']
            cliente.nombre = request.POST['nombre']
            cliente.apellido = request.POST['apellido']
            cliente.razonSocial = request.POST['razonSocial']
            cliente.direccion = request.POST['direccion']
            cliente.telefono = request.POST['telefono']
            cliente.email = request.POST['email']
            cliente.estado = request.POST['estado']
            cliente.parroquia=Lugares.objects.get(id=request.POST['parroquia'])
            if int(request.POST['estado']) == 1:
               cliente.estado = True
            else:
               cliente.estado = False
            cliente.save()
            mensaje = 'El registro se ha modificado correctamente...!!'
        else:
            error="La cedula o ruc ingresado: %s no es correcto, es posible que esten mal ingresados, Reintente..!!"%str(request.POST['ruc'])
    contexto= {
            'tipos_identificacion':TipoIndentificacion.objects.all(),
            'tipo':cliente.tipo_identificacion,
            'ruc': cliente.ruc,
            'nombre': cliente.nombre,
            'apellido': cliente.apellido,
            'razonSocial': cliente.razonSocial,
            'direccion': cliente.direccion,
            'telefono': cliente.telefono,
            'email': cliente.email,
            'estado': cliente.estado,
            'parroquia':cliente.parroquia,
            'empresa': user.empresa,
            'usuario': request.user,
            'paises': Lugares.objects.filter(lugar=None),
            'permisos': Permiso.objects.filter(grupo=user.grupo),
            'funciones': funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
            'items': Items.objects.all(),
            'mensaje': mensaje,
            'error':error,
            'user': user.is_admin,
    }
    return render(request, 'Clientes/registroClientes.html', contexto)

def DeshabilitarClienteView(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.estado = False
    cliente.save()
    #return HttpResponse("El Cliente fue dashabilitado del sistema.")
    return HttpResponseRedirect('/clientes/')

def ReporteClientes(request):
    user=myUsuario.objects.get(usuario=request.user)
    cliente = Cliente.objects.filter(empresa=user.empresa)
    reporte= Reportes.objects.filter(empresa=user.empresa).last()
    contexto = {
        "formatedDay":time.strftime("%x %X"),
        'clientes': cliente,
        'reporte': reporte,
        'configuracion': reporte,
        'user': user.is_admin,
    }
    return render_to_pdf('Clientes/reporteClientes.html',contexto)


def ReporteClientesDinamicos(request):
    user = myUsuario.objects.get(usuario=request.user)
    reporte = Reportes.objects.all().last()
    contexto = {
        'empresa':user.empresa,
        'reporte': reporte,
        'configuracion': reporte,
        'usuario':request.user,
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones':funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
        'items': Items.objects.all(),
        'user': user.is_admin,
    }
    return render(request, 'Clientes/reporteDinamicos.html', contexto)


def consultarClientes(request,estados,fecha1,fecha2):
    usuario=myUsuario.objects.get(usuario=request.user)
    estado=False
    clientes = None
    if estados=="A":
        estado=True

    if not fecha1 and not fecha2:
        clientes = Cliente.objects.filter(estado=estado,empresa=usuario.empresa)

    #se ejecuta cuando viene el estado, junto con las fechas1 o fecha2
    if fecha1 or fecha2:
        clientes = Cliente.objects.filter(estado=estado,empresa=usuario.empresa)
        if fecha1 and not fecha2:
            print('Clientes fecha1:', clientes)
            clientes = clientes.filter(estado=estado,empresa=usuario.empresa, creado__range=(fecha1, fecha1)) | clientes.filter(estado=estado,empresa=usuario.empresa, modificado__range=(fecha1, fecha1))
        elif fecha1 and fecha2:
            print('Clientes fecha1 y fecha2:', clientes)
            clientes = clientes.filter(estado=estado,empresa=usuario.empresa, creado__range=(fecha1, fecha1)) | clientes.filter(estado=estado,empresa=usuario.empresa, modificado__range=(fecha1, fecha2))
        else:
            print('Clientes fecha2:', clientes)
            clientes = clientes.filter(estado=estado,empresa=usuario.empresa,creado__range=(fecha2, fecha2)) | clientes.filter(estado=estado,empresa=usuario.empresa, modificado__range=(fecha2, fecha2))

    #se ejecuta cuando viene para mostrar todo
    if estados=='T':
        clientes = Cliente.objects.filter(empresa=usuario.empresa)
        if fecha1 or fecha2:
            if fecha1 and not fecha2:
                print('Todos Clientes fecha1:', clientes)
                clientes = clientes.filter(empresa=usuario.empresa,creado__range=(fecha1, fecha1)) | clientes.filter(modificado__range=(fecha1, fecha1))
            elif fecha1 and fecha2:
                print('Todos Clientes fecha1 y fecha2:', clientes)
                clientes = clientes.filter(empresa=usuario.empresa,creado__range=(fecha1, fecha2)) | clientes.filter(modificado__range=(fecha1, fecha2))
            else:
                print('Todos Clientes fecha2:', clientes)
                clientes = clientes.filter(empresa=usuario.empresa,creado__range=(fecha2, fecha2)) | clientes.filter(modificado__range=(fecha2, fecha2))
        else:
            clientes=Cliente.objects.filter(empresa=usuario.empresa)
    return clientes

@csrf_exempt
def ListarClientesAjax(request):
    data = {'status': False}
    items = []
    if request.POST:
        estado = request.POST['estado']
        fecha1 = request.POST['fecha1']
        fecha2 = request.POST['fecha2']
        print(estado, fecha1, fecha2)
        n=1
        for cliente in consultarClientes(request,estado,fecha1,fecha2):
            estado=""
            if cliente.estado:
                estado="ACTIVO"
            else:
                estado="NO ACTIVO "
            items.append({
                'numero':n,
                'identificacion': cliente.ruc,
                'nombre': cliente.nombre.upper(),
                'apellido': cliente.apellido.upper(),
                'telefono': cliente.telefono,
                'direccion': cliente.direccion.upper(),
                'estado': estado,
                'nombreComercial':cliente.razonSocial.upper()
            })
            n+=1
        data = {'status': True}
    data['items'] = items
    return JsonResponse(data)

@csrf_exempt
def simple_upload(request):
    if request.method == 'POST':
        print(request.POST)
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save("excel/"+myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(BASE_DIR+uploaded_file_url)
        datos=openpyxl.load_workbook(BASE_DIR+uploaded_file_url)
        hoja=datos.get_sheet_by_name('Hoja1')
        lista=[]
        dt={}
        for row in hoja.values:
            for i in range(len(row)):
                dt[i]=row[i]
            lista+=[dt]
        listado=json.dumps({'datos':lista}, ensure_ascii=False)
        print (listado)
        return HttpResponse(listado,content_type='application/json')

@csrf_exempt
def migrarClientes(request):
    user = myUsuario.objects.get(usuario=request.user)
    contexto = {
        'empresa': user.empresa,
        'usuario': request.user,
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
        'items': Items.objects.all(),
        'user': user.is_admin,
    }
    if request.POST:
        print (request.POST)
        if Cliente.objects.filter(ruc = request.POST['identificacion'], empresa_id = user.empresa.id):
            return HttpResponse("no")
        else:
            if int(request.POST['identificacion']) > 0:
                cliente = Cliente(empresa=user.empresa,ruc=request.POST['identificacion'], nombre=request.POST['nombres'], apellido=request.POST['apellidos'],
                                  razonSocial=request.POST['razonSocial'], direccion=request.POST['direccion'],
                                  telefono=request.POST['telefono'], email=request.POST['email'], estado=True,tipo_identificacion_id=request.POST['tipo'])
                cliente.save()
                return HttpResponse("ok")
            else:
               return HttpResponse("no")
    return render(request, "Clientes/migracionClientes.html",contexto)
