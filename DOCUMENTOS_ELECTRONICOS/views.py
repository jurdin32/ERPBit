# -*- coding: utf-8 -*-
import datetime
import json

from django.core import serializers
from django.db.models.aggregates import Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from lxml.html.clean import unicode

from CARTERA.models import AperturaCaja
from CLIENTES.models import Cliente, TipoIndentificacion
from CONFIGURACION.models import Reportes, Permiso, Funciones, Items, Lugares
from CONFIGURACION.views import funciones_usuario
from DOCUMENTOS_ELECTRONICOS.models import *
from DOCUMENTOS_ELECTRONICOS.sri import claveAcceso
from DOCUMENTOS_ELECTRONICOS.tasks import *
from DOCUMENTOS_ELECTRONICOS.xmls import *
from INVENTARIO.models import DetalleProProveedor, Proveedor, Compra
from INVENTARIO.reportes import render_to_pdf, render_to_pdf_factura
from TRANSPORTE.models import ConductorTrans, EmpresaTransporte, VehiculoTrans
from USERS.models import myUsuario
import copy


# FACTURAS
def FacturasView(request):
    user = myUsuario.objects.get(usuario=request.user)
    facturas = Factura.objects.filter(tipo="FACTURA", empresa=user.empresa).order_by("-id")
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario': request.user,
        'facturas': facturas,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    print(facturas)
    return render(request, 'Docuementos_Electronicos/facturas.html', contexto)


def ProfromasView(request):
    user = myUsuario.objects.get(usuario=request.user)
    facturas = Factura.objects.filter(tipo="PROFORMA", cliente__empresa=user.empresa).order_by("-id")
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario': request.user,
        'facturas': facturas,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    print(facturas)
    return render(request, 'Docuementos_Electronicos/proformas.html', contexto)


def enviarProforma(request, idFactura):
    factura = Factura.objects.get(id=idFactura)
    enviarPDF.delay(factura)
    return HttpResponseRedirect('/documentos_electronicos/Proformas/')


@csrf_exempt
def detallesFactura(request, idFactura):
    mensaje = ""
    error = ""
    usuario = myUsuario.objects.get(usuario=request.user)
    if request.POST:
        print(request.POST)
        try:
            detalle = DetallesFactura(factura_id=idFactura,
                                      producto_id=request.POST['producto'],
                                      cantidad=float(request.POST['cantidad']),
                                      subtotal_0=float(request.POST['sub0']),
                                      subtotal_iva=float(request.POST['sub12']),
                                      subtotal=float(request.POST['sub']),
                                      descuento=0, iva=float(request.POST['iva']),
                                      ice=float(request.POST['ice']),
                                      irbpnr=float(request.POST['Irbpnr']),
                                      total=float(request.POST['total'].replace(",", ".")))
            detalle.save()
            return HttpResponse("ok")
        except Exception as error:
            error = "Error al generar la factura"
            print(error)
            factura = Factura.objects.get(id=idFactura)
            factura.delete()
            return HttpResponse("no")
    else:
        factura = Factura.objects.get(id=idFactura)
        contexto = {
            'factura': factura,
            'detalles': DetallesFactura.objects.filter(factura_id=idFactura),
            'reporte': Reportes.objects.filter(empresa=usuario.empresa).last(),
            'user2': usuario.is_admin,
            'error':error,
        }
        return render_to_pdf_factura('Docuementos_Electronicos/repFactura.html', contexto, factura)

def reciboFactura(request, idFactura):
    mensaje = ""
    error = ""
    usuario = myUsuario.objects.get(usuario=request.user)
    if request.POST:
        print(request.POST)
        try:
            detalle = DetallesFactura(factura_id=idFactura,
                                      producto_id=request.POST['producto'],
                                      cantidad=float(request.POST['cantidad']),
                                      subtotal_0=float(request.POST['sub0']),
                                      subtotal_iva=float(request.POST['sub12']),
                                      subtotal=float(request.POST['sub']),
                                      descuento=0, iva=float(request.POST['iva']),
                                      ice=float(request.POST['ice']),
                                      irbpnr=float(request.POST['Irbpnr']),
                                      total=float(request.POST['total'].replace(",", ".")))
            detalle.save()
            return HttpResponse("ok")
        except Exception as error:
            error = "Error al generar la factura"
            print(error)
            factura = Factura.objects.get(id=idFactura)
            factura.delete()
            return HttpResponse("no")
    else:
        factura = Factura.objects.get(id=idFactura)
        contexto = {
            'factura': factura,
            'detalles': DetallesFactura.objects.filter(factura_id=idFactura),
            'reporte': Reportes.objects.filter(empresa=usuario.empresa).last(),
            'user2': usuario.is_admin,
            'error': error,
        }
        return render_to_pdf_factura('Docuementos_Electronicos/recibo.html', contexto, factura)


@csrf_exempt
def detallesProforma(request, idFactura):
    usuario = myUsuario.objects.get(usuario=request.user)

    if request.POST:
        print(request.POST)
        try:
            detalle = DetallesFactura(factura_id=idFactura,
                                      producto_id=request.POST['producto'],
                                      cantidad=request.POST['cantidad'],
                                      subtotal_0=float(request.POST['sub0']),
                                      subtotal_iva=float(request.POST['sub12']),
                                      subtotal=float(request.POST['sub']),
                                      descuento=0, iva=float(request.POST['iva']),
                                      ice=float(request.POST['ice']),
                                      irbpnr=float(request.POST['Irbpnr']),
                                      total=float(request.POST['total'].replace(",", ".")))
            detalle.save()
            return HttpResponse("ok")
        except Exception as error:
            print(error)
            factura = Factura.objects.get(id=idFactura)
            factura.delete()
            print("La Factura fue eliminada..!!")
            return HttpResponse("no")
    else:
        factura = Factura.objects.get(id=idFactura)
        contexto = {
            'factura': factura,
            'detalles': DetallesFactura.objects.filter(factura_id=idFactura),
            'reporte': Reportes.objects.filter(empresa=usuario.empresa).last(),
            'user2': usuario.is_admin,
        }
        return render_to_pdf_factura('Docuementos_Electronicos/repFactura.html', contexto, factura)


@csrf_exempt
def RegistroFacturasView(request):

    tipo = TipoComprobante.objects.get(nombre="FACTURA").codigo
    usuario = myUsuario.objects.get(usuario=request.user)
    fact=Factura.objects.filter(tipo="FACTURA", empresa=usuario.empresa)
    contador = fact.filter(ambiente=2).count()+2
    print("Nùmero de facturas: ", contador)
    DATOS = None
    secuencia = 0
    secuencial = ""
    try:
        DATOS = DatosDocumentos.objects.get(empresa=usuario.empresa, estado=True)
        secuencia = DATOS.secuencial
        print("ambiente registrado:",DATOS.ambiente.codigo)
        if int(DATOS.ambiente.codigo)==1:
            print("ambiente de pruebas......................................*")
            contador = fact.filter(ambiente=1).count()
        print(secuencia, contador)
        secuencial = str.zfill(str(contador + secuencia), 9)
    except:
        return HttpResponseRedirect("/documentos_electronicos/configuracion/")

    print("secuencial: ", secuencial)
    apertura = None
    try:
        apertura = AperturaCaja.objects.get(estado=False, usuario=request.user)
    except:
        return HttpResponseRedirect("/cartera/apertura/")

    if request.POST:
        contado = request.POST['tipoventa']
        if contado == "CONTADO":
            contado = True
        else:
            contado = False
        try:
            factura = Factura(contado=contado, diasPlazo=request.POST['dias'], usuario=request.user, empresa=usuario.empresa,
                              secuencial=secuencial, caja=apertura,
                              tipo="FACTURA", datosFactura=DATOS, cliente_id=request.POST['cliente'],
                              subtotal_0=request.POST['sutotal0'],
                              puntoEmision=DATOS.codigoEstablecimiento.codigo,
                              codigoEstablecimiento=DATOS.puntoEmision.codigo,
                              ambiente=DATOS.ambiente.codigo,
                              subtotal_iva=request.POST['subtotal12'], subtotal=request.POST['subtotal'], descuento=0,
                              iva=request.POST['iva'], ice=request.POST['ice'],
                              irbpnr=request.POST['irbpnr'], total=request.POST['total'], clave_acceso="", estado="")
            factura.save()
            fecha = factura.fecha.strftime("%d%m%Y")
            clave_acceso = claveAcceso(fecha, tipo, factura.datosFactura.empresa.ruc, factura.ambiente,
                                       factura.codigoEstablecimiento, factura.puntoEmision, secuencial, "00000000", '1')
            print("Clave de acceso: ", clave_acceso, len(clave_acceso))
            factura.clave_acceso = clave_acceso
            factura.save()

            return HttpResponse(factura.id)
        except Exception as error:
            print(error)
            return HttpResponse(-1)
    permisos=Permiso.objects.filter(grupo=usuario.grupo)
    contexto = {
        'usuario': request.user,
        'productos': DetalleProProveedor.objects.filter(producto__estado=True, producto__empresa=usuario.empresa),
        'clientes': Cliente.objects.filter(empresa=usuario.empresa,estado=True),
        'reportes': Reportes.objects.filter(empresa=usuario.empresa).last(),
        'consumidor': Cliente.objects.get(ruc='9999999999999', empresa=usuario.empresa),
        'secuencial': secuencial,
        'empresa': usuario.empresa,
        'datos': DATOS,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': usuario.is_admin,
        'tiposIdentificacion':TipoIndentificacion.objects.all(),
        'paises':Lugares.objects.filter(pais=True),
    }
    return render(request, 'Docuementos_Electronicos/registroFactura.html', contexto)


@csrf_exempt
def RegistroProformasView(request):
    usuario = myUsuario.objects.get(usuario=request.user)
    contador = Factura.objects.filter(tipo="PROFORMA", usuario__myusuario__empresa=usuario.empresa).count()
    print("Número de Proformas: ", contador)
    DATOS = DatosDocumentos.objects.get(empresa=usuario.empresa, estado=True)
    secuencia = DATOS.secuenciaProforma
    secuencial = str.zfill(str(contador + secuencia), 12)
    print("secuencial: ", secuencial)
    if request.POST:
        try:
            factura = Factura(usuario=request.user, empresa=usuario.empresa, secuencial=request.POST['secuencia'], tipo="PROFORMA",
                              datosFactura=DATOS,
                              cliente_id=request.POST['cliente'], subtotal_0=request.POST['sutotal0'],
                              puntoEmision=DATOS.puntoEmision.codigo,
                              codigoEstablecimiento=DATOS.codigoEstablecimiento.codigo, ambiente=0,
                              subtotal_iva=request.POST['subtotal12'], subtotal=request.POST['subtotal'], descuento=0,
                              iva=request.POST['iva'],
                              ice=request.POST['ice'], irbpnr=request.POST['irbpnr'], total=request.POST['total'],
                              clave_acceso="", estado="")
            factura.save()
            return HttpResponse(factura.id)
        except Exception as error:
            print(error)
            return HttpResponse(-1)
    permisos=Permiso.objects.filter(grupo=usuario.grupo)
    contexto = {
        'usuario': request.user,
        'productos': DetalleProProveedor.objects.filter(producto__estado=True, producto__empresa=usuario.empresa),
        'clientes': Cliente.objects.filter(empresa=usuario.empresa,estado=True),
        'reportes': Reportes.objects.filter(empresa=usuario.empresa).last(),
        'consumidor': Cliente.objects.get(ruc='9999999999999', empresa=usuario.empresa),
        'secuencial': secuencial,
        'empresa': usuario.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all(),
        'user2': usuario.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/registroProforma.html', contexto)


def facturaXML(request, n):
    factura = Factura.objects.get(id=n)
    contabilidad = "NO"
    if factura.datosFactura.empresa.obligado_llevar_contabilidad:
        contabilidad = "SI"
    print()
    nombre = "%s %s" % (factura.cliente.nombre, factura.cliente.apellido)
    nombre = nombre.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
    if nombre == " ":
        nombre = factura.cliente.razonSocial.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó",
                                                                                                           "O").replace(
            "Ú", "U")
    print(nombre)
    fact = {
        'factura': {
            'infoTributaria': {
                'ambiente': factura.ambiente,
                'tipoEmision': factura.datosFactura.tipoEmision,
                'razonSocial': factura.datosFactura.empresa.razonSocial,
                'nombreComercial': factura.datosFactura.empresa.nombreComercial,
                'ruc': factura.datosFactura.empresa.ruc,
                'claveAcceso': factura.clave_acceso,
                'codDoc': "01",
                'estab': factura.codigoEstablecimiento,
                'ptoEmi': factura.puntoEmision,
                'secuencial': factura.secuencial,
                'dirMatriz': factura.datosFactura.empresa.direccionMatriz,
            },
            'infoFactura': {
                'fechaEmision': factura.fecha.strftime("%d/%m/%Y"),
                'dirEstablecimiento': factura.datosFactura.empresa.direccionMatriz,
                'obligadoContabilidad': contabilidad,
                'tipoIdentificacionComprador': factura.cliente.tipo_identificacion.codigo,
                'razonSocialComprador': nombre,
                'identificacionComprador': factura.cliente.ruc,
                'direccionComprador': factura.cliente.direccion,
                'totalSinImpuestos': round(factura.subtotal, 2),
                'totalDescuento': round(factura.descuento, 2),
                'totalConImpuestos': {
                    'totalImpuesto':{
                        'codigo':2,
                        'codigoPorcentaje':2,
                        'baseImponible':factura.subtotal_iva,
                        'valor':factura.iva,
                    }
                },
                'propina': 0.00,
                'importeTotal': factura.total,
                'moneda': "DOLAR",
            },
            'detalles': "xt",

        }
    }
    impuestos = cadenaIMPUESTO(factura)

    detalles = cadenaDetalles(factura)
    contexto = {
        'factura': factura,
        'detalles': DetallesFactura.objects.filter(factura_id=n),
        'reporte': Reportes.objects.filter(empresa=factura.empresa).last(),
    }
    render_to_pdf_factura('Docuementos_Electronicos/repFactura.html', contexto, factura)
    xml = documentosXML(fact, impuestos, detalles, factura)
    return HttpResponse(xml, content_type="Application/xml")


def facturaJSON(request, n):
    usuario=myUsuario.objects.get(usuario=request.user)
    factura = Factura.objects.get(id=n)
    respuesta = json_sri(str(factura.clave_acceso), int(factura.datosFactura.ambiente.codigo),
                         'media/Facturacion/xml/response/resp-' + factura.clave_acceso + '.json')

    try:
        factura.estado = respuesta['autorizaciones']['autorizacion'][0]['estado']
        factura.save()
        contexto = {
            'factura': factura,
            'detalles': DetallesFactura.objects.filter(factura_id=n),
            'reporte': Reportes.objects.filter(empresa=usuario.empresa).last(),
        }
        render_to_pdf_factura('Docuementos_Electronicos/repFactura.html', contexto, factura)
    except Exception as error:
        print(error)
    return HttpResponse(str(respuesta), content_type="Application/json")


def cadenaDetalles(factura):
    datos = ""
    todoimpuesto = Tarifas.objects.filter(usado_en_retencion=False)
    ices = ""
    irbpnr = ""
    ddddd=DetallesFactura.objects.filter(factura=factura)
    print(ddddd.count())
    for detalle in DetallesFactura.objects.filter(factura=factura):
        iva = todoimpuesto.get(codigo=detalle.tarifa_iva)

        print("codigo de iva",iva.codigo)
        if int(detalle.tarifa_ice) > 0:
            ice = todoimpuesto.get(codigo=detalle.tarifa_ice)
        if int(detalle.tarifa_irbpnr) > 0:
            irbpnr = todoimpuesto.get(codigo=detalle.tarifa_irbpnr)
        print("datos de la linea", "iva impuesto:", iva.impuesto.codigo, 'codigo tarifa', str(iva.codigo),
              'porcentaje: ', str(iva.porcentaje), 'importe', str(detalle.subtotal_iva))
        sub = 0.00
        if detalle.iva == 0:
            sub = detalle.subtotal_0
        else:
            sub = detalle.subtotal_iva
        imp = """
            <impuesto>
                <codigo>%s</codigo>
                <codigoPorcentaje>%s</codigoPorcentaje>
                <tarifa>%s</tarifa>
                <baseImponible>%s</baseImponible>
                <valor>%s</valor>
            </impuesto>""" % (
            str(detalle.codigo_iva), str(detalle.tarifa_iva), str(iva.porcentaje), str(sub), str(detalle.iva))

        if int(detalle.tarifa_ice) > 0:
            ices = """
            <impuesto>
                <codigo>%s</codigo>
                <codigoPorcentaje>%s</codigoPorcentaje>
                <tarifa>%s</tarifa>
                <baseImponible>%s</baseImponible>
                <valor>%s</valor>
            </impuesto>""" % (
                str(detalle.codigo_ice), str(detalle.tarifa_ice), str(ice.porcentaje), str(detalle.subtotal),
                str(detalle.ice))

        if int(detalle.tarifa_irbpnr) > 0:
            ices = """<impuesto>
                        <codigo>%s</codigo>
                        <codigoPorcentaje>%s</codigoPorcentaje>
                        <tarifa>%s</tarifa>
                        <baseImponible>%s</baseImponible>
                        <valor>%s</valor>
                    </impuesto>""" % (
                str(detalle.codigo_irbpnr), str(detalle.tarifa_irbpnr), str(irbpnr.porcentaje), str(detalle.subtotal),
                str(detalle.irbpnr))
        print(imp)
        try:
            datos += u"""<detalle>
                      <codigoPrincipal>%s</codigoPrincipal>
                      <codigoAuxiliar>%s</codigoAuxiliar>
                      <descripcion>%s/%s x %s x %s</descripcion>
                      <cantidad>%s</cantidad>
                      <precioUnitario>%s</precioUnitario>
                      <descuento>0.00</descuento>
                      <precioTotalSinImpuesto>%s</precioTotalSinImpuesto>
                      <impuestos>%s
                      %s
                      %s
                      </impuestos>
                      </detalle>""" % (str(detalle.producto.id), detalle.producto.producto.cod_referencia.encode('utf8'),
                                       detalle.producto.producto.nombre.encode('utf8'),
                                       detalle.producto.producto.marca.nombre, detalle.producto.producto.medida,
                                       detalle.producto.producto.peso,
                                       detalle.cantidad, round(detalle.producto.pvp,2), round(detalle.subtotal,2), imp, ices, irbpnr)
            print("entro aqui a generar el detalle del xml")
        except Exception as error:
            print("aqui se genera una exception", error)
            datos += """<detalle>
                                  <codigoPrincipal>%s</codigoPrincipal>
                                  <codigoAuxiliar>%s</codigoAuxiliar>
                                  <descripcion>%s / %s</descripcion>
                                  <cantidad>%s</cantidad>
                                  <precioUnitario>%s</precioUnitario>
                                  <descuento>0.00</descuento>
                                  <precioTotalSinImpuesto>%s</precioTotalSinImpuesto>
                                  <impuestos>%s
                                  %s
                                  %s
                                  </impuestos>
                                  </detalle>""" % (
                str(detalle.producto.id), detalle.producto.producto.cod_referencia.encode('utf8'),
                detalle.producto.producto.nombre.encode('utf8'),
                detalle.producto.detalles.encode('utf8')[0:100], detalle.cantidad, round(detalle.producto.pvp,2),
                round(detalle.subtotal,2), imp, ices, irbpnr)
    # print(datos)
    return datos


def cadenaIMPUESTO(factura):
    impuesto = 2
    impuesto2 = 3
    impuesto3 = 5
    datos = impuestoIVA(factura, impuesto) + impuestoICE(factura, impuesto2) + impuestoIRBPNR(factura, impuesto3)
    return datos


def impuestoIVA(factura, codigoImpuesto):
    datos = ""
    for tarifas in Tarifas.objects.filter(impuesto__codigo=codigoImpuesto,usado_en_retencion=False):
        detalles = DetallesFactura.objects.filter(factura=factura, codigo_iva=codigoImpuesto, tarifa_iva=tarifas.codigo)
        print(tarifas)
        if detalles:
            baseImponible = 0
            total = 0
            for det in detalles:
                print("entra por el iva.........................")
                if det.iva == 0:
                    # baseImponible+=float(0.00)
                    baseImponible += float(det.subtotal_0)
                    print("esta entradndo ...................", float(det.subtotal_0))
                else:
                    print("entra por iva diferente de 0 -----------------------------------")
                    baseImponible += float(det.subtotal_iva)
                    total += float(det.iva)
            datos += '''<totalImpuesto>
                    <codigo>%s</codigo>
                    <codigoPorcentaje>%s</codigoPorcentaje>
                    <baseImponible>%s</baseImponible>
                    <valor>%s</valor>
                    </totalImpuesto>''' % (codigoImpuesto, tarifas.codigo, round(baseImponible, 2), round(total, 2))
    return datos


def impuestoICE(factura, codigoImpuesto):
    datos = ""
    for tarifas in Tarifas.objects.filter(impuesto__codigo=codigoImpuesto,usado_en_retencion=False):
        detalles = DetallesFactura.objects.filter(factura=factura, codigo_ice=codigoImpuesto, tarifa_ice=tarifas.codigo)
        if detalles:
            baseImponible = 0
            for det in detalles:

                total = 0
                if int(det.tarifa_ice) == -1:
                    pass
                    print("esta con ice -1", det.subtotal)
                else:
                    baseImponible += float(det.subtotal)
                    total = +det.ice
                    datos += '''<totalImpuesto>
                                <codigo>%s</codigo>
                                <codigoPorcentaje>%s</codigoPorcentaje>
                                <baseImponible>%s</baseImponible>
                                <valor>%s</valor>
                                </totalImpuesto>''' % (
                        codigoImpuesto, tarifas.codigo, round(baseImponible, 2), round(total, 2))
    return datos


def impuestoIRBPNR(factura, codigoImpuesto):
    datos = ""
    for tarifas in Tarifas.objects.filter(impuesto__codigo=codigoImpuesto,usado_en_retencion=False):
        detalles = DetallesFactura.objects.filter(factura=factura, codigo_ice=codigoImpuesto, tarifa_ice=tarifas.codigo)
        if detalles:
            baseImponible = 0
            for det in detalles:
                total = 0
                if int(det.tarifa_irbpnr) == -1:
                    pass
                    print("esta con ice -1", det.subtotal)
                else:
                    baseImponible += float(det.subtotal)
                    total = +det.irbpnr
                    datos += '''<totalImpuesto>
                                <codigo>%s</codigo>
                                <codigoPorcentaje>%s</codigoPorcentaje>
                                <baseImponible>%s</baseImponible>
                                <valor>%s</valor>
                                </totalImpuesto>''' % (
                        codigoImpuesto, tarifas.codigo, round(baseImponible, 2), round(total, 2))
    return datos


def detalles(request, id):
    data = {}
    item = []
    factura = Factura.objects.get(id=id)
    detales = DetallesFactura.objects.filter(factura=factura)

    for det in detales:
        try:
            item.append({
                'id': det.producto.id,
                'cantidad': det.cantidad,
                'codRef': det.producto.producto.cod_referencia,
                'producto': det.producto.producto.nombre + " / " + det.producto.producto.marca.nombre + "/" + det.producto.producto.categoria.categoria + " x " +
                            det.producto.producto.peso + " x " + det.producto.producto.medida
            })
        except Exception as error:
            item.append({
                'id': det.producto.id,
                'cantidad': det.cantidad,
                'codRef': det.producto.producto.cod_referencia,
                'producto': det.producto.producto.nombre + " / " + det.producto.detalles[0:100]
            })
    data['items'] = item
    return JsonResponse(data)


# GUIAS DE REMISION
def GuiaRemisionView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario': request.user,
        'empresa': user.empresa,
        'guias': GuiaRemision.objects.filter(usuario=request.user).order_by("-id"),
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
    }
    return render(request, 'Docuementos_Electronicos/guiasRemision.html', contexto)


def RegistroGuiaRemisionView(request):
    mensaje=""
    error=""
    user = myUsuario.objects.get(usuario=request.user)
    guiaaa=GuiaRemision.objects.filter(empresa=user.empresa)
    contador = guiaaa.filter(ambiente=2).count()

    DATOS = DatosDocumentos.objects.get(estado=True, empresa=user.empresa)
    tipo = TipoComprobante.objects.get(nombre="GUÍA DE REMISIÓN").codigo
    secuencia = DatosDocumentos.objects.get(estado=True, empresa=user.empresa).secuencialGuias
    secuencial = str.zfill(str(contador + secuencia), 9)

    if int(DATOS.ambiente.codigo) == 1:
        print("ambiente de pruebas......................................*")
        contador = guiaaa.filter(ambiente=1).count()
        secuencial = str.zfill(str(contador + secuencia), 9)
    print(secuencia, contador)

    guia = None

    if request.POST:
        print(request.POST)
        try:
            print("ambiente registrado:", DATOS.ambiente.codigo)


            vehiculo = VehiculoTrans.objects.get(id=request.POST['vehiculo'])
            factura = Factura.objects.get(secuencial=request.POST['factura'])
            guia = GuiaRemision(usuario=request.user, empresa=user.empresa,
                                ambiente=DATOS.ambiente.codigo,
                                secuencial=secuencial,
                                datosGuia=DATOS, vehiculo=vehiculo,
                                puntoPartida=request.POST['puntoPartida'],
                                fachaIniTrans=request.POST['fechaSalida'],
                                fachaFinTrans=request.POST['fechaLLegada'],
                                observaciones=request.POST['observaciones'],
                                factura=factura,
                                motivoTraslado=request.POST['motivoTraslado'],
                                puntoLLegada=request.POST['puntoLLegada'],
                                docAduanero=request.POST['docAduanero'],
                                codEstablecimiento=request.POST['codEstablecimiento'],
                                clave_acceso="", estado="")
            guia.save()
            print("se registro la guia")
            fecha = guia.fecha.strftime("%d%m%Y")

            clave_acceso = claveAcceso(fecha, tipo, user.empresa.ruc, guia.ambiente, DATOS.codigoEstablecimiento.codigo,
                                       DATOS.puntoEmision.codigo, secuencial, "06060606", "1")

            guia.clave_acceso = clave_acceso
            guia.save()
            print("guia numero: ", guia.id)
            guiRemisionRide(request, guia.id)

            guiaRemisionXML(request, guia.id)

            mensaje="La Guia de remision se ha creado con exito."
        except Exception as error2:
            print("error detectado: ", error2)
            guia.delete()
            error="Al parecer hay un error al generar la guia, Revise y reinente..!!"

    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'conductores': ConductorTrans.objects.filter(estado=True, empresaTrans__empresa=user.empresa),
        'empresas': EmpresaTransporte.objects.filter(estado=True, empresa=user.empresa),
        'vehiculos': VehiculoTrans.objects.filter(estado=True, conductor__empresaTrans__empresa=user.empresa),
        'facturas': DatosDocumentos.objects.filter(empresa=user.empresa),
        'documentos': Factura.objects.filter(usuario__myusuario__empresa=user.empresa, tipo="FACTURA"),
        'reportes': Reportes.objects.filter(empresa=user.empresa).last(),
        'secuencial': secuencial,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
        'error':error,
        'mensaje':mensaje,


    }
    return render(request, 'Docuementos_Electronicos/registroGuiaRemision.html', contexto)


def guiRemisionRide(request, idGuia):
    guia = GuiaRemision.objects.get(id=idGuia)
    user = myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'guia': guia,
        'detalles': DetallesFactura.objects.filter(factura=guia.factura),
        'reporte': Reportes.objects.filter(empresa=user.empresa).last(),
        'permisos':permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    template = 'Docuementos_Electronicos/repGuiaRemision.html'
    return render_to_pdf(template, contexto)
    # return render(request,template, contexto)


def guiaRemisionXML(request, n):
    guiaRemision = GuiaRemision.objects.get(id=n)
    factura = guiaRemision.factura
    detalles = DetallesFactura.objects.filter(factura=factura)
    contabilidad = "NO"
    ncontribuyente = ""
    guia = {
        'guia': {
            'infoTributaria': {},
            'infoGuiaRemision': {
                'contribuyenteEspecial': ""
            },
            'destinatarios': {
                'destinatario': {
                    'docAduaneroUnico': "",
                    'codEstabDestino': "",
                }
            },

        }
    }

    if factura.datosFactura.empresa.obligado_llevar_contabilidad:
        contabilidad = "SI"
    if factura.datosFactura.empresa.contribuyenteEspecial:
        ncontribuyente = factura.datosFactura.empresa.contribuyenteEspecialNumero
        guia['guia']['infoGuiaRemision']['contribuyenteEspecial'] = ncontribuyente
    if guiaRemision.docAduanero != "SIN DOCUMENTO ADUANERO":
        guia['guia']['destinatarios']['destinatario']['docAduaneroUnico'] = guiaRemision.docAduanero,
    if guiaRemision.codEstablecimiento != "SIN CODIGO":
        guia['guia']['destinatarios']['destinatario']['codEstabDestino'] = guiaRemision.codEstablecimiento,
    print("aqui va")

    detallesGuia = ""
    for det in detalles:
        if det.producto.producto.tipo == "PRODUCTO":
            detallesGuia += '''<detalle><codigoInterno>%s</codigoInterno>
            <codigoAdicional>%s</codigoAdicional>
            <descripcion>%s/%s x %s x %s</descripcion>
            <cantidad>%s</cantidad></detalle>''' % (det.producto.id,
                                                    det.producto.producto.cod_referencia,
                                                    det.producto.producto.nombre,
                                                    det.producto.producto.marca.nombre,
                                                    det.producto.producto.peso,
                                                    det.producto.producto.medida,
                                                    str(det.cantidad))
        else:
            detallesGuia += '''<detalle><codigoInterno>%s</codigoInterno>
                        <codigoAdicional>%s</codigoAdicional>
                        <descripcion>%s</descripcion>
                        <cantidad>%s</cantidad></detalle>''' % (det.producto.id,
                                                                det.producto.producto.cod_referencia,
                                                                det.producto.producto.nombre,
                                                                str(det.cantidad))
    print("detalles guia: ", detallesGuia)

    guia = {
        'guia': {
            'infoTributaria': {
                'ambiente': guiaRemision.ambiente,
                'tipoEmision': '1',
                'razonSocial': guiaRemision.datosGuia.empresa.razonSocial,
                'nombreComercial': guiaRemision.datosGuia.empresa.nombreComercial,
                'ruc': guiaRemision.datosGuia.empresa.ruc,
                'claveAcceso': guiaRemision.clave_acceso,
                'codDoc': "06",
                'estab': guiaRemision.datosGuia.codigoEstablecimiento.codigo,
                'ptoEmi': guiaRemision.datosGuia.puntoEmision.codigo,
                'secuencial': guiaRemision.secuencial,
                'dirMatriz': guiaRemision.datosGuia.empresa.direccionMatriz,
            },
            'infoGuiaRemision': {
                'dirEstablecimiento': factura.datosFactura.empresa.direccionMatriz,
                'dirPartida': guiaRemision.puntoPartida,
                'razonSocialTransportista': guiaRemision.vehiculo.conductor.nombre + " " + guiaRemision.vehiculo.conductor.nombre,
                'tipoIdentificacionTransportista': guiaRemision.vehiculo.conductor.tipoIndentificacion.codigo,
                'rucTransportista': guiaRemision.vehiculo.conductor.ruc,
                'rise': "Contribuyente Regimen Simplificado RISE",
                'obligadoContabilidad': contabilidad,
                'fechaIniTransporte': guiaRemision.fachaIniTrans.strftime("%d/%m/%Y"),
                'fechaFinTransporte': guiaRemision.fachaFinTrans.strftime("%d/%m/%Y"),
                'placa': guiaRemision.vehiculo.placa,
            },
            'destinatarios': {
                'destinatario': {
                    'identificacionDestinatario': factura.cliente.ruc,
                    'razonSocialDestinatario': factura.cliente.nombre + " " + factura.cliente.apellido,
                    'dirDestinatario': factura.cliente.direccion,
                    'motivoTraslado': guiaRemision.motivoTraslado,
                    'ruta': guiaRemision.ruta,
                    'codDocSustento': "01",  # es de la factura
                    'numDocSustento': factura.codigoEstablecimiento + "-" + factura.puntoEmision + "-" + factura.secuencial,
                    'numAutDocSustento': factura.clave_acceso,
                    'fechaEmisionDocSustento': factura.fecha.strftime("%d/%m/%Y"),
                    'detalles': "xt",
                },
            },
        }
    }

    print("Iniciando la creacion del archivo..!!")
    xml = GuiaRemisionXML(guia, detallesGuia, guiaRemision)
    return HttpResponse(xml, content_type="Application/xml")


def guiRemisionRideSlug(request, codigo):
    user = myUsuario.objects.get(usuario=request.user)
    try:
        guia = GuiaRemision.objects.get(secuencial=codigo)
        contexto = {
            'guia': guia,
            'detalles': DetallesFactura.objects.filter(factura=guia.factura),
            'reporte': Reportes.objects.filter(empresa=user.empresa).last(),
            'user2': user.is_admin,
        }
        template = 'Docuementos_Electronicos/repGuiaRemision.html'
        return render_to_pdf(template, contexto)
    except:
        return redirect('/documentos_electronicos/registroGuiaRemision/')


def guiaRemisionJSON(request, n):
    guia = GuiaRemision.objects.get(id=n)
    respuesta = json_sri(str(guia.clave_acceso), int(guia.ambiente),
                         'media/Facturacion/xml/guias/response/' + guia.clave_acceso + '.json')
    print(respuesta)
    guia.estado = respuesta['autorizaciones']['autorizacion'][0]['estado']
    guia.save()

    return HttpResponse(str(respuesta), content_type="Application/json")



# NOTAS DE VENTA:
def notasVenta(request):
    user = myUsuario.objects.get(usuario=request.user)
    facturas = Factura.objects.filter(usuario__myusuario__empresa=user.empresa, tipo="NOTA DE VENTA").order_by("-id")
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario': request.user,
        'facturas': facturas,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/NotasVenta.html', contexto)


@csrf_exempt
def RegistroNotasView(request):
    usuario = myUsuario.objects.get(usuario=request.user)
    contador = Factura.objects.filter(tipo="NOTA DE VENTA", usuario__myusuario__empresa=usuario.empresa).count()
    print("Número de Notas de Venta: ", contador)
    DATOS = DatosDocumentos.objects.get(empresa=usuario.empresa, estado=True)
    secuencia = DATOS.secuencialNotaVenta
    secuencial = str.zfill(str(contador + secuencia), 15)
    print("secuencial: ", secuencial)
    if request.POST:
        contado = request.POST['tipoventa']
        if contado == "CONTADO":
            contado = True
        else:
            contado = False
        try:
            factura = Factura(contado=contado, diasPlazo=request.POST['dias'], usuario=request.user,
                              secuencial=secuencial, tipo="NOTA DE VENTA", datosFactura=DATOS,
                              cliente_id=request.POST['cliente'],
                              subtotal_0=request.POST['sutotal0'],
                              puntoEmision=DATOS.codigoEstablecimiento.codigo,
                              codigoEstablecimiento=DATOS.puntoEmision.codigo,
                              ambiente=DATOS.ambiente.codigo,
                              subtotal_iva=request.POST['subtotal12'], subtotal=request.POST['subtotal'], descuento=0,
                              iva=request.POST['iva'], ice=request.POST['ice'],
                              irbpnr=request.POST['irbpnr'], total=request.POST['total'], clave_acceso="", estado="")
            factura.save()
            return HttpResponse(factura.id)
        except Exception as error:
            print(error)
            return HttpResponse(-1)
    permisos=Permiso.objects.filter(grupo=usuario.grupo)
    contexto = {
        'usuario': request.user,
        'productos': DetalleProProveedor.objects.filter(producto__estado=True, producto__empresa=usuario.empresa),
        'clientes': Cliente.objects.filter(empresa=usuario.empresa),
        'reportes': Reportes.objects.filter(empresa=usuario.empresa).last(),
        'consumidor': Cliente.objects.get(ruc='9999999999999', empresa=usuario.empresa),
        'secuencial': secuencial,
        'empresa': usuario.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': usuario.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/registroNotaVenta.html', contexto)


@csrf_exempt
def detallesNotaVenta(request, idFactura):
    usuario = myUsuario.objects.get(usuario=request.user)
    if request.POST:
        print(request.POST)
        try:
            detalle = DetallesFactura(factura_id=idFactura,
                                      producto_id=request.POST['producto'],
                                      cantidad=request.POST['cantidad'],
                                      subtotal_0=float(request.POST['sub0']),
                                      subtotal_iva=float(request.POST['sub12']),
                                      subtotal=float(request.POST['sub']),
                                      descuento=0, iva=float(request.POST['iva']),
                                      ice=float(request.POST['ice']),
                                      irbpnr=float(request.POST['Irbpnr']),
                                      total=float(request.POST['total'].replace(",", ".")))
            detalle.save()
            return HttpResponse("ok")
        except Exception as error:
            print(error)
            factura = Factura.objects.get(id=idFactura)
            factura.delete()
            print("La Factura fue eliminada..!!")
            return HttpResponse("no")
    else:
        factura = Factura.objects.get(id=idFactura)
        contexto = {
            'factura': factura,
            'detalles': DetallesFactura.objects.filter(factura_id=idFactura),
            'reporte': Reportes.objects.filter(empresa=usuario.empresa).last(),
            'user2': usuario.is_admin,
        }
        return render_to_pdf_factura('Docuementos_Electronicos/repFactura.html', contexto, factura)


def RetencionesView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario':request.user,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'retenciones': Retencion.objects.filter(empresa=user.empresa),
        'user2': user.is_admin,
    }

    return render(request, 'Docuementos_Electronicos/retenciones.html', contexto)


def RegistroRetencionesView(request, id):
    mensaje = error = ""
    usuario = myUsuario.objects.get(usuario=request.user)
    documentos = DatosDocumentos.objects.filter(empresa=usuario.empresa, estado=True).last()
    rett=Retencion.objects.filter(empresa=usuario.empresa)
    contador = rett.filter(ambiente=2).count()
    secuencia = documentos.secuencialRetencion
    secuencial = str.zfill(str(contador + secuencia), 9)
    tarifas = Tarifas.objects.all()
    tipo = TipoComprobante.objects.get(nombre="COMPROBANTE DE RETENCIÓN").codigo
    proveedor = None
    compra = None
    print("ambiente registrado:", documentos.ambiente.codigo)
    if int(documentos.ambiente.codigo) == 1:
        print("ambiente de pruebas......................................*")
        contador = rett.filter(ambiente=1).count()

        secuencial = str.zfill(str(contador + secuencia), 9)

    print(secuencia, contador)

    if id > 0:
        proveedor = Proveedor.objects.get(id=id)
        compra = Compra.objects.filter(proveedor_id=id)

    if request.POST:
        retencion = Retencion(usuario=usuario, secuencial=secuencial, empresa=usuario.empresa,
                              ambiente=documentos.ambiente.codigo,
                              fecha_emisionFactura=compra.get(id=request.POST['idcompra']).fecha_emision,
                              datosRetencion=documentos,
                              proveedor_id=request.POST['idproveedor'],
                              compra_id=request.POST['idcompra'],
                              valor_total=request.POST['totales'],
                              clave_acceso="", estado="")

        retencion.save()
        fecha = retencion.fecha.strftime("%d%m%Y")
        print("se registro la retencion")
        clave_acceso = claveAcceso(fecha, tipo, usuario.empresa.ruc, documentos.ambiente.codigo,
                                   documentos.codigoEstablecimiento.codigo, documentos.puntoEmision.codigo,
                                   secuencial, "00000111", '1')
        retencion.clave_acceso = clave_acceso
        retencion.save()
        print("se registro hasta aqui")
        if detallesRetenciones(retencion.id, request.POST['jsones']):
            mensaje = "La retencion se emitio correctamente..!!"
            RetencionXML(request,retencion.id)
        else:
            error = "Al parecer ha ocurrido un error..!!"
    permisos=Permiso.objects.filter(grupo=usuario.grupo)
    contexto = {
        'usuario': request.user,
        'compras': Compra.objects.filter(usuario__empresa=usuario.empresa),
        'compra': compra,
        'proveedor': proveedor,
        'proveedores': Proveedor.objects.filter(estado=True, empresa=usuario.empresa),
        'tarifas': tarifas.filter(usado_en_retencion=True).order_by('impuesto', 'porcentaje'),
        'secuencial': secuencial,
        'empresa': usuario.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje': mensaje,
        'error': error,
        'user2': usuario.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/registroRetenciones.html', contexto)


def detallesRetenciones(idRetencion, jsones):
    retencion = Retencion.objects.get(id=idRetencion)
    try:
        for i in json.loads(jsones):
            tarifa = Tarifas.objects.get(id=int(i['tarifa']))
            print(tarifa)
            detalle = DetallesRetencion(retencion_id=idRetencion,
                                        docSustento="%s" % (retencion.compra.secuencial.replace("-", "")),
                                        tarifa=tarifa, impuesto=tarifa.impuesto.codigo,
                                        fecha=retencion.compra.fecha_emision,
                                        porcentaje=tarifa.porcentaje, baseImp=i['baseImp'],
                                        total_retencion=i['Saldos'])
            detalle.save()
        return True
    except Exception as error:
        retencion.delete()
        return False


def RetencionXML(request,n):
    retencion=Retencion.objects.get(id=n)
    xml = ""
    for detalle in DetallesRetencion.objects.filter(retencion=retencion):
        xml += """<impuesto>
                    <codigo>%s</codigo><codigoRetencion>%s</codigoRetencion><baseImponible>%s</baseImponible><porcentajeRetener>%s</porcentajeRetener><valorRetenido>%s</valorRetenido><codDocSustento>01</codDocSustento><numDocSustento>%s</numDocSustento><fechaEmisionDocSustento>%s</fechaEmisionDocSustento></impuesto>""" % (
            detalle.tarifa.impuesto.codigo,detalle.tarifa.codigo,detalle.baseImp, detalle.porcentaje,
            detalle.total_retencion, detalle.docSustento, detalle.retencion.fecha_emisionFactura.strftime("%d/%m/%Y"))

    ret = {
        'retencion': {
            'infoTributaria': {
                'ambiente': retencion.ambiente,
                'tipoEmision': '1',
                'razonSocial': retencion.datosRetencion.empresa.razonSocial,
                'nombreComercial': retencion.datosRetencion.empresa.nombreComercial,
                'ruc': retencion.datosRetencion.empresa.ruc,
                'claveAcceso': retencion.clave_acceso,
                'codDoc': "07",
                'estab': retencion.datosRetencion.codigoEstablecimiento.codigo,
                'ptoEmi': retencion.datosRetencion.puntoEmision.codigo,
                'secuencial': retencion.secuencial,
                'dirMatriz': retencion.datosRetencion.empresa.direccionMatriz,
            },
            'infoCompRetencion': {
                'fechaEmision': retencion.compra.fecha_emision.strftime("%d/%m/%Y"),
                'dirEstablecimiento': retencion.compra.proveedor.direccion,
                'obligadoContabilidad': 'SI',
                'tipoIdentificacionSujetoRetenido': retencion.compra.proveedor.tipo_identificacion.codigo,
                'razonSocialSujetoRetenido': retencion.compra.proveedor.razonSocial,
                'identificacionSujetoRetenido': retencion.compra.proveedor.ruc,
                'periodoFiscal': str.zfill(str(retencion.compra.fecha_emision.month),2)+"/"+str(retencion.compra.fecha_emision.year), #zfill hace que el numerop que se registre siempre tenga 2 como se extrae el mes solo te esta dando un numero con eso se arregla.
            },
            'impuestos': "xs",
        }
    }
    print(ret)
    xml2=documentosRetencionXML(ret,xml,retencion)
    return HttpResponse(xml2, content_type="Application/xml")



def RetencionJSON(request, n):
    retencion = Retencion.objects.get(id=n)
    respuesta = json_sri(str(retencion.clave_acceso), int(retencion.datosRetencion.ambiente.codigo),
                         'media/Facturacion/xml/retencion/response/' + retencion.clave_acceso + '.json')
    try:
        retencion.estado = respuesta['autorizaciones']['autorizacion'][0]['estado']
        retencion.save()
    except Exception as error:
        print(error)
    return HttpResponse(str(respuesta), content_type="Application/json")

#reporte retencion
def RetencionRideSlug(request, id):
    user = myUsuario.objects.get(usuario=request.user)
    retencion = Retencion.objects.get(id=id)
    contexto = {
        'retencion': retencion,
        'detalles': DetallesRetencion.objects.filter(retencion=retencion),
        'reporte': Reportes.objects.filter(empresa=user.empresa).last(),
        'impuestos':Impuestos.objects.all(),
        'user2': user.is_admin,
    }
    template = 'Docuementos_Electronicos/repRetencion.html'
    return render_to_pdf(template, contexto)

def NotaDebitoView(request):
    return render(request, 'Docuementos_Electronicos/notasDebito.html')


def RegistroNotaDebitoView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario': request.user,
        'empresa': user.empresa,
        'reportes': Reportes.objects.last(),
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/registroNotasDebito.html', contexto)


def NotaCreditoView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario': request.user,
        'empresa': user.empresa,
        'reportes': Reportes.objects.last(),
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/notasCredito.html', contexto)


def RegistroNotaCreditoView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario': request.user,
        'empresa': user.empresa,
        'reportes': Reportes.objects.last(),
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/registroNotasCredito.html', contexto)


def ReporteDinamicos(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario': request.user,
        'empresa': user.empresa,
        'reportes': Reportes.objects.last(),
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'tiposComprobantes': TipoComprobante.objects.all(),
        'estadoDoc': EstadoComprobante.objects.all(),
        'usuarios': myUsuario.objects.filter(empresa=user.empresa),
        'ambientes': TipoAmbiente.objects.all(),
        'user2': user.is_admin,

    }
    return render(request, 'Docuementos_Electronicos/reporteDinamico.html', contexto)

def ConsulatDocumento(request):
    user = myUsuario.objects.get(usuario=request.user)
    facturas = None
    guia_remison = None
    retenciones = None

    if request.POST:
        print(request.POST)
        tipo = request.POST['tipo']
        estado =request.POST['estado']
        fecha1 =request.POST['fecha1']
        fecha2 =request.POST['fecha2']
        usuario =request.POST['usuario']
        ambiente =request.POST['ambiente']

        if tipo == 'FACTURA':
            print(usuario)
            facturas=None
            if int(usuario) == 0:
                facturas = Factura.objects.filter(empresa=user.empresa, tipo='FACTURA', estado=estado,ambiente=ambiente,fecha__range=(fecha1, fecha2))
            else:
                facturas = Factura.objects.filter(empresa = user.empresa,tipo='FACTURA',estado=estado,ambiente=ambiente,caja__usuario__id=usuario,fecha__range=(fecha1, fecha2))

            subtotal0=facturas.aggregate(Sum('subtotal_0'))
            subtotal12=facturas.aggregate(Sum("subtotal_iva"))
            subtotal=facturas.aggregate(Sum('subtotal'))
            iva=facturas.aggregate(Sum('iva'))
            total=facturas.aggregate(Sum('total'))
            return render(request, "Docuementos_Electronicos/tablas/factura.html", {'documentos':facturas,'subtotal0':subtotal0,'subtotal12':subtotal12,"subtotal":subtotal,"iva":iva,'total':total})

        elif tipo == 'PROFORMA':
            facturas = None
            if int(usuario) == 0:
                proformas = Factura.objects.filter(empresa=user.empresa, tipo='PROFORMA',fecha__range=(fecha1, fecha2))
            else:
                proformas = Factura.objects.filter(usuario_id=usuario, tipo='PROFORMA', fecha__range=(fecha1, fecha2))

            print("Proformas: ",proformas.count(), proformas)
            return render(request, "Docuementos_Electronicos/tablas/proforma.html", {'documentos': proformas})


        elif tipo == 'GUIA_REMISION':
            guia_remison=None
            if int(usuario) == 0:
                guia_remison = GuiaRemision.objects.filter(empresa=user.empresa,estado=estado,ambiente=ambiente,fecha__range=(fecha1, fecha2))
                print("Guias de remision",guia_remison.count(),guia_remison)
            else:
                guia_remison = GuiaRemision.objects.filter(empresa=user.empresa,estado=estado,fecha__range=(fecha1, fecha2), ambiente=ambiente,usuario_id=usuario)
            return render(request, "Docuementos_Electronicos/tablas/guia.html", {'guias': guia_remison})


        elif tipo == 'RETENCION':
            retenciones=None
            if int(usuario) == 0:
                retenciones = Retencion.objects.filter(tipo='RETENCION', estado=estado, fecha__range=(fecha1, fecha2), ambiente=ambiente,empresa=user.empresa)
            else:
                retenciones = Retencion.objects.filter(tipo='RETENCION', estado=estado, fecha__range=(fecha1, fecha2),usuario_id=usuario, ambiente=ambiente,empresa=user.empresa)
            return render(request, "Docuementos_Electronicos/tablas/retencion.html", {'retenciones': retenciones})

    return HttpResponse("NO HAY NADA")


def CodEstablecimiento(request):
    user = myUsuario.objects.get(usuario=request.user)
    codEstablecimiento = CodigosEstablecimientos.objects.filter(empresa=user.empresa).order_by('id')
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario':request.user,
        'codEstablecimientos': codEstablecimiento,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/CodEstablecimiento.html', contexto)


def RegistroCodEstablecimiento(request):
    user = myUsuario.objects.get(usuario=request.user)
    empresa = DatosEmpresa.objects.filter(usuario=request.user)
    mensaje = ""
    permisos=Permiso.objects.filter(grupo=user.grupo)
    if request.method == 'POST':
        codEstablecimiento = CodigosEstablecimientos(empresa_id=request.POST['empresa'], codigo=request.POST['codigo'],
                                                     estado=True)
        codEstablecimiento.save()
        mensaje = "El codigo de establecimiento se ha creado con exito."
    contexto = {
        'usuario': request.user,
        'empresas': empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje': mensaje,
        'user2': user.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/registroCodEstablecimiento.html', contexto)


def EditarCodEstablecimiento(request, id):
    codEstablecimiento = CodigosEstablecimientos.objects.get(id=id)
    user = myUsuario.objects.get(usuario=request.user)
    empresa = DatosEmpresa.objects.filter(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    mensaje = ""
    if request.POST:
        codEstablecimiento.empresa_id = request.POST['empresa']
        codEstablecimiento.codigo = request.POST['codigo']
        if int(request.POST['estado']) == 1:
            codEstablecimiento.estado = True
        else:
            codEstablecimiento.estado = False
        codEstablecimiento.save()
        mensaje = "Codigo de establecimiento Modificado con exito."
    contexto = {
        'codEstablecimiento': codEstablecimiento,
        'usuario': request.user,
        'empresas': empresa,
        'permisos':permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje': mensaje,
        'user2': user.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/registroCodEstablecimiento.html', contexto)


def DeshabilitarCodEstablecimiento(request, id):
    user = myUsuario.objects.get(usuario=request.user)
    codEstablecimiento = CodigosEstablecimientos.objects.get(id=id)
    codEstablecimiento.estado = False
    codEstablecimiento.save()
    codEstablecimiento = CodigosEstablecimientos.objects.filter(empresa=user.empresa).order_by('id')
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario': request.user,
        'codEstablecimientos': codEstablecimiento,
        'empresa': DatosEmpresa.objects.filter(usuario=request.user),
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje': "Este codigo de establecimiento se ha desactivado..!!",
        'user2': user.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/CodEstablecimiento.html', contexto)


def PuntoEmisionView(request):
    user = myUsuario.objects.get(usuario=request.user)
    puntoEmision = PuntoEmision.objects.filter(empresa=user.empresa)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario':request.user,
        'puntoEmision': puntoEmision,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/PuntoEmision.html', contexto)


def RegistroPuntoEmision(request):
    user = myUsuario.objects.get(usuario=request.user)
    empresa = DatosEmpresa.objects.filter(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    mensaje = ""
    if request.method == 'POST':
        puntoEmision = PuntoEmision(empresa_id=request.POST['empresa'], codigo=request.POST['codigo'], estado=True)
        puntoEmision.save()
        mensaje = "El punto de Emision se ha creado exitosamente."
    contexto = {
        'usuario': request.user,
        'empresas': empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje': mensaje,
        'user2': user.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/registroPuntoEmision.html', contexto)


def EditarPuntoEmision(request, id):
    puntoEmision = PuntoEmision.objects.get(id=id)
    user = myUsuario.objects.get(usuario=request.user)
    permisos=Permiso.objects.filter(grupo=user.grupo)
    mensaje = ""
    empresa = DatosEmpresa.objects.filter(usuario=request.user)
    if request.POST:
        puntoEmision.empresa_id = request.POST['empresa']
        puntoEmision.codigo = request.POST['codigo']

        if int(request.POST['estado']) == 1:
            puntoEmision.estado = True
        else:
            puntoEmision.estado = False
        puntoEmision.save()
        mensaje = "El punto de Emision se ha modificado exitosamente."
    contexto = {
        'puntoEmision': puntoEmision,
        'usuario': request.user,
        'empresas': empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje': mensaje,
        'user2': user.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/registroPuntoEmision.html', contexto)


def DeshabilitarPuntoEmision(request, id):
    puntoEmision = PuntoEmision.objects.get(id=id)
    puntoEmision.estado = False
    puntoEmision.save()
    user = myUsuario.objects.get(usuario=request.user)
    puntoEmision = PuntoEmision.objects.filter(empresa=user.empresa).order_by("id")
    permisos=Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario': request.user,
        'puntoEmision': puntoEmision,
        'empresa': DatosEmpresa.objects.filter(usuario=request.user),
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje': "El Punto de emision seleccionado fue desactivado.",
        'user2': user.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/PuntoEmision.html', contexto)


def Configuracion(request, id=0):
    user = myUsuario.objects.get(usuario=request.user)
    ambientes = TipoAmbiente.objects.all()
    codEstablecimiento = CodigosEstablecimientos.objects.filter(empresa=user.empresa)
    puntoEmision = PuntoEmision.objects.filter(empresa=user.empresa)
    mensaje = ""
    error = ""
    if id > 0:
        for i in DatosDocumentos.objects.filter(empresa=user.empresa):
            if i.id == id:
                if i.estado:
                    i.estado = False
                else:
                    i.estado = True
            else:
                i.estado = False
            i.save()
        return HttpResponseRedirect("/documentos_electronicos/configuracion/")

    if request.method == 'POST':
        print(request.POST)
        ambiente = request.POST['ambiente']
        cod_Establecimiento = request.POST['cod_Establecimiento']
        punto_Emision = request.POST['punto_Emision']
        tipo_Emision = request.POST['tipo_Emision']
        firma = request.FILES['firma']
        clave_Firma = request.POST['clave_Firma']
        banner = request.FILES['banner']
        sec_Factura = request.POST['sec_Factura']
        sec_Proforma = request.POST['sec_Proforma']
        sec_Guia = request.POST['sec_Guia']
        sec_Retencion = request.POST['sec_Retencion']
        try:
            docs = DatosDocumentos.objects.get(ambiente_id=ambiente, codigoEstablecimiento_id=cod_Establecimiento,
                                               puntoEmision_id=punto_Emision, empresa=user.empresa)
            error = "NO es posible crear dos veces la misma configuración"
        except:
            datosDocumento = DatosDocumentos(empresa=user.empresa, ambiente_id=ambiente,
                                             codigoEstablecimiento_id=cod_Establecimiento,
                                             puntoEmision_id=punto_Emision, tipoEmision=tipo_Emision,
                                             firmaElectronica=firma, claveFirma=clave_Firma, banner=banner,
                                             secuencial=sec_Factura, secuenciaProforma=sec_Proforma,
                                             secuencialGuias=sec_Guia
                                             , secuencialRetencion=sec_Retencion, estado=False)
            datosDocumento.save()
            mensaje = "El registro se ha creado exitosamente..!!!"

    contexto = {
        'usuario': request.user,
        'empresas': user.empresa,
        'ambientes': ambientes,
        'codEstablecimiento': codEstablecimiento,
        'puntoEmision': puntoEmision,
        'permisos':Permiso.objects.filter(grupo=user.grupo),
        'funciones': funciones_usuario(Permiso.objects.filter(grupo=user.grupo)),
        'items': Items.objects.all().order_by('prioridad'),
        'datos': DatosDocumentos.objects.filter(empresa=user.empresa).order_by("id"),
        'error': error,
        'mensaje': mensaje,
        'user2': user.is_admin,
    }
    return render(request, 'Docuementos_Electronicos/configuracion.html', contexto)

def anularFactura(request,id):
    factura=Factura.objects.get(id=id)
    factura.estado="ANULADO"
    factura.save()
    user = myUsuario.objects.get(usuario=request.user)
    facturas = Factura.objects.filter(tipo="FACTURA", cliente__empresa=user.empresa).order_by("-id")
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'usuario': request.user,
        'facturas': facturas,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
        'mensaje':"La factura se anulo exitosamente."
    }
    return render(request, 'Docuementos_Electronicos/facturas.html',contexto)

def convertirNota_to_Factura(request, idFactura):
    usuario = myUsuario.objects.get(usuario=request.user)
    contador = Factura.objects.filter(tipo="FACTURA",empresa=usuario.empresa).count()
    print("Numero de facturas: ", contador)
    DATOS = DatosDocumentos.objects.get(empresa=usuario.empresa, estado=True)
    secuencia = DATOS.secuencial
    secuencial = str.zfill(str(contador + secuencia), 9)
    print("secuencial: ", secuencial)
    apertura = None
    tipo = TipoComprobante.objects.get(nombre="FACTURA").codigo
    try:
        apertura = AperturaCaja.objects.get(estado=False, usuario=request.user)
    except:
        return HttpResponseRedirect("/cartera/apertura/")

    factura = Factura.objects.get(id=idFactura)
    detalles = DetallesFactura.objects.filter(factura=factura)
    fac = Clon(factura)
    fac.ambiente = DATOS.ambiente.codigo
    fac.contado=True
    fac.usuario = request.user
    fac.secuencial = secuencial
    fac.caja = apertura
    fac.tipo = "FACTURA"
    fac.fecha = datetime.datetime.now().date()
    fecha = datetime.datetime.now().date().strftime("%d%m%Y")
    clave_acceso = claveAcceso(fecha, tipo, usuario.empresa.ruc, fac.ambiente,str(factura.codigoEstablecimiento), str(factura.puntoEmision), secuencial, "00000000",'1')
    print("Clave de acceso: ", clave_acceso, len(clave_acceso))
    fac.clave_acceso = clave_acceso
    fac.save()

    for det in detalles:
        d = Clon(det)
        d.factura = fac
        d.save()
    facturaXML(request, fac.id)
    return HttpResponseRedirect("/documentos_electronicos/Facturas/")


def Clon(instance):
    cloned = copy.copy(instance)  # don't alter original instance
    cloned.pk = None
    try:
        delattr(cloned, '_prefetched_objects_cache')
    except AttributeError:
        pass
    print("Modelo Clonado: ", cloned)
    return cloned
