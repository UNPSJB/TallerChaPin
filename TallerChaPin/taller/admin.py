from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Marca, Modelo
# Register your models here.


class MarcaAdmin(admin.ModelAdmin):
    pass


class ModeloAdmin(admin.ModelAdmin):
    pass


admin.site.register(Marca, MarcaAdmin)
admin.site.register(Modelo, ModeloAdmin)
# admin.site.register(Permission)
