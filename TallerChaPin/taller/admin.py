from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Marca, Modelo
# Register your models here.


class MarcaAdmin(admin.ModelAdmin):
    fields = ('name', 'title', 'view_birth_date')
    ordering = ('nombre', )


class ModeloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'descripcion')
    list_filter = ('marca',)
    ordering = ('marca', 'nombre')


admin.site.register(Marca, MarcaAdmin)
admin.site.register(Modelo, ModeloAdmin)
# admin.site.register(Permission)
