# coding: utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from CONFIGURACION.models import Reportes, Permiso, Funciones, Items
from CONFIGURACION.views import funciones_usuario
from INVENTARIO.reportes import render_to_pdf
from TRANSPORTE.models import *
import time

from USERS.models import myUsuario


def EmpresaView(request):
    user=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'emprasaTrans': EmpresaTransporte.objects.filter(empresa=user.empresa),
        'empresa':user.empresa,
        'usuario':request.user,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request, 'Transporte/empresas.html', contexto)


def RegistroEmpresaTransView(request):
    user= myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    if request.method == 'POST':
        ruc = request.POST['ruc']
        razonSocial = request.POST['razonSocial']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        convencional = request.POST['convencional']
        email = request.POST['email']
        estado = request.POST['estado']
        if int(estado) == 1:
            estado = True
        else:
            estado = False
        empresaTrans = EmpresaTransporte(empresa=user.empresa,ruc=ruc,razonSocial=razonSocial, direccion=direccion,
                          telefono=telefono, convencional=convencional, email=email, estado=True)

        empresaTrans.save()
    contexto = {
        'emprasaTrans': EmpresaTransporte.objects.filter(empresa=user.empresa),
        'empresa': user.empresa,
        'usuario': request.user,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }

    return render(request, 'Transporte/registroEmpresaTrans.html', contexto)


def EditarEmpresaView(request, id):
    empresaTrans = EmpresaTransporte.objects.get(id=id)
    user=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    if request.POST:
        empresaTrans.ruc = request.POST['ruc']
        empresaTrans.razonSocial = request.POST['razonSocial']
        empresaTrans.direccion = request.POST['direccion']
        empresaTrans.telefono = request.POST['telefono']
        empresaTrans.convencional = request.POST['convencional']
        empresaTrans.email = request.POST['email']
        empresaTrans.estado = request.POST['estado']
        if int(request.POST['estado']) == 1:
            empresaTrans.estado = True
        else:
            empresaTrans.estado = False

        empresaTrans.save()

    contexto = {
            'ruc': empresaTrans.ruc,
            'razonSocial': empresaTrans.razonSocial,
            'direccion': empresaTrans.direccion,
            'telefono': empresaTrans.telefono,
            'convencional': empresaTrans.telefono,
            'email': empresaTrans.email,
            'estado': empresaTrans.estado,
            'usuario':request.user,
            'empresa':user.empresa,
            'permisos': permisos,
            'funciones': funciones_usuario(permisos),
            'items': Items.objects.all(),
            'user2': user.is_admin,
        }

    return render(request, 'Transporte/registroEmpresaTrans.html', contexto)


def DeshabilitarEmpresaView(request, id):
    empresaTrans = EmpresaTransporte.objects.get(id=id)
    empresaTrans.estado = False
    empresaTrans.save()
    return HttpResponseRedirect('/transporte/empresas/')


def ConductorView(request):
    user=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'conductores': ConductorTrans.objects.all(),
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request, 'Transporte/conductores.html', contexto)


def RegistroConductorView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    if request.method == 'POST':
        ruc = request.POST['ruc']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        email = request.POST['email']
        licencia = request.POST['licencia']
        empresa = request.POST['empresa']
        estado = request.POST['estado']
        tipo_identificacion=request.POST['tipo_identificacion']

        if int(estado) == 1:
            estado = True
        else:
            estado = False
        conductorTrans = ConductorTrans(empresa=user.empresa,ruc=ruc,nombre=nombre, apellido=apellido, direccion=direccion,tipoIndentificacion_id=tipo_identificacion,
                          telefono=telefono, email=email, licencia=licencia, empresaTrans_id=empresa, estado=True)

        conductorTrans.save()

    contexto = {
        'empresas': EmpresaTransporte.objects.filter(empresa=user.empresa),
        'usuario': request.user,
        'empresa':user.empresa,
        'tipos': TipoIndentificacion.objects.all(),
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request, 'Transporte/registroConductor.html', contexto)


def EditarConductorView(request, id):
    user=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    conductorTrans = ConductorTrans.objects.get(id=id)
    if request.POST:
        conductorTrans.tipoIndentificacion=TipoIndentificacion.objects.get(id=request.POST['tipo_identificacion'])
        conductorTrans.ruc = request.POST['ruc']
        conductorTrans.nombre = request.POST['nombre']
        conductorTrans.apellido = request.POST['apellido']
        conductorTrans.direccion = request.POST['direccion']
        conductorTrans.telefono = request.POST['telefono']
        conductorTrans.email = request.POST['email']
        conductorTrans.licencia = request.POST['licencia']
        conductorTrans.empresaTrans_id = request.POST['empresa']
        conductorTrans.estado = request.POST['estado']
        if int(request.POST['estado']) == 1:
            conductorTrans.estado = True
        else:
            conductorTrans.estado = False

        conductorTrans.save()
        print("se guardo")

    contexto = {
        'conductor': conductorTrans,
        'empresas': EmpresaTransporte.objects.all(),
        'tipos':TipoIndentificacion.objects.all(),
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request, 'Transporte/registroConductor.html', contexto)


def DeshabilitarConductorView(request, id):
    conductorTrans = ConductorTrans.objects.get(id=id)
    conductorTrans.estado = False
    conductorTrans.save()
    return HttpResponseRedirect('/transporte/conductores/')

def VehiculoView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'empresas': EmpresaTransporte.objects.filter(estado=True),
        'condutores': ConductorTrans.objects.filter(estado=True),
        'vehiculos': VehiculoTrans.objects.all(),
        'empresa':user.empresa,
        'usuario':request.user,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request, 'Transporte/vehiculos.html', contexto)

def RegistroVehiculoView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    if request.method == 'POST':
        placa = request.POST['placas'].upper()
        modelo = request.POST['modelo'].upper()
        marca = request.POST['marca'].upper()
        matricula = request.POST['matricula'].upper()
        conductor = request.POST['conductor'].upper()
        descripcion = request.POST['descripcion'].upper()
        estado = request.POST['estado']

        if int(estado) == 1:
            estado = True
        else:
            estado = False

        vehiculo = VehiculoTrans(empresa=user.empresa,placa=placa, modelo=modelo, marca=marca, matricula=matricula, conductor_id=conductor,
                                 estado=True)
        vehiculo.save()
        vehiculo.codigoAdicional=modelo[0:2]+"-"+marca[0:2]+"-"+str(vehiculo.id)
        vehiculo.save()

    contexto = {
        'conductores': ConductorTrans.objects.all(),
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }

    return render(request, 'Transporte/registroVehiculo.html', contexto)

def EditarVehiculoView(request, id):
    vehiculo = VehiculoTrans.objects.get(id=id)
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    if request.POST:
        vehiculo.placa = request.POST['placas'].upper()
        vehiculo.modelo = request.POST['modelo'].upper()
        vehiculo.marca = request.POST['marca'].upper()
        vehiculo.matricula = request.POST['matricula'].upper()
        vehiculo.conductor_id = request.POST['conductor'].upper()
        vehiculo.descripcion = request.POST['descripcion'].upper()
        vehiculo.estado = request.POST['estado']

        vehiculo.codigoAdicional=request.POST['modelo'][0:2].upper()+"-"+request.POST['marca'][0:2].upper()+"-"+str(vehiculo.id)
        if int(request.POST['estado'])== 1:
            vehiculo.estado = True
        else:
            vehiculo.estado = False
        vehiculo.save()


    contexto = {
        'vehiculo':VehiculoTrans.objects.get(id=id),
        'conductores': ConductorTrans.objects.all(),
        'usuario':request.user,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request, 'Transporte/registroVehiculo.html', contexto)

def DeshabilitarVehiculoView(request, id):
    vehiculo = VehiculoTrans.objects.get(id=id)
    vehiculo.estado = False
    vehiculo.save()
    return HttpResponseRedirect('/transporte/vehiculos/')

def ReporteTransporte(request):
    empresas = EmpresaTransporte.objects.all()
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)

    contexto = {
        "formatedDay":time.strftime("%x %X"),
        'empresas': empresas,
        'reporte': Reportes.objects.all().last(),
        'configuracion': Reportes.objects.all().last(),
        'empresa':user.empresa,
        'usuario':request.user,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render_to_pdf('Transporte/reporteTransportes.html', contexto)