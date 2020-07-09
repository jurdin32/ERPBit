from django.db import models

# Create your models here.

from CARTERA.models import AperturaCaja
from CONFIGURACION.models import DatosEmpresa

listPlanCuentas=['id','nivel','principal','codigo','nombre']

class PlanCuentas(models.Model):
    empresa=models.ForeignKey(DatosEmpresa,on_delete=models.CASCADE,null=True,blank=True)
    principal=models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True)
    nivel=models.IntegerField(default=1)
    codigo=models.CharField(max_length=30,blank=True,null=True)
    nombre=models.TextField(null=True,blank=True)

    def __str__(self):
        return "%s | %s"%(self.codigo,self.nombre)


listBancos=['id','nombre']
class Bancos(models.Model):
    nombre=models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.nombre=str.upper(self.nombre)
        super(Bancos, self).save()


listCuentaBancos=['id','empresa','banco','no_cuenta','tipo_cuenta','enlace','estado']
class Cuenta_Banco(models.Model):
    empresa=models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE,null=True,blank=True)
    banco=models.ForeignKey(Bancos,on_delete=models.CASCADE)
    no_cuenta=models.CharField(max_length=15)
    tipo_cuenta=models.CharField(max_length=50, choices=(("CA","AHORRO"), ("CC",'CORRIENTE')))
    estado=models.BooleanField(default=True)
    enlace=models.ForeignKey(PlanCuentas,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return "%s | %s | %s"%(self.banco.nombre,self.tipo_cuenta,self.no_cuenta)


