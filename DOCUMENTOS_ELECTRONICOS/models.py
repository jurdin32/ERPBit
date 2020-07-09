# encoding: utf-8
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from CARTERA.models import AperturaCaja
from CLIENTES.models import Cliente
from CONFIGURACION.models import DatosEmpresa
from INVENTARIO.models import DetalleProProveedor, Kardex, Compra, Proveedor
from TRANSPORTE.models import VehiculoTrans
from USERS.models import myUsuario
from django.utils.safestring import mark_safe

listTipoComprobante = ['id','codigo','nombre']
class TipoComprobante(models.Model):
    codigo = models.CharField(max_length=4)
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.nombre=self.nombre.upper()
        super(TipoComprobante, self).save()

    class Meta:
        verbose_name_plural = '8. Tipo de Comprobantes'


listCodigosEstablecimientos = ['empresa','id', 'empresa', 'codigo']
class CodigosEstablecimientos(models.Model):
    empresa = models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    codigo = models.CharField(max_length=3, help_text='Codigo de 3 digitos')
    estado=models.BooleanField(default=True)

    def __str__(self):
        return "%s | %s"%(self.empresa,self.codigo)

    def __str__(self):
        return self.empresa.nombreComercial


    class Meta:
        verbose_name_plural = '2. Codigo de Establecimientos'

listPuntoEmision = ['empresa', 'id', 'codigo']
class PuntoEmision(models.Model):
    empresa = models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    codigo = models.CharField(max_length=3, help_text='Codigo de 3 digitos')
    estado = models.BooleanField(default=True)

    def __str__(self):
        return '%s | %s' % (self.empresa,self.codigo)

    def __str__(self):
        return self.empresa.nombreComercial

    class Meta:
        verbose_name_plural = '3. Punto de Emision'

listEstadoComprobante = ['id', 'nombre', 'siglas']
class EstadoComprobante(models.Model):
    nombre = models.CharField(max_length=60)
    siglas = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.nombre=self.nombre.upper()
        super(EstadoComprobante, self).save()
    
    class Meta:
        verbose_name_plural = '9. Estado de Comprobantes'

listTipoAmbiente = ['id','nombre','codigo']
class TipoAmbiente(models.Model):
    nombre = models.CharField(max_length=60)
    codigo = models.CharField(max_length=3)
    estado= models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.nombre=self.nombre.upper()
        super(TipoAmbiente, self).save()

    class Meta:
        verbose_name_plural = '1. Ambientes'


listTipoEmision = ['id','nombre','codigo']
class TipoEmision(models.Model):
    nombre = models.CharField(max_length=60)
    codigo = models.CharField(max_length=3)
    
    def __str__(self):
        return self.nombre

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.nombre=self.nombre.upper()
        super(TipoEmision, self).save()
        
    class Meta:
        verbose_name_plural = '4. Tipo Emision'

listImpuestos = ['nombre','codigo']
class Impuestos(models.Model):
    nombre = models.CharField(max_length=60)
    codigo = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.nombre

    def save(self):
        self.nombre = self.nombre.upper()
        super(Impuestos, self).save()

    class Meta:
        verbose_name_plural = '6. Impuestos'

listTarias = ['id','porcentaje','codigo','numeroCampo','detalle','impuesto','tarifaAD','activo','usado_en_retencion','valorIva']
class Tarifas(models.Model):
    impuesto = models.ForeignKey(Impuestos, on_delete = models.CASCADE, null = True, blank = True)
    porcentaje = models.DecimalField(max_digits=9, decimal_places=2, null = True, blank = True)
    codigo = models.IntegerField(default=0)
    numeroCampo=models.CharField(max_length=6,unique=True,null=True,blank=True)
    detalle = models.TextField()
    tarifaAD = models.CharField(max_length=10,  null = True, blank = True)
    activo=models.BooleanField(default=True)
    usado_en_retencion=models.BooleanField(default=False)
    valorIva=models.BooleanField(default=False)

    def __str__(self):
        return '%s:%s '%(self.impuesto.nombre, self.codigo)
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.detalle=self.detalle.upper()
        super(Tarifas, self).save()
        

    class Meta:
        verbose_name_plural = '6.1. Tarifas'


listDatosDocumentos = ['empresa','ambiente','baner','tipoEmision', 'firma', 'clave','secuencial','secuencialGuias','secuencialRetencion','estado']
class DatosDocumentos(models.Model):
    empresa=models.ForeignKey(DatosEmpresa,on_delete=models.CASCADE,null=True,blank=True)
    ambiente = models.ForeignKey(TipoAmbiente,on_delete= models.CASCADE,null=True, blank=True)
    codigoEstablecimiento=models.ForeignKey(CodigosEstablecimientos,on_delete= models.CASCADE,null=True, blank=True)
    puntoEmision = models.ForeignKey(PuntoEmision, on_delete=models.CASCADE, null=True, blank=True)
    tipoEmision = models.CharField(max_length=1, default='1')
    firmaElectronica = models.FileField(upload_to='firmas', null=True, blank=True)
    claveFirma = models.CharField(max_length=30)
    banner = models.FileField(upload_to='Banner', null=True, blank=True)
    secuencial=models.IntegerField(default=1)
    secuenciaProforma=models.IntegerField(default=1)
    caducidadProforma=models.TextField(default="Estos precios pueden variar; válido por 7 dias a partir de la emisión..!!")
    secuencialGuias=models.IntegerField(default=1)
    secuencialRetencion = models.IntegerField(default=1)
    secuencialNotaVenta=models.IntegerField(default=1)
    estado=models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = '5. Datos de los Documentos'

    def baner(self):
        return mark_safe('<img width="100px" src="/media/%s">' % self.banner)

    def firma(self):
        if self.firmaElectronica:
            return "SI"
        else:
            return "NO"
    def clave(self):
        if self.claveFirma:
            return "*"*len(self.claveFirma)
        else:
            return "No se ha especificado"

    def __str__(self):
        return self.empresa.nombreComercial

listFactura=['usuario','secuencial','tipo','fecha','cliente','total','clave_acceso','estado','contado']
class Factura(models.Model):
    empresa=models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE,null=True,blank=True)
    caja=models.ForeignKey(AperturaCaja,on_delete=models.CASCADE, null=True,blank=True)
    contado=models.BooleanField(default=True)
    diasPlazo=models.IntegerField(default=0)
    usuario=models.ForeignKey(User,on_delete=models.CASCADE, null=True,blank=True)
    ambiente=models.IntegerField(default=1)
    secuencial=models.CharField(max_length=15,null=True,blank=True)
    codigoEstablecimiento=models.CharField(max_length=3,default="001",null=True,blank=True)
    puntoEmision = models.CharField(max_length=3, default="001",null=True,blank=True)
    tipo=models.CharField(max_length=20,choices=(('FACTURA','FACTURA'),('PROFORMA','PROFORMA'),('NOTA DE VENTA','NOTA DE VENTA')))
    datosFactura=models.ForeignKey(DatosDocumentos,on_delete=models.CASCADE,null=True,blank=True)
    fecha=models.DateField(auto_now_add=True)
    #fecha = models.DateField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,null=True,blank=True)
    subtotal_0=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    subtotal_iva=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    subtotal=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    descuento=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    iva=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    ice=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    irbpnr=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    clave_acceso=models.CharField(max_length=50,null=True,blank=True)
    guiaRemision=models.CharField(max_length=50,null=True,blank=True)
    estado=models.CharField(max_length=30,null=True,blank=True)
    estado_por_pagar=models.BooleanField(default=False)

    def __str__(self):
        return self.secuencial

    class Meta:
        verbose_name_plural = '10. Facturacion'

class DetallesFactura(models.Model):
    factura = models.ForeignKey(Factura,on_delete=models.CASCADE,null=True,blank=True)
    producto = models.ForeignKey(DetalleProProveedor,on_delete=models.CASCADE,null=True,blank=True)
    cantidad = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    subtotal_0 = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    subtotal_iva = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    ice = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    irbpnr = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    codigo_iva=models.CharField(max_length=30,default=0)
    tarifa_iva=models.CharField(max_length=30,default=0)
    codigo_ice=models.CharField(max_length=30,default=0)
    tarifa_ice = models.CharField(max_length=30, default=0)
    codigo_irbpnr=models.CharField(max_length=30,default=0)
    tarifa_irbpnr = models.CharField(max_length=30, default=0)

    def save(self):
        print("")
        tarifas = Tarifas.objects.all()
        self.codigo_iva=tarifas.get(id=self.producto.codigoIVA).impuesto.codigo
        self.tarifa_iva=tarifas.get(id=self.producto.codigoIVA).codigo
        if int(self.producto.codigoICE)>0:
            self.codigo_ice = tarifas.get(id=self.producto.codigoICE).impuesto.codigo
            self.tarifa_ice = tarifas.get(id=self.producto.codigoICE).codigo
        if int(self.producto.codigoIRBPNR)> 0:
            self.codigo_irbpnr = tarifas.get(id=self.producto.codigoIRBPNR).impuesto.codigo
            self.tarifa_irbpnr = tarifas.get(id=self.producto.codigoIRBPNR).codigo
        self.total=float(self.subtotal)+float(self.iva)+float(self.ice)+float(self.irbpnr)-float(self.descuento)
        if self.factura.tipo == "FACTURA":
            kardex = Kardex(
                detalle=self.producto,
                descripcion="Factura de Venta No: " + self.factura.secuencial + " con autorización: " + self.factura.clave_acceso + ", fecha: " + str(
                    self.factura.fecha),
                tipo="E",
                fechaCreacion=self.factura.fecha,
                cantidad=self.cantidad
            )
            kardex.save()
            print("Es una Factura de venta, el kardex se vera afectado..!!")
        elif self.factura.tipo == "NOTA DE VENTA":
            kardex = Kardex(
                detalle=self.producto,
                descripcion="Nota de Entrega No: " + self.factura.secuencial +"con fecha: " + str(
                    self.factura.fecha)+", registrado por el usuario: "+self.factura.usuario.username,
                tipo="E",
                fechaCreacion=self.factura.fecha,
                cantidad=self.cantidad
            )
            kardex.save()
            print("Es una nota de venta, el kardex se vera afectado..!!")
        else:
            print("Es una proforma, no se vera afectado el kardex..!!")
        super(DetallesFactura,self).save()


listGuiaRemision=['secuencial','facturaId','fecha','ruta']
class GuiaRemision(models.Model):
    tipo = models.CharField(max_length=20, default='GUIA_REMISION')
    empresa=models.ForeignKey(DatosEmpresa,on_delete=models.CASCADE,null=True,blank=True)
    ambiente=models.CharField(default=1, max_length=10)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    secuencial = models.CharField(max_length=9, null=True, blank=True, unique="True")
    datosGuia = models.ForeignKey(DatosDocumentos, on_delete=models.CASCADE, null=True, blank=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, null=True, blank=True)
    vehiculo = models.ForeignKey(VehiculoTrans, on_delete=models.CASCADE,null=True,blank=True)
    fecha = models.DateField(auto_now_add=True)
    puntoPartida = models.CharField(max_length=120, null=True, blank=True)
    fachaIniTrans = models.DateField()
    fachaFinTrans = models.DateField()
    observaciones = models.CharField(max_length=200, null=True, blank=True)
    motivoTraslado = models.CharField(max_length=200, null=True, blank=True)
    puntoLLegada = models.CharField(max_length=200, null=True, blank=True)
    docAduanero = models.CharField(max_length=100, null=True, blank=True)
    codEstablecimiento = models.CharField(max_length=10,null=True, blank=True )
    ruta = models.CharField(max_length=200, null=True, blank=True)
    clave_acceso = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=10, null=True, blank=True)


    def facturaId(self):
        return self.factura.secuencial

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        factura=Factura.objects.get(id=self.factura.id)
        factura.guiaRemision=self.factura.codigoEstablecimiento+"-"+factura.puntoEmision+"-"+self.secuencial
        factura.save()
        print("la factura se modifico",factura.guiaRemision)
        print("clave de acceso de la guia: ",self.clave_acceso)
        self.ruta = self.puntoPartida + " - " + self.puntoLLegada
        super(GuiaRemision, self).save()

    class Meta:
        verbose_name_plural = '11. Guias de Remision'


listRetencion=['usuario','secuencial','fecha','clave_acceso','estado']
class Retencion(models.Model):
    tipo = models.CharField(max_length=20, default='RETENCION')
    empresa=models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, default=2)
    ambiente=models.CharField(max_length=10,null=True,blank=True, default=1)
    usuario = models.ForeignKey(myUsuario, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(auto_now=True)
    fecha_emisionFactura = models.DateField(blank=True, null=True)
    secuencial = models.CharField(max_length=9, null=True, blank=True)
    datosRetencion = models.ForeignKey(DatosDocumentos, on_delete=models.CASCADE, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, null=True, blank=True )
    valor_total = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    clave_acceso = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name_plural = '12. Retenciones'


class DetallesRetencion(models.Model):
    retencion = models.ForeignKey(Retencion, on_delete=models.CASCADE)
    docSustento=models.CharField(max_length=20, default='001001000000001', null=True,blank=True)
    fecha=models.DateField(null=True,blank=True)
    tarifa = models.ForeignKey(Tarifas, on_delete=models.CASCADE,null=True,blank=True)
    impuesto = models.CharField(max_length=100,null=True,blank=True)
    porcentaje = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    baseImp = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total_retencion = models.DecimalField(max_digits=9, decimal_places=2, default=0)



# cartera documentos por cobrar:
listCuentasCobrar=['usuario','factura','fecha','valor','plazo','cuotas','estado']
class CuentasPorCobrar(models.Model):

    usuario = models.ForeignKey(myUsuario, on_delete=models.CASCADE)
    factura=models.OneToOneField(Factura,on_delete=models.CASCADE,unique=True)
    fecha = models.DateField(auto_now_add=True)
    valor = models.DecimalField(max_digits=9,decimal_places=2,default=0.00)
    plazo = models.IntegerField(default=0, help_text="dias de plazo")
    cuotas=models.IntegerField(default=1)
    estado=models.BooleanField(default=False)

    def __str__(self):
        return self.factura.cliente.ruc



class DetallesCuentasCobrar(models.Model):
    cuenta=models.ForeignKey(CuentasPorCobrar,on_delete=models.CASCADE)
    caja = models.ForeignKey(AperturaCaja, on_delete=models.CASCADE,null=True,blank=True)
    n_pago=models.IntegerField(default=1)
    detalles=models.CharField(max_length=100,null=True,blank=True)
    fecha_esperada = models.DateField(null=True,blank=True)
    fecha_pago=models.DateField(null=True,blank=True)
    abono=models.DecimalField(max_digits=9,decimal_places=2,default=0.00)
    saldo=models.DecimalField(max_digits=9,decimal_places=2,default=0.00)
    estado=models.BooleanField(default=False)

    def __str__(self):
        value=str(self.abono)
        print(value)
        return str(value)



