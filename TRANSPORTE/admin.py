from django.contrib import admin

# Register your models here.
from TRANSPORTE.models import *


class EmpresaTransporteAdmin(admin.ModelAdmin):
    list_display_links = listEmpresaTransporte
    list_display = listEmpresaTransporte
    search_fields = ['ruc']
admin.site.register(EmpresaTransporte, EmpresaTransporteAdmin)


class ConductorTransAdmin(admin.ModelAdmin):
    list_display_links = listConductorTrans
    list_display = listConductorTrans
    search_fields = ['ruc']
admin.site.register(ConductorTrans, ConductorTransAdmin)


class listVehiculoTransAdmin(admin.ModelAdmin):
    list_display_links = listVehiculoTrans
    list_display = listVehiculoTrans
    search_fields = ['ruc']
admin.site.register(VehiculoTrans, listVehiculoTransAdmin)