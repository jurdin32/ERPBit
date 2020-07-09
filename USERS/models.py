from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from CONFIGURACION.models import DatosEmpresa, Grupo

listMyEmpresa=['id','empresa','usuario','nombre_y_apellido','email','is_superuser','is_active','is_staff']
class myUsuario(models.Model):
    empresa=models.ForeignKey(DatosEmpresa,on_delete=models.CASCADE,null=True,blank=True,help_text="Seleccione la empresa a la que pertenece el usuario")
    usuario=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,help_text="Seleccione el Usuaio que desea agregar")
    grupo=models.ForeignKey(Grupo,on_delete=models.CASCADE,null=True,blank=True)
    is_admin=models.BooleanField(default=False)

    def save(self):
        usuario=self.usuario
        usuario.is_staff=True
        usuario.is_active=True
        usuario.save()
        super(myUsuario,self).save()

    def nombre_y_apellido(self):
        return "%s %s "%(self.usuario.first_name,self.usuario.last_name)

    def is_active(self):
        return self.usuario.is_active

    def is_staff(self):
        return self.usuario.is_staff

    def is_superuser(self):
        return self.usuario.is_superuser

    def email(self):
        return self.usuario.email

    def __str__(self):
        return "%s | %s"%(self.usuario,self.empresa)
