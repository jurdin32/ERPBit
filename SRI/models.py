from django.db import models

# Create your models here.
from CONFIGURACION.models import DatosEmpresa

class Formularios(models.Model):
    codigoFormulario=models.CharField(max_length=60)
    detalle = models.TextField()
    formulario = models.TextField()
    codigo_version_formulario=models.CharField(max_length=50,null=True,blank=True)

listF104=['id','empresa','codigo_version_formulario','ruc','codigoMoneda']
class F104(models.Model):
    empresa= models.ForeignKey(DatosEmpresa, null=True, blank=True, on_delete= models.CASCADE)
    codigo_version_formulario=models.CharField(max_length=60)
    ruc = models.CharField(max_length=60)
    codigoMoneda= models.CharField(max_length=20, default='1')

    c101 = models.CharField(max_length=60, null=True, blank=True)
    c102 = models.CharField(max_length=60, null=True, blank=True)
    c31 = models.CharField(max_length=60)
    c104 = models.CharField(max_length=60, null=True, blank=True)

    c201 = models.CharField(max_length=60, null=True, blank=True)
    c202 = models.CharField(max_length=60, null=True, blank=True)



listF104A=['id','empresa','codigo_version_formulario','ruc','codigoMoneda']
class F104A(models.Model):
    empresa=models.ForeignKey(DatosEmpresa,null=True,blank=True,on_delete=models.CASCADE)
    codigo_version_formulario=models.CharField(max_length=60)
    ruc=models.CharField(max_length=60)
    codigoMoneda=models.CharField(max_length=20, default='1')
    c31=models.CharField(max_length=60)

    c101 = models.CharField(max_length=60,null=True,blank=True)
    c102 = models.CharField(max_length=60,null=True,blank=True)
    c104 = models.CharField(max_length=60,null=True,blank=True)
    c111 = models.CharField(max_length=60,null=True,blank=True)
    c113 = models.CharField(max_length=60,null=True,blank=True)
    c115 = models.CharField(max_length=60,null=True,blank=True)
    c117 = models.CharField(max_length=60,null=True,blank=True)
    c119 = models.CharField(max_length=60,null=True,blank=True)
    c198 = models.CharField(max_length=60,null=True,blank=True)

    c201 = models.CharField(max_length=60,null=True,blank=True)
    c202 = models.CharField(max_length=60,null=True,blank=True)

    c401 = models.CharField(max_length=60,null=True,blank=True)
    c402 = models.CharField(max_length=60,null=True,blank=True)
    c403 = models.CharField(max_length=60,null=True,blank=True)
    c404 = models.CharField(max_length=60,null=True,blank=True)
    c405 = models.CharField(max_length=60,null=True,blank=True)
    c406 = models.CharField(max_length=60,null=True,blank=True)
    c409 = models.CharField(max_length=60,null=True,blank=True)
    c411 = models.CharField(max_length=60,null=True,blank=True)
    c412 = models.CharField(max_length=60,null=True,blank=True)
    c413 = models.CharField(max_length=60,null=True,blank=True)
    c414 = models.CharField(max_length=60,null=True,blank=True)
    c415 = models.CharField(max_length=60,null=True,blank=True)
    c416 = models.CharField(max_length=60,null=True,blank=True)
    c419 = models.CharField(max_length=60,null=True,blank=True)
    c421 = models.CharField(max_length=60,null=True,blank=True)
    c422 = models.CharField(max_length=60,null=True,blank=True)
    c423 = models.CharField(max_length=60,null=True,blank=True)
    c424 = models.CharField(max_length=60,null=True,blank=True)
    c429 = models.CharField(max_length=60,null=True,blank=True)
    c431 = models.CharField(max_length=60,null=True,blank=True)
    c434 = models.CharField(max_length=60,null=True,blank=True)
    c441 = models.CharField(max_length=60,null=True,blank=True)
    c442 = models.CharField(max_length=60,null=True,blank=True)
    c443 = models.CharField(max_length=60,null=True,blank=True)
    c444 = models.CharField(max_length=60,null=True,blank=True)

    c453 = models.CharField(max_length=60,null=True,blank=True)
    c454 = models.CharField(max_length=60,null=True,blank=True)
    c499 = models.CharField(max_length=60,null=True,blank=True)

    c480 = models.CharField(max_length=60,null=True,blank=True)
    c481 = models.CharField(max_length=60,null=True,blank=True)
    c482 = models.CharField(max_length=60,null=True,blank=True)
    c483 = models.CharField(max_length=60,null=True,blank=True)
    c484 = models.CharField(max_length=60,null=True,blank=True)
    c485 = models.CharField(max_length=60,null=True,blank=True)

    c500 = models.CharField(max_length=60,null=True,blank=True)
    c501 = models.CharField(max_length=60,null=True,blank=True)
    c502 = models.CharField(max_length=60,null=True,blank=True)
    c507 = models.CharField(max_length=60,null=True,blank=True)
    c508 = models.CharField(max_length=60,null=True,blank=True)
    c509 = models.CharField(max_length=60,null=True,blank=True)
    c510 = models.CharField(max_length=60,null=True,blank=True)
    c511 = models.CharField(max_length=60,null=True,blank=True)
    c512 = models.CharField(max_length=60,null=True,blank=True)
    c517 = models.CharField(max_length=60,null=True,blank=True)
    c518 = models.CharField(max_length=60,null=True,blank=True)
    c519 = models.CharField(max_length=60,null=True,blank=True)
    c520 = models.CharField(max_length=60,null=True,blank=True)
    c521 = models.CharField(max_length=60,null=True,blank=True)
    c522 = models.CharField(max_length=60,null=True,blank=True)
    c526 = models.CharField(max_length=60,null=True,blank=True)
    c527 = models.CharField(max_length=60,null=True,blank=True)
    c529 = models.CharField(max_length=60,null=True,blank=True)
    c531 = models.CharField(max_length=60,null=True,blank=True)
    c532 = models.CharField(max_length=60,null=True,blank=True)
    c535 = models.CharField(max_length=60,null=True,blank=True)
    c541 = models.CharField(max_length=60,null=True,blank=True)
    c542 = models.CharField(max_length=60,null=True,blank=True)
    c543 = models.CharField(max_length=60,null=True,blank=True)
    c544 = models.CharField(max_length=60,null=True,blank=True)
    c545 = models.CharField(max_length=60,null=True,blank=True)
    c554 = models.CharField(max_length=60,null=True,blank=True)
    c555 = models.CharField(max_length=60,null=True,blank=True)
    c563 = models.CharField(max_length=60,null=True,blank=True)
    c564 = models.CharField(max_length=60,null=True,blank=True)

    c601 = models.CharField(max_length=60,null=True,blank=True)
    c602 = models.CharField(max_length=60,null=True,blank=True)
    c603 = models.CharField(max_length=60,null=True,blank=True)
    c604 = models.CharField(max_length=60,null=True,blank=True)
    c605 = models.CharField(max_length=60,null=True,blank=True)
    c606 = models.CharField(max_length=60,null=True,blank=True)
    c607 = models.CharField(max_length=60,null=True,blank=True)
    c608 = models.CharField(max_length=60,null=True,blank=True)
    c609 = models.CharField(max_length=60,null=True,blank=True)
    c610 = models.CharField(max_length=60,null=True,blank=True)
    c611 = models.CharField(max_length=60,null=True,blank=True)
    c612 = models.CharField(max_length=60,null=True,blank=True)
    c613 = models.CharField(max_length=60,null=True,blank=True)
    c614 = models.CharField(max_length=60,null=True,blank=True)
    c615 = models.CharField(max_length=60,null=True,blank=True)
    c617 = models.CharField(max_length=60,null=True,blank=True)
    c618 = models.CharField(max_length=60,null=True,blank=True)
    c619 = models.CharField(max_length=60,null=True,blank=True)
    c620 = models.CharField(max_length=60,null=True,blank=True)
    c621 = models.CharField(max_length=60,null=True,blank=True)
    c699 = models.CharField(max_length=60,null=True,blank=True)

    c890 = models.CharField(max_length=60,null=True,blank=True)
    c897 = models.CharField(max_length=60,null=True,blank=True)
    c898 = models.CharField(max_length=60,null=True,blank=True)
    c899 = models.CharField(max_length=60,null=True,blank=True)

    c902 = models.CharField(max_length=60,null=True,blank=True)
    c903 = models.CharField(max_length=60,null=True,blank=True)
    c904 = models.CharField(max_length=60,null=True,blank=True)
    c905 = models.CharField(max_length=60,null=True,blank=True)
    c906 = models.CharField(max_length=60,null=True,blank=True)
    c907 = models.CharField(max_length=60,null=True,blank=True)
    c908 = models.CharField(max_length=60,null=True,blank=True)
    c909 = models.CharField(max_length=60,null=True,blank=True)
    c910 = models.CharField(max_length=60,null=True,blank=True)
    c911 = models.CharField(max_length=60,null=True,blank=True)
    c912 = models.CharField(max_length=60,null=True,blank=True)
    c913 = models.CharField(max_length=60,null=True,blank=True)
    c915 = models.CharField(max_length=60,null=True,blank=True)
    c916 = models.CharField(max_length=60,null=True,blank=True)
    c917 = models.CharField(max_length=60,null=True,blank=True)
    c918 = models.CharField(max_length=60,null=True,blank=True)
    c919 = models.CharField(max_length=60,null=True,blank=True)
    c920 = models.CharField(max_length=60,null=True,blank=True)
    c922 = models.CharField(max_length=60,null=True,blank=True)
    c925 = models.CharField(max_length=60,null=True,blank=True)
    c999 = models.CharField(max_length=60,null=True,blank=True)

    class Meta:
        verbose_name_plural="FORMULARIO 104A - IVA MENSUAL PERSONAS NO OBLIGADAS A LLEVAR CONTABILIDAD"

























