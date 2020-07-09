import json

from django.db.models import Sum
from django.shortcuts import render, HttpResponse

# Create your views here.
from CONFIGURACION.models import DatosEmpresa, Permiso, Items
from CONFIGURACION.views import funciones_usuario
from DOCUMENTOS_ELECTRONICOS.models import Factura
from INVENTARIO.models import Compra
from SRI.models import Formularios
from TALENTO_HUMANO.models import Anio
from USERS.models import myUsuario


def formulario104AMesual(request):
    user = myUsuario.objects.get(usuario=request.user)
    empresa = user.empresa
    anio = Anio.objects.filter(empresa=empresa).order_by('anio')
    contexto = {
        'empresa': empresa,
        'anio': anio,
        'usuario': request.user,
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
        'items': Items.objects.all(),
        'user': user.is_admin,
    }

    return render(request, 'sri/104AMensual.html',contexto)



## VISTA PARA CALCULOS DEL FORMULARIO 104A MENSUAL
def formulario104ObtenerVentas(request):
    user = myUsuario.objects.get(usuario=request.user)
    anio = request.GET['anio']
    mes = request.GET['mes']
    print(anio,mes)
    totalFacturasVentas =0
    totalDocumentosCompras=0
    valorTotal= IvaTotal= SubtotalrTotal=IvaCompras=SubtotalCompras=0.00

    ##PROCESOS PARA LAS VENTAS
    facturas = Factura.objects.filter(estado= 'AUTORIZADO', empresa=user.empresa, fecha__month=mes, fecha__year=anio,ambiente=2)
    print(facturas)
    if facturas:
        SubtotalrTotal = float(facturas.aggregate(Sum('subtotal_iva'))['subtotal_iva__sum'])
        IvaTotal = round(SubtotalrTotal*0.12, 2)
        valorTotal = SubtotalrTotal + IvaTotal
        totalFacturasVentas = facturas.count()
    totalFacturasVentasAnuladas = Factura.objects.filter(estado= 'ANULADO', empresa=user.empresa, fecha__month=mes, fecha__year=anio).count()
    print(valorTotal,IvaTotal,  SubtotalrTotal)

    ##PROCESOS PARA LAS COMPRAS
    compras = Compra.objects.filter(empresa=user.empresa, fecha_emision__month=mes, fecha_emision__year=anio)
    if compras:
        SubtotalCompras = float(compras.aggregate(Sum('subtotal_iva'))['subtotal_iva__sum'])
        IvaCompras = round(SubtotalCompras * 0.12,2)
        totalDocumentosCompras = compras.count()
    print(totalDocumentosCompras)
    print (SubtotalCompras)

    totales = {
        "subtotal":round(SubtotalrTotal,2),
        "iva" : round(IvaTotal,2),
        "totales":round(valorTotal,2),
        'nFacturas':totalFacturasVentas + totalFacturasVentasAnuladas,
        'nFacturasAnuladas':totalFacturasVentasAnuladas,

        'SubtotalCompras':SubtotalCompras,
        'IvaCompras':IvaCompras,
        'nCompras': totalDocumentosCompras,
    }
    return HttpResponse(json.dumps(totales))



def formulario104ASemestral(request):
    return render(request, 'sri/104ASemestral.html')


def formulario104(request):
    user = myUsuario.objects.get(usuario=request.user)
    anio= Anio.objects.get(activado=True, empresa= user.empresa)

    contexto = {
        'empresa': user.empresa,
        'anio':anio,
        'usuario': request.user,
        'permisos': Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
        'items': Items.objects.all(),
        'user': user.is_admin,
    }
    return render(request, 'sri/104.html', contexto)