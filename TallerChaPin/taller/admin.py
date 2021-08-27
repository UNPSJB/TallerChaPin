from django.contrib import admin

from .models import Marca, Modelo
# Register your models here.


class MarcaAdmin(admin.ModelAdmin):
    pass


class ModeloAdmin(admin.ModelAdmin):
    pass


admin.site.register(Marca, MarcaAdmin)
admin.site.register(Modelo, ModeloAdmin)
