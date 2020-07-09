# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
from CLIENTES.models import TipoIndentificacion
from CONFIGURACION.models import Lugares, DatosEmpresa
from USERS.models import myUsuario

listCategorias = ['empresa', 'id', 'categoria', 'descripcion', 'estado']


class Categoria(models.Model):
    empresa = models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    categoria = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    estado = models.BooleanField(default=True)

    def save(self):
        self.categoria = self.categoria.upper()
        super(Categoria, self).save()

    def __str__(self):
        return self.categoria

    class Meta:
        verbose_name_plural = "1. Registro de Categorias"


listBodegas = ['empresa', 'id', 'bodega', 'descripcion', 'estado']


class Bodega(models.Model):
    empresa = models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    bodega = models.CharField(max_length=120)
    descripcion = models.CharField(max_length=200)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.bodega

    class Meta:
        verbose_name_plural = "2. Registro de Bodegas"


listProveedores = ['empresa', 'tipo_identificacion', 'ruc', 'razonSocial', 'nombreComercial', 'sector', 'actividad',
                   'telefono', 'convencional', 'web', 'direccion', 'email', 'estado']


class Proveedor(models.Model):
    empresa = models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    tipo_identificacion = models.ForeignKey(TipoIndentificacion, on_delete=models.CASCADE, null=True, blank=True)
    ruc = models.CharField(max_length=13)
    razonSocial = models.CharField(max_length=150)
    nombreComercial = models.CharField(max_length=150)
    sector = models.CharField(max_length=150)
    actividad = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    convencional = models.CharField(max_length=20)
    web = models.CharField(max_length=200)
    parroquia = models.ForeignKey(Lugares, on_delete=models.CASCADE, null=True, blank=True)
    direccion = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombreComercial

    class Meta:
        verbose_name_plural = "4. Registro de Proveedores"


listMarcas = ['empresa', 'id', 'nombre', 'descripcion']


class Marcas(models.Model):
    empresa = models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=60)
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "3. Registro de Marcas"


listProductos = ['empresa', 'id', 'tipo', 'cod_referencia', 'nombre', 'codigoBarra', 'peso', 'medida', 'categoria',
                 'bodega', 'usuario', 'estado']


class Producto(models.Model):
    empresa = models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=(("PRODUCTO", "PRODUCTO"), ("SERVICIO", "SERVICIO")),
                            default="PRODUCTO")
    cod_referencia = models.CharField(max_length=20, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    codigoBarra = models.CharField(max_length=100, blank=True, null=True)
    peso = models.CharField(max_length=50, blank=True, null=True)
    medida = models.CharField(max_length=50, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, blank=True, null=True, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marcas, on_delete=models.CASCADE, null=True, blank=True)
    bodega = models.ForeignKey(Bodega, blank=True, null=True, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    usuario = models.CharField(max_length=40)

    def __str__(self):
        return self.nombre

    def clean(self):
        self.nombre = (self.nombre).upper()
        cat = str(self.categoria.categoria[0:3]).upper().replace("Á", "A").replace("É", "E").replace("Í", "I").replace(
            "Ó", "O").replace("Ú", "U")
        self.cod_referencia = (cat.upper() + "-" + str(str.zfill(str(self.id), 3)))

    class Meta:
        verbose_name_plural = "5. Registro de Productos"


listDetalleProProvedores = ['producto', 'proveedor', 'precioProveedor', 'iva', 'total','stockmax','stockmin', 'porcentajeGanancia', ]

class DetalleProProveedor(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    detalles = models.TextField(null=True, blank=True)
    precioProveedor = models.DecimalField(max_digits=9, decimal_places=2)
    porcentajeIVA = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    codigoIVA = models.CharField(max_length=10, default=0.00)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    codigoICE = models.CharField(max_length=10, default=0.00)
    porcentajeICE = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    ice = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    codigoIRBPNR = models.CharField(max_length=10, default=0.00)
    porcentajeIRBPNR = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    irbpnr = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2)

    stockmax = models.IntegerField(blank=True, null=True)
    stockmin = models.IntegerField(blank=True, null=True)
    porcentajeGanancia = models.DecimalField(max_digits=9, decimal_places=2)
    recargo = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    pvp = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    ivapvp = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    icepvp = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    irbpnrpvp = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    totalpvp = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.producto.nombre

    class Meta:
        verbose_name_plural = "6. Productos del Proveedor"


listKardex = ['detalle', 'tipo','fechaCreacion', 'cantidad', 'descripcion']


class Kardex(models.Model):
    empresa = models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    detalle = models.ForeignKey(DetalleProProveedor, on_delete=models.CASCADE, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=(('I', 'Ingreso'), ('E', 'Egreso')))
    fechaCreacion = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "7. Inventario - Kardex"


listCompras = ['fecha', 'proveedor', 'subtotal', 'iva', 'total']


class Compra(models.Model):
    tipo = models.CharField(max_length=120, null=True, blank=True)
    empresa = models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    contado = models.BooleanField(default=True)
    diasPlazo = models.IntegerField(default=0)
    usuario = models.ForeignKey(myUsuario, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(auto_now=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    subtotal_0 = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    subtotal_iva = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    ice = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    irbpnr = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    fecha_emision = models.DateField(blank=True, null=True)
    clave_acceso = models.CharField(max_length=50, blank=True, null=True)
    secuencial = models.CharField(max_length=17, null=True, blank=True, unique="True")

    def __str__(self):
        return "%s | %s| %s" % (self.proveedor.nombreComercial, self.proveedor.razonSocial, self.secuencial)

    class Meta:
        verbose_name_plural = "8. Registro de Compras"


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(DetalleProProveedor, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    subtotal_0 = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    subtotal_iva = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    ice = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    irbpnr = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    codigo_iva = models.CharField(max_length=30, default=0)
    tarifa_iva = models.CharField(max_length=30, default=0)
    codigo_ice = models.CharField(max_length=30, default=0)
    tarifa_ice = models.CharField(max_length=30, default=0)
    codigo_irbpnr = models.CharField(max_length=30, default=0)
    tarifa_irbpnr = models.CharField(max_length=30, default=0)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        kardex = Kardex(
            detalle=self.producto,
            descripcion="Factura de Compra No: " + self.compra.secuencial + " con autorización: " + self.compra.clave_acceso + ", fecha: " + str(
                self.compra.fecha),
            tipo="I",
            fechaCreacion=self.compra.fecha,
            cantidad=self.cantidad
        )
        kardex.save()
        super(DetalleCompra, self).save()
