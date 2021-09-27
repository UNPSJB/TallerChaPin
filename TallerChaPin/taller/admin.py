from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Marca, Modelo, Cliente
# Register your models here.


class MarcaAdmin(admin.ModelAdmin):
    ordering = ('nombre', )


class ModeloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'descripcion')
    list_filter = ('marca',)
    ordering = ('marca', 'nombre')

class ClienteAdmin(admin.ModelAdmin):
    ordering = ('dni', )


admin.site.register(Marca, MarcaAdmin)
admin.site.register(Modelo, ModeloAdmin)
admin.site.register(Cliente, ClienteAdmin)
# admin.site.register(Permission)
