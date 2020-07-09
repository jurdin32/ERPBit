from django.http import HttpResponse

from DOCUMENTOS_ELECTRONICOS.models import Factura, GuiaRemision, Retencion
from USERS.models import myUsuario


def ConsulatDocumento(request, tipo, estado, fecha1, fecha2, usuario, ambiente):
    user = myUsuario.objects.get(usuario=request.user)
    factura = guia_remison=retenciones=None
    if tipo == 'FACTURA':
        factura = Factura.objects.filter(tipo='FACTURA', estado=estado, fecha__range=(fecha1,fecha2), usuario__username=usuario, ambiente=ambiente)
    elif tipo == 'PROFORMA':
        factura = Factura.objects.filter(tipo='PROFORMA', estado=estado, fecha__range=(fecha1, fecha2),
                                         usuario__username=usuario, ambiente=ambiente)
    elif tipo == 'GUIA_REMISION':
        guia_remison = GuiaRemision.objects.filter(tipo='GUIA_REMISION', estado=estado, fecha__range=(fecha1, fecha2),
                                         usuario__username=usuario, ambiente=ambiente)
    elif tipo == 'RETENCION':
        retenciones = Retencion.objects.filter(tipo='RETENCION', estado=estado, fecha__range=(fecha1, fecha2),
                                         usuario__username=usuario, ambiente=ambiente)

    return HttpResponse(factura)