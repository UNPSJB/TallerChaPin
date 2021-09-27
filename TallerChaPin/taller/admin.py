from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Empleado, Marca, Material, Modelo, Cliente, Repuesto, Tarea, TipoMaterial, TipoTarea
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
admin.site.register(TipoMaterial)
admin.site.register(Material)
admin.site.register(Repuesto)
admin.site.register(Tarea)
admin.site.register(TipoTarea)
admin.site.register(Empleado)
# admin.site.register(Permission)
