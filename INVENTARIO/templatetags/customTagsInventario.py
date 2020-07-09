from django import template
from INVENTARIO.models import Kardex, DetalleProProveedor
from django.db.models import Sum

register = template.Library()

@register.simple_tag
def CalcularStock(det):
    detalles=Kardex.objects.filter(detalle_id=det)
    ing=detalles.filter(tipo='I').aggregate(Sum('cantidad'))['cantidad__sum']
    eg=detalles.filter(tipo='E').aggregate(Sum('cantidad'))['cantidad__sum']
    ingresos=0
    egresos=0
    total=0
    if not ing == None:
        ingresos=int(ing)
    if not eg == None:
        egresos=int(eg)
    detall=DetalleProProveedor.objects.get(id=det)
    if detall.producto.tipo == "SERVICIO":
        total=egresos
    else:
        total=ingresos-egresos
    return total

@register.simple_tag
def CalcularIngresos(det):
    detalles = Kardex.objects.filter(detalle_id=det)
    ing=detalles.filter(tipo='I').aggregate(Sum('cantidad'))['cantidad__sum']
    ingresos=0
    if not ing == None:
        ingresos=int(ing)
    return ingresos


@register.simple_tag
def CalcularEngresos(det):
    detalles = Kardex.objects.filter(detalle_id=det)
    ing=detalles.filter(tipo='E').aggregate(Sum('cantidad'))['cantidad__sum']
    ingresos=0
    if not ing == None:
        ingresos=int(ing)
    return ingresos

@register.simple_tag
def UltimaModificacionInventario(det):
    detalles=None
    fecha=''
    try:
        detalles = Kardex.objects.filter(detalle_id=det).last()
        fecha=detalles.fechaCreacion
    except:
        fecha="No se han efectuado Cambios"
    return fecha