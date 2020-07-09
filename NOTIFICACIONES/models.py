from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import m2m_changed

from USERS.models import myUsuario

listMensajes=['id','principal','hora','asunto','prioridad','origen','destino','estado']
class Mensajes(models.Model):
    principal=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    hora=models.DateTimeField(auto_now_add=True)
    asunto=models.CharField(max_length=150,null=True,blank=True)
    mensaje=models.TextField()
    prioridad=models.CharField(max_length=3,null=True,blank=True)
    origen=models.ForeignKey(myUsuario, models.CASCADE, null=True,blank=True)
    destino=models.ForeignKey(User,models.CASCADE,null=True,blank=True)
    estado=models.BooleanField(default=False)

    def __str__(self):
        return self.mensaje



#crea objetos de recuperacion personalizados
class ThreadManager(models.Manager):
    def find(self,usuario1,usuario2):
        queryset=self.filter(usuarios=usuario1).filter(usuarios=usuario2)
        if len(queryset)>0:
            return queryset[0]
        return None

    def find_create(self,usuario1,usuario2):
        thread=self.find(usuario1,usuario2)

        if thread is None:
            threads=Thread.objects.create()
            threads.usuarios.add(usuario1,usuario2)
        return thread



#chat
listMensajesChat=['user','contenido','fecha']
class MensajesChat(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    contenido=models.TextField()
    fecha=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['fecha']


class Thread(models.Model):
    usuarios=models.ManyToManyField(User,related_name='threads')
    mensajes=models.ManyToManyField(MensajesChat)
    updated = models.DateTimeField(auto_now=True)

    objects = ThreadManager()


def mensajesCambio(sender,**kwargs):
    instanciaHilo=kwargs.pop("instanciaHilo",None)
    accion=kwargs.pop("accion",None)
    pk_set=kwargs.pop("pk_set",None)
    print(instanciaHilo,accion,pk_set)

    false_pk_set=set()

    if accion is 'pre_add':
        for mensaje_pk in pk_set:
            msg=Mensajes.objects.get(pk=mensaje_pk)
            if msg.user not in instanciaHilo.usuarios.all():
                print("no forma parte del hilo")
                false_pk_set.add(mensaje_pk)
    pk_set.difference_update(false_pk_set)

m2m_changed.connect(mensajesCambio, sender=Thread.mensajes.through)




