from django.contrib import admin

# Register your models here.
from CARTERA.models import *
from DOCUMENTOS_ELECTRONICOS.models import listCuentasCobrar, CuentasPorCobrar, DetallesCuentasCobrar


class AperturaCajaAmin(admin.ModelAdmin):
    list_display_links = listAperturaCaja
    list_display = listAperturaCaja
admin.site.register(AperturaCaja,AperturaCajaAmin)

class GastosDiariosAdmin(admin.ModelAdmin):
    list_display = listGastosDiarios
    list_display_links = listGastosDiarios
admin.site.register(GastosDiarios,GastosDiariosAdmin)

class CierreCajaAdmin(admin.ModelAdmin):
    list_display_links = listCierreCaja
    list_display = listCierreCaja
admin.site.register(CierreCaja,CierreCajaAdmin)

class AnticiposSueldoAdmin(admin.ModelAdmin):
    list_display_links = listAnticipoSueldos
    list_display = listAnticipoSueldos
admin.site.register(AnticiposSueldos,AnticiposSueldoAdmin)

class DetallesCuentasCobrarInline(admin.StackedInline):
    model = DetallesCuentasCobrar
    extra = 1

#consume desde documentos electronicos
class CuentasPorCobrarAdim(admin.ModelAdmin):
    list_display = listCuentasCobrar
    list_display_links = listCuentasCobrar
    inlines = [DetallesCuentasCobrarInline,]
admin.site.register(CuentasPorCobrar,CuentasPorCobrarAdim)