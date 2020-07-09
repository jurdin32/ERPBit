from django.contrib import admin

# Register your models here.
from SRI.models import Formularios, listF104A, F104A


class FormulariosAdmin(admin.ModelAdmin):
    list_display = ["codigo_version_formulario","codigoFormulario","detalle"]
    list_display_links = ["codigo_version_formulario","codigoFormulario","detalle"]
admin.site.register(Formularios,FormulariosAdmin)

class F104Aadmin(admin.ModelAdmin):
    list_display_links = listF104A
    list_display = listF104A
admin.site.register(F104A,F104Aadmin)
