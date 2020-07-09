from django.contrib import admin

# Register your models here.
from CONTABILIDAD.models import *


class PlanCuentasAdmin(admin.ModelAdmin):
    list_display_links = listPlanCuentas
    list_display = listPlanCuentas
admin.site.register(PlanCuentas,PlanCuentasAdmin)

class CuentaBancosInline(admin.StackedInline):
    model = Cuenta_Banco
    extra = 0

class CuentaBancosAdmin(admin.ModelAdmin):
    list_display =listCuentaBancos
    list_display_links =listCuentaBancos
    list_filter = listCuentaBancos
admin.site.register(Cuenta_Banco,CuentaBancosAdmin)

class BancosAdmin(admin.ModelAdmin):
    list_display_links = listBancos
    list_display = listBancos
    inlines = [CuentaBancosInline]

admin.site.register(Bancos,BancosAdmin)
