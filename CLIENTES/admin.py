from django.contrib import admin

# Register your models here.
from CLIENTES.models import *

class TipoIdentificacionAdmin(admin.ModelAdmin):
    list_display = listTipoIdentificacion
    list_display_links = listTipoIdentificacion
admin.site.register(TipoIndentificacion, TipoIdentificacionAdmin)

class ClienteAdmin(admin.ModelAdmin):
    list_display_links = listClientes
    list_display = listClientes
    search_fields = ['ruc']
admin.site.register(Cliente, ClienteAdmin)