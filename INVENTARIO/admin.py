from django.contrib import admin

# Register your models here.
from INVENTARIO.models import *


class CategoriaAdmin(admin.ModelAdmin):
    list_display_links = listCategorias
    list_display = listCategorias
admin.site.register(Categoria, CategoriaAdmin)

class BodegaAdmin(admin.ModelAdmin):
    list_display_links = listBodegas
    list_display = listBodegas
admin.site.register(Bodega, BodegaAdmin)

class MarcasAdmin(admin.ModelAdmin):
    list_display_links = listMarcas
    list_display = listMarcas
admin.site.register(Marcas,MarcasAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display_links = listProductos
    list_display = listProductos
    search_fields = ['nombre']
admin.site.register(Producto, ProductoAdmin)

class ProveedorAdmin(admin.ModelAdmin):
    list_display_links = listProveedores
    list_display = listProveedores
    search_fields = ['nombre']
admin.site.register(Proveedor, ProveedorAdmin)

class DetalleProdProvedorAdmin(admin.ModelAdmin):
    list_display_links = listDetalleProProvedores
    list_display = listDetalleProProvedores
    search_fields = ['producto__nombre']
admin.site.register(DetalleProProveedor, DetalleProdProvedorAdmin)

class KardexAdmin(admin.ModelAdmin):
    list_display_links = listKardex
    list_display = listKardex
    search_fields = ['tipo']
admin.site.register(Kardex, KardexAdmin)


class DetalleCompraInline(admin.StackedInline):
    model = DetalleCompra
    extra = 0

class CompraAdmin(admin.ModelAdmin):
    list_display_links = listCompras
    list_display = listCompras
    inlines = [DetalleCompraInline]
admin.site.register(Compra, CompraAdmin)

