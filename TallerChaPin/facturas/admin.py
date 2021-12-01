from django.contrib import admin

from .models import Factura, Pago
# Register your models here.

admin.site.register(Factura)
admin.site.register(Pago)