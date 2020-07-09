from django import template
from CONTABILIDAD.models import PlanCuentas

register = template.Library()

@register.simple_tag
def CodigosPrincipal():
    codigo = PlanCuentas.objects.filter(principal=None).count()+1
    return codigo

@register.simple_tag
def codigos(codigo,nivel):
    cnt=PlanCuentas.objects.filter(principal__codigo=codigo)
    if not cnt:
        return str.zfill(str(cnt.count() + 1), nivel)
    for i in cnt:
        return str.zfill(str(cnt.count()+1),nivel)