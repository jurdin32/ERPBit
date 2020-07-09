from django.contrib import admin

# Register your models here.
from NOTIFICACIONES.models import listMensajes, Mensajes, listMensajesChat, MensajesChat, Thread


class MensajesAmin(admin.ModelAdmin):
    list_display_links = listMensajes
    list_display = listMensajes
admin.site.register(Mensajes,MensajesAmin)

class MensajesChatAdmin(admin.ModelAdmin):
    list_display = listMensajesChat
    list_display_links = listMensajesChat
admin.site.register(MensajesChat,MensajesChatAdmin)

admin.site.register(Thread)
