from django.contrib import admin

# Register your models here.
from TALENTO_HUMANO.models import *

class EmpleadoAdmin(admin.ModelAdmin):
    list_display_links = listEmpleados
    list_display = listEmpleados
    search_fields = ['nombre']
admin.site.register(Empleado, EmpleadoAdmin)

class AnioAdmin(admin.ModelAdmin):
    list_display_links = listAnios
    list_display = listAnios
admin.site.register(Anio, AnioAdmin)

class FormaPagoAdmin(admin.ModelAdmin):
    list_display_links = listFormaPagos
    list_display = listFormaPagos
admin.site.register(FormaPago, FormaPagoAdmin)

class RolPagosAdmin(admin.ModelAdmin):
    list_display_links = listRolPagos
    list_display = listRolPagos
admin.site.register(RolPagos, RolPagosAdmin)

class SueldosAdmin(admin.ModelAdmin):
    list_display = listSueldos
    list_display_links = listSueldos
admin.site.register(Sueldos,SueldosAdmin)

class RemuneracionesAdmin(admin.ModelAdmin):
    list_display = listRemuneracion
    list_display_links = listRemuneracion
admin.site.register(Remuneraciones,RemuneracionesAdmin)

class IngresoEgresoAdmin(admin.ModelAdmin):
    list_display_links = listIngresosEgresos
    list_display = listIngresosEgresos
admin.site.register(IngresosEgresos,IngresoEgresoAdmin)
