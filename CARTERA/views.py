#encoding:utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime
# Create your views here.
from CARTERA.models import *
from CONFIGURACION.models import Permiso, Reportes, Cargos, Departamento, Items, Funciones
from CONFIGURACION.views import funciones_usuario
from DOCUMENTOS_ELECTRONICOS.models import Factura, CuentasPorCobrar, DetallesCuentasCobrar
from django.db.models import Sum
import json

from INVENTARIO.reportes import render_to_pdf
from TALENTO_HUMANO.models import Empleado, Sueldos
from USERS.models import myUsuario


def aperturaCaja(request):
    aperturas=AperturaCaja.objects.filter(usuario=request.user).order_by('-id')
    user=myUsuario.objects.get(usuario=request.user)
    print ("Filtrando por el mes: ",datetime.now().month)
    if request.POST:
        print(request.POST)
        try:
            logica=aperturas.get(usuario=request.user,estado=False)
            print("ya hay logica aqui")
        except:
            saldo=float(request.POST['tbilletes'])+float(request.POST['tmonedas'])+float(request.POST['tdocumentos'])
            print(saldo)
            apertura = AperturaCaja(empresa=user.empresa,usuario=request.user, totalBilletes=request.POST['tbilletes'],
                                    totalMonedas=request.POST['tmonedas'], totalDocumentos=request.POST['tdocumentos'],estado=False, saldoInicial=saldo,
                                    mon1=request.POST['mon1'],mon5=request.POST['mon5'],mon10=request.POST['mon10'],mon25=request.POST['mon25'],mon50=request.POST['mon50'],mon100=request.POST['mon100'],
                                    bil1=request.POST['bil1'],bil5=request.POST['bil5'],bil10=request.POST['bil10'],bil20=request.POST['bil20'],bil50=request.POST['bil50'],bil100=request.POST['bil100'],
                                    )
            apertura.save()
    contexto={
        'aperturas':aperturas,
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
        'items': Items.objects.all(),
        'user2': user.is_admin,
    }
    return render(request, 'Cartera/aperturaCaja.html',contexto)


def gastosDiarios(request):
    user = myUsuario.objects.get(usuario=request.user)
    apertura =None
    try:
        apertura=AperturaCaja.objects.get(estado=False,usuario=request.user)
    except Exception as error:
        print(error)

    gastos = GastosDiarios.objects.filter(caja__usuario=request.user, fecha__month=datetime.now().month).order_by('-id')
    mensaje=""
    if request.POST:
        if apertura:
            gasto=GastosDiarios(caja=apertura,descripcion=request.POST['descripcion'],valor=request.POST['valor'],tipoDocumento=request.POST['tipoDocumento'],numeroDocumento=request.POST['numero'],tipo=request.POST['tipo'])
            gasto.save()
        else:
            mensaje = "No hay caja aperturada..!!"
            print(mensaje)

    contexto={
        'usuario':request.user,
        'gastos':gastos,
        'empresa':user.empresa,
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
        'items': Items.objects.all(),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request,'Cartera/GastosDiarios.html',contexto)


def cierreCaja(request):
    user = myUsuario.objects.get(usuario=request.user)
    apertura = AperturaCaja.objects.filter(estado=False, usuario=request.user).last()
    ventas = 0.00
    gastos  = 0.00
    suma =0.00
    cuentas_cobrar=0.00
    cierres = CierreCaja.objects.filter(caja__usuario=request.user).order_by('-id')
    print(DetallesCuentasCobrar.objects.filter(caja=apertura,estado=True),'cuentas por cobrar')
    try:
        cuentas_cobrar=float(DetallesCuentasCobrar.objects.filter(caja=apertura,estado=True).aggregate(Sum('abono'))['abono__sum'])
        print("cuentas por cobrar",cuentas_cobrar)
    except Exception as error:
        print(error,"cuentas por cobrar",DetallesCuentasCobrar.objects.filter(caja=apertura))
    try:
        ventas=float(Factura.objects.filter(caja=apertura,contado=True,tipo="FACTURA",estado="AUTORIZADO",ambiente=2).aggregate(Sum('total'))['total__sum'])
    except Exception as error:
        print(error,'ventas')
    try:
        gastos = float(GastosDiarios.objects.filter(caja=apertura).aggregate(Sum('valor'))['valor__sum'])
    except Exception as error:
        print(error,'gastos')
    try:
        suma=(float(apertura.saldoInicial) + ventas + cuentas_cobrar) - gastos
    except Exception as error:
        print(error,'suma')
    print("la suma de los valores es: ",suma, apertura.saldoInicial)

    if request.POST and apertura:
        cierre=CierreCaja(empresa=user.empresa,caja=apertura,saldoInicial=apertura.saldoInicial,totalGasto=gastos,totalVentas=ventas,cuentasCobrar=cuentas_cobrar,totalBilletes=request.POST['billetes'],
                          totalMonedas=request.POST['monedas'],totalDocumentos=request.POST['documentos'],saldoFinal=request.POST['saldo'],estado=True)
        cierre.save()
        apertura.estado=True
        apertura.save()
        print("La Caja se Cerro..!!")
    contexto={
        'cierres':cierres,
        'usuario':request.user,
        'apertura':apertura,
        'ventas':ventas + cuentas_cobrar,
        'gastos':gastos,
        'totales':suma,
        'empresa':user.empresa,
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
        'items': Items.objects.all(),
        'user2': user.is_admin,
    }
    return render(request,'Cartera/CierreCaja.html',contexto)

def AnticiposSueldo(request):
    user=myUsuario.objects.get(usuario=request.user)
    contexto={
        'usuario':request.user,
        'empresa':user.empresa,
        'empleados':Empleado.objects.filter(departamento__empresa=user.empresa,estado=True),
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
        'items': Items.objects.all(),
        'user2': user.is_admin,
    }
    return render(request, 'Cartera/AnticiposSueldo.html', contexto)

def registroAnticipo(request,id):
    usuario = myUsuario.objects.get(usuario=request.user)
    empleado=Empleado.objects.get(id=id)
    if request.POST:
        anticipo=AnticiposSueldos(valor=request.POST['valor'],descripcion=request.POST['descripcion'],empleado=empleado)
        anticipo.save()
    anticipos = AnticiposSueldos.objects.filter(empleado=empleado, fecha__month=datetime.now().month).order_by('id')
    valores = 0.00
    if anticipos:
        valores = anticipos.aggregate(Sum('valor'))['valor__sum']
    contexto = {
        'usuario': request.user,
        'empresa': usuario.empresa,
        'empleado': empleado,
        'sueldo':Sueldos.objects.get(estado=True,empleado=empleado),
        'anticipos':anticipos,
        'valorAnticipo':valores,
        'permisos': Permiso.objects.filter(grupo=usuario.grupo),
        'funciones': funciones_usuario(Permiso.objects.filter(grupo=usuario.grupo)),
        'items': Items.objects.all(),
        'user2': usuario.is_admin,
    }
    return render(request, 'Cartera/AnticiposSueldoEmpleado.html', contexto)

def CuentasPagar(request):
    user = myUsuario.objects.get(usuario=request.user)
    contexto={
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
        'items': Items.objects.all(),
        'user2': user.is_admin,
    }
    return render(request,'',contexto)

def CuentasCobraar(request):
    user = myUsuario.objects.get(usuario=request.user)
    contexto = {
        'usuario': request.user,
        'empresa': user.empresa,
        'facturas': Factura.objects.filter(cliente__empresa=user.empresa,contado=False).order_by("-id"),
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
        'items': Items.objects.all(),
        'user2': user.is_admin,
    }
    return render(request,'Cartera/ctasxCobrar.html',contexto)


def registroCuentas(request,idFactura):
    user = myUsuario.objects.get(usuario=request.user)
    tabla=None
    cuenta=None
    mensaje=""
    if request.POST:
        try:
            factura=Factura.objects.get(id=idFactura)
            factura.estado_por_pagar=False
            factura.save()
            cuentas=CuentasPorCobrar(usuario=user,factura_id=idFactura,valor=request.POST['totales'].replace(",","."),plazo=request.POST['frecuencia'],cuotas=request.POST['cuotas'],estado=False)
            cuentas.save()
            mensaje=detallesCuentasCobrar(request,cuentas, request.POST['json'])
            print(mensaje)
        except :
            mensaje="Al parecer no hay caja aperturada...!!"
    try:
        cuenta=CuentasPorCobrar.objects.get(factura_id=idFactura)
        tabla=DetallesCuentasCobrar.objects.filter(cuenta=cuenta)
    except Exception as error:
        cuenta=None
        tabla=None
        print(error,cuenta,tabla)
    contexto={
        'factura':Factura.objects.get(id=idFactura),
        'usuario':user.usuario,
        'tabla':tabla,
        'cuenta':cuenta,
        'mensaje':mensaje,
        'user2': user.is_admin,
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
        'items': Items.objects.all(),
    }

    return render(request,'Cartera/registroCuenta.html',contexto)

def detallesCuentasCobrar(request,cuenta,jsones):
    mensaje=""
    user=myUsuario.objects.get(usuario=request.user)
    try:
        apertura = AperturaCaja.objects.filter(estado=False, usuario=request.user).last()
        for i in json.loads(jsones):
            if apertura:
                print(i["Id"], i['Detalles'], i['Fechas'], i['Pagos'], i['Saldos'])
                fecha = datetime.strptime(i['Fechas'], '%d/%m/%Y')

                if i["Id"] == '1':
                    detalle = DetallesCuentasCobrar(cuenta=cuenta, caja=apertura, n_pago=i["Id"],empresa=user.empresa,
                                                    detalles=i['Detalles'], fecha_esperada=fecha, fecha_pago=fecha,
                                                    abono=i['Pagos'], saldo=i['Saldos'], estado=True)
                else:
                    detalle = DetallesCuentasCobrar(cuenta=cuenta, n_pago=i["Id"], detalles=i['Detalles'],empresa=user.empresa,
                                                    fecha_esperada=fecha, abono=i['Pagos'], saldo=i['Saldos'])

                detalle.save()
                mensaje="La cuenta se registro Correctamente..!!"
                print('se registro una cuenta', 'Codigo de la cuenta:', detalle.id)
            else:
                mensaje = "Al parecer no hay caja aperturada..!!"
                cuenta.delete()
                print('se elimino la cuenta')
    except Exception as error:
        mensaje = "Al parecer no hay caja aperturada..!!"
        cuenta.delete()
        print("no hay caja no se puede guardar.. la cuenta fue eliminada..!!",error)
    return mensaje

def TablaPagosCuentasCobrar(request,idCuenta):
    user=myUsuario.objects.get(usuario=request.user)
    cuenta=CuentasPorCobrar.objects.get(id=idCuenta)
    contexto={
        'cuenta':cuenta,
        'detalles':DetallesCuentasCobrar.objects.filter(cuenta=cuenta).order_by('n_pago'),
        'reporte':Reportes.objects.filter(empresa=user.empresa).last(),
        'user2': user.is_admin,
    }
    return render_to_pdf('Cartera/repCuentasCobrar.html',contexto)

def PagarCuentaCobrar(request,idDetalle):
    apertura = AperturaCaja.objects.filter(estado=False, usuario=request.user).last()
    detalle=DetallesCuentasCobrar.objects.get(id=idDetalle)
    detalle.estado=True
    detalle.caja=apertura
    detalle.fecha_pago=datetime.now().date()
    if detalle.saldo <= 0.00:
        cuenta=CuentasPorCobrar.objects.get(id=detalle.cuenta_id)
        cuenta.estado=True
        factura=cuenta.factura
        factura.estado_por_pagar=True
        factura.save()
        print("ultimo pago..!! liquidando cuenta...")
        cuenta.save()
    detalle.save()
    return HttpResponseRedirect("/cartera/cuentasCobrar/registro/%s/"%str(detalle.cuenta.factura.id))

def PagarCuentaCobrarPPT(request):
    apertura = AperturaCaja.objects.filter(estado=False, usuario=request.user).last()
    if request.POST:
        idDetalle = request.POST['det']
        detalle = DetallesCuentasCobrar.objects.get(id=idDetalle)
        detalle.estado = True
        detalle.caja = apertura
        detalle.abono=request.POST['ppt'].replace(",",".")
        detalle.fecha_pago = datetime.now().date()
        detalle.detalles=request.POST['detallesppt']
        saldo = detalle.saldo = float(request.POST['saldoppt'].replace(",","."))
        detalle.save()
        cuentaCobrar(detalle.cuenta_id,saldo,detalle.n_pago,float(request.POST['parcial'].replace(",",".")))
        if detalle.saldo <= 0.00:
            cuenta=CuentasPorCobrar.objects.get(id=detalle.cuenta_id)
            cuenta.estado=True
            factura=cuenta.factura
            factura.estado_por_pagar=True
            factura.save()
            print("ultimo pago..!! liquidando cuenta...")
            cuenta.save()
        return HttpResponseRedirect("/cartera/cuentasCobrar/registro/%s/"%str(detalle.cuenta.factura.id))

def cuentaCobrar(idCuenta,saldos,npago,parcial):
    cuenta=CuentasPorCobrar.objects.get(id=idCuenta)
    detalles=DetallesCuentasCobrar.objects.filter(cuenta=cuenta,estado=False)
    parcial=parcial
    for detalle in detalles:
        npago+=1
        saldo = saldos - parcial
        saldos=saldo
        print(saldo,parcial)
        if detalle.n_pago >= npago:
            detalle.abono=parcial
            detalle.saldo=saldo
            detalle.n_pago=npago
            detalle.save()

def ReciboPgoCuentaCobrar(request,idDetalle):
    user = myUsuario.objects.get(usuario=request.user)
    detalle=DetallesCuentasCobrar.objects.get(id=idDetalle)
    ciudad=user.empresa.parroquia.lugar.nombre
    contexto={
        'detalle':detalle,
        'reporte':Reportes.objects.filter(empresa=user.empresa).last(),
        'cuenta':detalle.cuenta,
        'fecha':datetime.now().date(),
        'ciudad':ciudad,
        'user2': user.is_admin,
    }
    return render_to_pdf('Cartera/repPagoCuentaCobrar.html',contexto)

def Devoluciones(request):
    user = myUsuario.objects.get(usuario=request.user)
    contexto = {
        'usuario': request.user,
        'empresa': user.empresa,
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': Funciones.objects.all().order_by("id"),
        'items': Items.objects.all(),
        'user2': user.is_admin,
    }
    return render(request,'',contexto)

def cajasUsuariosEmpresa(request):
    user = myUsuario.objects.get(usuario=request.user)
    cierres=CierreCaja.objects.filter(empresa=user.empresa)
    aperturas=AperturaCaja.objects.filter(empresa=user.empresa,estado=False)
    contexto = {
        'usuario': request.user,
        'empresa': user.empresa,
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': Funciones.objects.all().order_by("id"),
        'items': Items.objects.all(),
        'user2': user.is_admin,
        'cierres':cierres,
        'aperturas':aperturas,
    }
    return render(request, 'Cartera/CajaUsuarioEmpresa.html', contexto)


