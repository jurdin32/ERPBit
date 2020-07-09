#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from CONFIGURACION.models import DatosEmpresa
from TALENTO_HUMANO.models import Empleado
from USERS.models import myUsuario

listAperturaCaja=['usuario','fecha','hora','totalBilletes','totalMonedas','totalDocumentos','saldoInicial','estado']
class AperturaCaja(models.Model):
    empresa=models.ForeignKey(DatosEmpresa,on_delete=models.CASCADE,null=True,blank=True)
    usuario=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    fecha=models.DateField(auto_now_add=True)
    hora=models.TimeField(auto_now_add=True)
    mon1=models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    mon5=models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    mon10=models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    mon25=models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    mon50=models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    mon100=models.DecimalField(default=0.00, decimal_places=2, max_digits=9)

    bil1=models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    bil5 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    bil10 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    bil20 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    bil50 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    bil100 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)

    totalBilletes=models.DecimalField(max_digits=9,decimal_places=2,default=0.00)
    totalMonedas=models.DecimalField(max_digits=9, decimal_places=2,default=0.00)
    totalDocumentos=models.DecimalField(max_digits=9, decimal_places=2,default=0.00)
    saldoInicial = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    estado=models.BooleanField(default=True)


    def __str__(self):
        return "%s"%(self.usuario.username)

    class Meta:
        verbose_name_plural="1. Apertura de Caja"

listGastosDiarios=['caja','fecha','descripcion','tipoDocumento','numeroDocumento','valor']
class GastosDiarios(models.Model):
    tipo=models.CharField(max_length=30,default="GASTO")
    caja=models.ForeignKey(AperturaCaja,on_delete=models.CASCADE,null=True,blank=True)
    fecha = models.DateField(auto_now_add=True)
    descripcion=models.TextField(null=True,blank=True)
    valor=models.DecimalField(max_digits=9,decimal_places=2,default=0.00)
    tipoDocumento=models.CharField(max_length=60,default="FACTURA DE LA CASA COMERCIAL")
    numeroDocumento=models.CharField(max_length=20,default="000-000-000000000")

    class Meta:
        verbose_name_plural="2. Registro de Gastos Diarios"

listCierreCaja=['caja','fecha','hora','saldoInicial','totalGasto','totalVentas','total','saldoFinal','faltante','observacion',]
class CierreCaja(models.Model):
    empresa = models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    caja = models.ForeignKey(AperturaCaja, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    saldoInicial = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    totalGasto=models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    totalVentas = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    cuentasCobrar=models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    totalDiario=models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    mon1 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    mon5 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    mon10 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    mon25 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    mon50 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    mon100 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)

    bil1 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    bil5 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    bil10 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    bil20 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    bil50 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    bil100 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)

    totalBilletes = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    totalMonedas = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    totalDocumentos = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    saldoFinal=models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    faltante=models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    observacion=models.TextField(null=True,blank=True)
    estado=models.BooleanField(default=True)

    def total(self):
        return (self.totalDiario)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        saldos=(float(self.saldoInicial)+float(self.totalVentas)+float(self.cuentasCobrar))-float(self.totalGasto)
        self.totalDiario=saldos

        final=float(self.totalBilletes)+float(self.totalMonedas)+float(self.totalDocumentos)
        if saldos >final:
            print(saldos,final)
            self.faltante=saldos-final
            self.observacion=("El total conformado por: ((Saldo de Apertura + Total de las Ventas) - Total del Gasto Diario), difiere, por lo que se considera un valor faltante de: "+str(self.faltante)+" Segun ha sido registrado por el usuario: "+self.caja.usuario.username)
        elif (saldos)*-1 >0 and final < (saldos)*-1:
            print(saldos, final,"se esta registrando con exceso..!!")
            self.faltante = (saldos)*-1
            self.observacion = ("El total conformado por: ((Saldo de Apertura + Total de las Ventas) - Total del Gasto Diario), difiere, por lo que se considera un valor en exceso de: " + str(self.faltante) + " Segun ha sido registrado por el usuario: " + self.caja.usuario.username)
        elif (saldos)*-1 >0 and final>(saldos)*-1:
            self.faltante = ((saldos)*-1) - final
            if self.faltante > 0:
                self.faltante = (((saldos) * -1) - final)*-1
                self.observacion = ("El total conformado por: ((Saldo de Apertura + Total de las Ventas) - Total del Gasto Diario), difiere, por lo que se considera un valor en exceso de: " + str(self.faltante) + " Segun ha sido registrado por el usuario: " + self.caja.usuario.username)
            else:
                self.faltante = (((saldos) * -1) - final) * -1
                self.observacion = "Sin Novedades"
        else:
            self.faltante = saldos - final
            self.observacion="Sin Novedades"

        super(CierreCaja, self).save()

    class Meta:
        verbose_name_plural="3. Cierre de Caja"

listAnticipoSueldos=['empleado','fecha','valor','descripcion']
class AnticiposSueldos(models.Model):
    empleado=models.ForeignKey(Empleado,on_delete=True)
    fecha=models.DateField(auto_now_add=True)
    valor=models.DecimalField(max_digits=9, decimal_places=2,default=0.00)
    descripcion=models.TextField()

    class Meta:
        verbose_name_plural="4. Anticipo de Sueldos"



