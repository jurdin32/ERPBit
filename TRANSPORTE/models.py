from django.db import models
# Create your models here.
from CLIENTES.models import TipoIndentificacion
from CONFIGURACION.models import DatosEmpresa

listEmpresaTransporte = ['empresa','ruc','razonSocial','direccion', 'telefono','convencional','email', 'estado']
class EmpresaTransporte(models.Model):
    empresa=models.ForeignKey(DatosEmpresa,on_delete=models.CASCADE,null=True, blank=True)
    ruc = models.CharField(max_length=13, null=True, blank=True)
    razonSocial = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=100)
    convencional = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    estado = models.BooleanField(default=True) 

    def __str__(self):
        return self.razonSocial

    class Meta:
        verbose_name_plural="1. Empresas de Transporte"

listConductorTrans = ['empresa','ruc','nombre','apellido','direccion', 'telefono', 'email','licencia','empresaTrans', 'estado']
class ConductorTrans(models.Model):
    empresa = models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    empresaTrans = models.ForeignKey(EmpresaTransporte, on_delete=models.CASCADE)
    tipoIndentificacion=models.ForeignKey(TipoIndentificacion, on_delete=models.CASCADE,null=True, blank=True)
    ruc = models.CharField(max_length=13, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    licencia = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.ruc

    def __str__(self):
        return self.empresa.nombreComercial

    class Meta:
        verbose_name_plural="2. Registro de Conductores"


listVehiculoTrans = ['empresa','codigoAdicional','descripcion','modelo','marca','placa','matricula','conductor','estado']
class VehiculoTrans(models.Model):
    empresa = models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    codigoAdicional=models.CharField(max_length=20,null=True,blank=True)
    conductor = models.ForeignKey(ConductorTrans, on_delete=models.CASCADE,null=True,blank=True)
    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    placa = models.CharField(max_length=50)
    matricula = models.CharField(max_length=100)
    descripcion=models.CharField(max_length=150,null=True,blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.placa


    class Meta:
        verbose_name_plural="3. Registro de Vehiculos"
