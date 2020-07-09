from django import template
from django.db.models import Sum
from django.http import HttpResponseRedirect
from TALENTO_HUMANO.models import Sueldos, Remuneraciones

register = template.Library()


@register.simple_tag
def sueldo(id_empleado):
    try:
        return round(Sueldos.objects.get(empleado_id=id_empleado,estado=True).sueldo,2)
    except:
        return round(0,2)

@register.simple_tag
def sueldoEstado(id_empleado):
    try:
        estado=Sueldos.objects.get(empleado_id=id_empleado,estado=True).estado
        if estado:
            return 'Activo'
    except:
        return "No tiene sueldo Configurado"

@register.simple_tag
def sueldoId(id_empleado):
    try:
            return Sueldos.objects.get(empleado_id=id_empleado,estado=True).id
    except:
        return None

@register.simple_tag
def cargoSueldoId(id):
    return Sueldos.objects.get(id=id).cargo.cargo

@register.filter(name='annio')
def consultarRemuneracionesAnnio(value,arg):
    remuneraciones=Remuneraciones.objects.filter(sueldo__annio_id=arg)
    remun=[]
    rm={}
    for rem in remuneraciones:
        if not rem.periodo.replace('/','-') in remun:
            remun.append(rem.periodo.replace('/','-'))
    return (sorted(remun))
