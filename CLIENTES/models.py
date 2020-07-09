from django.db import models

# Create your models here.
from CONFIGURACION.models import Lugares, DatosEmpresa


class TimeStampModel(models.Model):
    """
    Permite a todos los objetos llevar un historico
    de los registros en la fecha que han sido creados
    y actualizados de manera invisible al usuario.
    """
    creado = models.DateField(auto_now_add=True, null=True,blank=True)
    modificado = models.DateField(auto_now=True, null=True,blank=True )

    class Meta:
        abstract = True

listTipoIdentificacion = ['id', 'nombre', 'codigo']
class TipoIndentificacion(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=3, help_text='Codigo de 2 digitos')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = '1. Tipo de Identificacion'

listClientes = ['empresa', 'tipo_identificacion','ruc','nombre','apellido','razonSocial','direccion', 'telefono', 'email', 'estado', 'creado','modificado']
class Cliente(TimeStampModel):
    empresa=models.ForeignKey(DatosEmpresa,on_delete=models.CASCADE,null=True,blank=True)
    tipo_identificacion=models.ForeignKey(TipoIndentificacion,on_delete=models.CASCADE,null=True,blank=True)
    ruc = models.CharField(max_length=13)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    razonSocial = models.CharField(max_length=150)
    parroquia=models.ForeignKey(Lugares,on_delete=models.CASCADE,null=True,blank=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    estado = models.BooleanField(default=True)


    def __str__(self):
        if not self.razonSocial:
            return "%s %s"%(self.nombre,self.apellido)
        else:
            return "%s" % (self.razonSocial)


    class Meta:
        verbose_name_plural = '2. Clientes'