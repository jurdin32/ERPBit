from DOCUMENTOS_ELECTRONICOS.models import DetallesFactura

raiz = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><factura id='comprobante' version='1.0.0'>'''


def informacionTributaria(ambiente, razonSocial, nombreComercial, ruc, claveAcceso, codEstablecimiento, ptoEmision,
                          secuencial, direccionMatriz):
    datos = '''
    <infoTributaria>
        <ambiente>%s</ambiente>
        <tipoEmision>1</tipoEmision>
        <razonSocial>%s</razonSocial>
        <nombreComercial>%s</nombreComercial>
        <ruc>%s</ruc>
        <claveAcceso>%s</claveAcceso>
        <codDoc>01</codDoc>
        <estab>%s</estab>
        <ptoEmi>%s</ptoEmi>
        <secuencial>%s</secuencial>
        <dirMatriz>%s</dirMatriz>
    </infoTributaria>
''' % (ambiente, razonSocial, nombreComercial, ruc, claveAcceso, codEstablecimiento, ptoEmision, secuencial,
       direccionMatriz)
    return datos


def informacionFactura(fecha,dirEstablecimiento,obligadoContabilidad,tipoIdentificacionComprador,identificacionComprador,direccionComprador,totalSinImpuestos,totalDescuento,importeTotal,factura):
    detalles=DetallesFactura.objects.filter(factura=factura)
    impuesto=""
    for det in detalles:

        impuestos += '''
         <totalImpuesto>
            <codigo>%s</codigo>
            <codigoPorcentaje>%s</codigoPorcentaje>
            <baseImponible>%s</baseImponible>
            <valor>%s</valor>
        </totalImpuesto>
        '''%(det.codigo_iva,det.tarifa_iva,subtotal_iva,det.iva)

        if int(det.tarifa_ice)>0:
            impuestos += '''
                     <totalImpuesto>
                        <codigo>2</codigo>
                        <codigoPorcentaje>2</codigoPorcentaje>
                        <baseImponible>23.1</baseImponible>
                        <valor>2.77</valor>
                    </totalImpuesto>
                    ''' % (det.codigo_iva, det.tarifa_iva, subtotal_iva, det.iva)

    infoFactura = """
    <infoFactura>
        <fechaEmision>03/01/2019</fechaEmision>
        <dirEstablecimiento>Rocafuerte 504 y Buenavista</dirEstablecimiento>
        <obligadoContabilidad>NO</obligadoContabilidad>
        <tipoIdentificacionComprador>07</tipoIdentificacionComprador>
        <razonSocialComprador>CONSUMIDOR FINAL</razonSocialComprador>
        <identificacionComprador>9999999999999</identificacionComprador>
        <direccionComprador>S/N</direccionComprador>
        <totalSinImpuestos>23.10</totalSinImpuestos>
        <totalDescuento>0.00</totalDescuento>
        <totalConImpuestos>
           
        </totalConImpuestos>
        <propina>0.0</propina>
        <importeTotal>25.87</importeTotal>
        <moneda>DOLAR</moneda>
    </infoFactura>
    """
#
#     < detalles >
#     < detalle >
#     < codigoPrincipal > 124 < / codigoPrincipal >
#     < codigoAuxiliar > b'BAL-0078' < / codigoAuxiliar >
#     < descripcion > b'BALANCEADO' / EL
#     GALLO
#     x
#     x
#     45
#     kg < / descripcion >
#     < cantidad > 1.00 < / cantidad >
#     < precioUnitario > 23.1000 < / precioUnitario >
#     < descuento > 0.00 < / descuento >
#     < precioTotalSinImpuesto > 23.10 < / precioTotalSinImpuesto >
#     < impuestos >
#     < impuesto >
#     < codigo > 2 < / codigo >
#     < codigoPorcentaje > 2 < / codigoPorcentaje >
#     < tarifa > 12.00 < / tarifa >
#     < baseImponible > 23.10 < / baseImponible >
#     < valor > 2.77 < / valor >
#
# < / impuesto >
# < / impuestos >
# < / detalle >
# < / detalles >
# < / factura >
