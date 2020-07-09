from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
# Create your views here.
from CONFIGURACION.models import Permiso, Items
from CONFIGURACION.views import funciones_usuario
from NOTIFICACIONES.models import Mensajes, Thread, MensajesChat
from USERS.models import myUsuario


def noticias(request):
    usuario = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=usuario.grupo)
    contexto={
        'empresa': usuario.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),  # Funciones.objects.all().order_by("id"),
        'items': Items.objects.all().order_by("prioridad"),
        'usuario':usuario,
        'mensajes':Mensajes.objects.filter(destino=usuario.usuario).order_by('-id')
    }
    return render(request, 'Notificaciones/inbox.html',contexto)

def visualizarMensaje(request,id):
    usuario = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=usuario.grupo)
    mensaje=Mensajes.objects.get(id=id)
    mensaje.estado=True
    mensaje.save()
    contexto={
        'empresa': usuario.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),  # Funciones.objects.all().order_by("id"),
        'items': Items.objects.all().order_by("prioridad"),
        'usuario': usuario,
        'mensajes': Mensajes.objects.filter(destino=usuario.usuario).order_by('-id'),
        'mensajeUI':mensaje,
    }
    return render(request,'Notificaciones/codes/visualizar.html',contexto)

def responderMensaje(request, id):
    usuario = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=usuario.grupo)
    mensaje=None
    mensaje = Mensajes.objects.get(id=id)
    mensaje.estado = True
    mensaje.save()
    if request.POST:
        mensaje=Mensajes(principal_id=id,asunto=request.POST['asunto'],prioridad='A',origen=usuario,destino=mensaje.origen.usuario,mensaje=request.POST['mensaje'])
        mensaje.save()
        contexto = {
            'empresa': usuario.empresa,
            'permisos': permisos,
            'funciones': funciones_usuario(permisos),  # Funciones.objects.all().order_by("id"),
            'items': Items.objects.all().order_by("prioridad"),
            'usuario': usuario,
            'mensajes': Mensajes.objects.filter(destino=usuario.usuario).order_by('-id'),
            'mensajeUI': mensaje,
            'mensaje': "Tu mensaje se envio con exito."
        }
        return render(request, 'Notificaciones/inbox.html', contexto)
    contexto = {
        'empresa': usuario.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),  # Funciones.objects.all().order_by("id"),
        'items': Items.objects.all().order_by("prioridad"),
        'usuario': usuario,
        'mensajes': Mensajes.objects.filter(destino=usuario.usuario).order_by('-id'),
        'mensajeUI': mensaje,
    }
    return render(request, 'Notificaciones/codes/responder.html', contexto)



def componerMensaje(request):
    usuario = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=usuario.grupo)
    mensaje = ''
    if request.POST:
        print(request.POST['usuarios'])
        users=request.POST['usuarios'].split(",")
        for user in users:
            try:
                destino=User.objects.get(username=user)
                mensajess = Mensajes(asunto=request.POST['asunto'], prioridad='A', origen=usuario, mensaje=request.POST['mensaje'],destino=destino)
                mensajess.save()
            except:
                error="Es posible que al menos un usuario no este disponible"
        mensaje="Tu mensaje se envio con exito."
    contexto = {
        'empresa': usuario.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),  # Funciones.objects.all().order_by("id"),
        'items': Items.objects.all().order_by("prioridad"),
        'usuario': usuario,
        'mensajes': Mensajes.objects.filter(destino=usuario.usuario).order_by('-id'),
        'mensaje': mensaje,
        'usuarios': User.objects.all(),
        'usuariosEmp':myUsuario.objects.filter(empresa=usuario.empresa),
    }
    return render(request, 'Notificaciones/codes/componer.html', contexto)


#messenger
def hilos(request):
    hilos = Thread.objects.filter(usuarios=request.user)
    usuario=myUsuario.objects.get(usuario=request.user)
    contexto={
        'hilos':hilos,
        'usuarios':myUsuario.objects.filter(empresa=usuario.empresa)
    }
    print("Hilos del usuario",hilos)
    return render(request, 'Notificaciones/Chat/thread_list.html',contexto)


def agregarMensaje(request,pk):
    contexto = {'creado': False}
    print(request.GET)
    hilo=get_object_or_404(Thread,pk=pk)
    print(hilo)
    msj=MensajesChat.objects.create(user=request.user,contenido=request.GET['msj'])
    hilo.mensajes.add(msj)
    print("este es el hilo",hilo)
    contexto = {'creado': True}


    return JsonResponse(contexto)

def mensajesHilo(request):
    pass

