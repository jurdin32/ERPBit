from django import template

from CARTERA.models import GastosDiarios
from DOCUMENTOS_ELECTRONICOS.models import Factura
from django.db.models import Sum

register = template.Library()

@register.simple_tag
def CalcularVentas(caja):
    ventas=Factura.objects.filter(caja=caja, estado="AUTORIZADO",ambiente=2)
    if ventas.aggregate(Sum('total'))['total__sum'] == None:
        return "0.00"
    return ventas.aggregate(Sum('total'))['total__sum']

@register.simple_tag
def CalcularGastos(caja):
    ventas=GastosDiarios.objects.filter(caja=caja)
    if ventas.aggregate(Sum('valor'))['valor__sum'] == None:
        return "0.00"
    return ventas.aggregate(Sum('valor'))['valor__sum']


@register.simple_tag
def CalcularTodo(caja):
    ventas = Factura.objects.filter(caja=caja, estado="AUTORIZADO",ambiente=2).aggregate(Sum('total'))['total__sum']
    gastos = GastosDiarios.objects.filter(caja=caja).aggregate(Sum('valor'))['valor__sum']

    print("Saldo Inicial",caja.saldoInicial)
    print("Ventas",ventas)
    print("Gastos",gastos)
    if  ventas==None:
        ventas=0.00

    if gastos==None:
        gastos=0.00

    print("ventas", ventas)
    print('gastos',gastos)

    return round(((float(ventas)+float(caja.saldoInicial))-float(gastos)),2)
