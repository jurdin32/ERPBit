from django.contrib import admin


from CONFIGURACION.models import *


class EmpresaAdmin(admin.ModelAdmin):
    list_display_links = listDatosEmpresa
    list_display = listDatosEmpresa
    search_fields = ['ruc']
admin.site.register(DatosEmpresa, EmpresaAdmin)

class CargosInline(admin.StackedInline):
    model=Cargos
    extra=1

class DepartamentoAdmin(admin.ModelAdmin):
    list_display_links = listDepartamentos
    list_display = listDepartamentos
    inlines=[CargosInline]
admin.site.register(Departamento, DepartamentoAdmin)

class LugaresAdmin(admin.ModelAdmin):
    list_display = listLugares
    list_display_links = listLugares
    ordering = ['-lugar']
    list_filter=['lugar','provincia','ciudad','parroquia']
admin.site.register(Lugares, LugaresAdmin)

class ItemsLine(admin.StackedInline):
    model = Items
    extra=1


class FuncionesAdmin(admin.ModelAdmin):
    list_display = listFunciones
    list_display_links = listFunciones
    inlines = [ItemsLine]
admin.site.register(Funciones,FuncionesAdmin)



class ReportesAdmin(admin.ModelAdmin):
    list_display_links = listReportes
    list_display = listReportes
admin.site.register(Reportes,ReportesAdmin)


class PermisosAdmin(admin.ModelAdmin):
    list_display = listPermiso
    list_display_links = listPermiso
admin.site.register(Permiso,PermisosAdmin)

class PermisosInline(admin.StackedInline):
    model = Permiso
    extra = 1

class GruposAdmin(admin.ModelAdmin):
    list_display_links = ListGrupos
    list_display = ListGrupos
    inlines = [PermisosInline]
admin.site.register(Grupo,GruposAdmin)


class HelperDocsInline(admin.StackedInline):
    model = HelpersDetalles
    extra = 1

class HelperAdmin(admin.ModelAdmin):
    list_display_links =listHelper
    list_display=listHelper
    inlines = [HelperDocsInline]
    ordering = ['id',]
    search_fields = ['descripcion','titulo']
admin.site.register(Helpers, HelperAdmin)


class ItemsAdmin(admin.ModelAdmin):
    list_display_links = listItems
    list_display=listItems
    list_filter = listItems
    # readonly_fields = ['prioridad',]
admin.site.register(Items,ItemsAdmin)
