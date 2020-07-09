from django.contrib import admin

# Register your models here.
from USERS.models import listMyEmpresa, myUsuario


class myUserAdmin(admin.ModelAdmin):
    list_display_links = listMyEmpresa
    list_display = listMyEmpresa
admin.site.register(myUsuario,myUserAdmin)