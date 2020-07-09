from django.core import serializers
from django.http import HttpResponseRedirect,JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from CONFIGURACION.models import Permiso, Items
from CONFIGURACION.views import funciones_usuario
from CONTABILIDAD.models import PlanCuentas, Cuenta_Banco, Bancos
from DOCUMENTOS_ELECTRONICOS.models import Impuestos
from USERS.models import myUsuario
import json

def catalogoCuentas(request,id=0):
    user=myUsuario.objects.get(usuario=request.user)
    principal=None
    permisos=Permiso.objects.filter(grupo=user.grupo)
    nivel=1
    if request.POST and id>0:
        nivel = len(request.POST['codigo'].split("."))
        cuenta=PlanCuentas.objects.get(id=id)
        cuenta.nombre=request.POST['nombre'].upper()
        cuenta.nivel=nivel
        cuenta.save()
    if request.POST and id==0:
        if request.POST['principal']:
            nivel=len(request.POST['codigo'].split("."))
            principal=PlanCuentas.objects.get(codigo=request.POST['principal'])
        cuenta = PlanCuentas(nivel=nivel,nombre=request.POST['nombre'].upper(),
                             codigo=request.POST['codigo'],principal=principal,empresa=user.empresa)
        cuenta.save()
    contexto={
        'usuario': request.user,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all(),
        'cuentas': PlanCuentas.objects.filter(empresa=user.empresa).order_by('codigo'),
        'user2': user.is_admin,
    }
    # plan=PlanCuentas.objects.filter(empresa=user.empresa).order_by('codigo')
    # return HttpResponse(serializers.serialize('json',plan),content_type="application/json")
    return render(request,'Contabilidad/catalogoCuentas.html',contexto)

def eliminarCuenta(request,id):
    cuenta=PlanCuentas.objects.get(id=id)
    cuenta.delete()
    return HttpResponseRedirect('/contabilidad/catalogo/')

def registroContable(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all(),
        'cuentas': PlanCuentas.objects.filter(empresa=user.empresa).order_by('codigo'),
        'user2': user.is_admin,
    }
    return render(request,'Contabilidad/regitroContable.html',contexto)

def registroBancos(request,id=0):
    mensaje=""
    user=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    cuentac=""
    error=''
    if request.POST:
        try:
            if id == 0:
                if request.POST['tipo']=="0":
                    error="La cuenta no puede crearse sin un tipo especificado"
                else:
                    cuenta=Cuenta_Banco(empresa=user.empresa,banco_id=request.POST['banco'],tipo_cuenta=request.POST['tipo'],
                                        no_cuenta=request.POST['cuenta'],enlace_id=request.POST['ccuenta'])
                    cuenta.save()
                    mensaje="Se ha registrado la cuenta %s del %s de manera exitosa."%(cuenta.no_cuenta,cuenta.banco.nombre)
            else:
                if request.POST['tipo']=="0":
                    error="La cuenta no puede modificarse sin un tipo especificado"
                else:
                    cuenta=Cuenta_Banco.objects.get(id=id)
                    cuenta.banco_id=request.POST['banco']
                    cuenta.tipo_cuenta=request.POST['tipo']
                    cuenta.no_cuenta=request.POST['cuenta']
                    cuenta.enlace_id=request.POST['ccuenta']
                    cuenta.save()
                    mensaje = "Se ha modificado una cuenta exitosamente."
        except:
            error="Es posible que algunos campos falten"

    if not id==0:
        cuentac=Cuenta_Banco.objects.get(id=id)
    contexto = {
        'bancos':Bancos.objects.all().order_by('nombre'),
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all(),
        'cuentas': PlanCuentas.objects.filter(empresa=user.empresa).order_by('codigo'),
        'cbancos':Cuenta_Banco.objects.filter(empresa=user.empresa).order_by("banco"),
        'mensaje':mensaje,
        'cuenta':cuentac,
        'error':error,
        'user2': user.is_admin,
    }
    return render(request,'Contabilidad/CuentaBancos.html',contexto)

def desactivarRegistroBancos(request,id=0):
    user = myUsuario.objects.get(usuario=request.user)
    cuenta=Cuenta_Banco.objects.get(id=id)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    if cuenta.estado == False:
        cuenta.estado=True
        mensaje = "Se ha Habilitado una cuenta exitosamente."

    else:
        cuenta.estado=False
        mensaje = "Se ha Deshabilitado una cuenta exitosamente."
    cuenta.save()

    contexto = {
        'bancos':Bancos.objects.all().order_by('nombre'),
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all(),
        'cuentas': PlanCuentas.objects.filter(empresa=user.empresa).order_by('codigo'),
        'cbancos':Cuenta_Banco.objects.filter(empresa=user.empresa).order_by("banco"),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request,'Contabilidad/CuentaBancos.html',contexto)


#porcentajes de retencion:
def porcentajes_retencion(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    mensaje=""
    error=""
    if request.POST:
        if request.POST['id']:
            try:
                impuesto=Impuestos.objects.get(id=request.POST['id'])
                impuesto.codigo=request.POST['codigo']
                impuesto.nombre=request.POST['nombre']
                impuesto.save()
                mensaje="El registro ha sido actualizado exitosamente.!"
            except Exception as error2:
                print(error2)
                error="Al Parecer hay un error: %s"%str(error2.args)
        else:
            try:
                Impuestos(codigo=request.POST['codigo'],nombre=request.POST['nombre']).save()
                mensaje="El Impuesto fue creado exitosamente.!"
            except Exception as error2:
                print(error2)
                error = "Al Parecer hay un error: %s" % str(error2.args)

    contexto = {
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all(),
        'cuentas': PlanCuentas.objects.filter(empresa=user.empresa).order_by('codigo'),
        'user2': user.is_admin,
        'impuestos':Impuestos.objects.all().order_by('codigo'),
        'mensaje':mensaje,
        'error':error,
    }
    return render(request, 'Contabilidad/porcentajesRetencion.html', contexto)