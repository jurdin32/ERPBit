from django.contrib import admin

# Register your models here.
from DOCUMENTOS_ELECTRONICOS.models import *

class TipoComprobanteAdmin(admin.ModelAdmin):
    list_display = listTipoComprobante
    list_display_links = listTipoComprobante
admin.site.register(TipoComprobante, TipoComprobanteAdmin)

class CodigoEstablecimientosAdmin(admin.ModelAdmin):
    list_display_links = listCodigosEstablecimientos
    list_display = listCodigosEstablecimientos
admin.site.register(CodigosEstablecimientos, CodigoEstablecimientosAdmin)


class PuntoEmisionAdmin(admin.ModelAdmin):
    list_display_links = listPuntoEmision
    list_display = listPuntoEmision
admin.site.register(PuntoEmision, PuntoEmisionAdmin)

class EstadoComprobanteAdmin(admin.ModelAdmin):
    list_display_links = listEstadoComprobante
    list_display = listEstadoComprobante
admin.site.register(EstadoComprobante, EstadoComprobanteAdmin)


class TipoAmbienteAdmin(admin.ModelAdmin):
    list_display_links = listTipoAmbiente
    list_display = listTipoAmbiente
admin.site.register(TipoAmbiente, TipoAmbienteAdmin)

class TipoEmisionAdmin(admin.ModelAdmin):
    list_display_links = listTipoEmision
    list_display = listTipoEmision
admin.site.register(TipoEmision, TipoEmisionAdmin)

class TarifasInline(admin.StackedInline):
    model=Tarifas
    extra=0

class ImpuestosAdmin(admin.ModelAdmin):
    list_display_links = listImpuestos
    list_display = listImpuestos
    inlines=[TarifasInline,]
admin.site.register(Impuestos, ImpuestosAdmin)

class TarifaAdmin(admin.ModelAdmin):
    list_display_links = listTarias
    list_display = listTarias
    list_filter = ['impuesto','detalle']
    search_fields = ['codigo','numeroCampo']
admin.site.register(Tarifas, TarifaAdmin)

class DatosDocumentosAdmin(admin.ModelAdmin):
    list_display_links = listDatosDocumentos
    list_display = listDatosDocumentos
admin.site.register(DatosDocumentos, DatosDocumentosAdmin)

class DetallesFacturaInline(admin.StackedInline):
    model=DetallesFactura
    extra=0

class FacturaAdmin(admin.ModelAdmin):
    list_display_links = listFactura
    list_display = listFactura
    inlines=[DetallesFacturaInline]
    search_fields = ['secuencial','fecha','ambiente','cliente__nombre', 'cliente__apellido','cliente__ruc']
    list_filter = ['usuario','tipo','ambiente','puntoEmision','codigoEstablecimiento','cliente','estado','contado']
admin.site.register(Factura,FacturaAdmin)


class DetallesRetencionInline(admin.StackedInline):
    model=DetallesRetencion
    extra=1

class RetencionesAdmin(admin.ModelAdmin):
    list_display_links = listRetencion
    list_display = listRetencion
    inlines = [DetallesRetencionInline]
admin.site.register(Retencion,RetencionesAdmin)


class GuiaRemisionAdmin(admin.ModelAdmin):
    list_display_links = listGuiaRemision
    list_display = listGuiaRemision
admin.site.register(GuiaRemision, GuiaRemisionAdmin)