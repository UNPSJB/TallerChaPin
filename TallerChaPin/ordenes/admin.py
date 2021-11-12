from django.contrib import admin

from .models import (OrdenDeTrabajo, DetalleOrdenDeTrabajo, MaterialOrdenDeTrabajo, RepuestoOrdenDeTrabajo,
                     Presupuesto, PlanillaDePintura, DetallePlanillaDePintura, PresupuestoMaterial, PresupuestoRepuesto)
# Register your models here.


class PresupuestoMaterialInline(admin.TabularInline):
    model = Presupuesto.materiales.through

class PresupuestoAdmin(admin.ModelAdmin):
    inlines = [
        PresupuestoMaterialInline,
    ]
class MaterialAdmin(admin.ModelAdmin):
    inlines = [
        PresupuestoMaterialInline,
    ]
    exclude = ('presupuesto',)

admin.site.register(OrdenDeTrabajo)
admin.site.register(DetalleOrdenDeTrabajo)
admin.site.register(MaterialOrdenDeTrabajo)
admin.site.register(RepuestoOrdenDeTrabajo)
admin.site.register(Presupuesto,PresupuestoAdmin)
admin.site.register(PlanillaDePintura)
admin.site.register(DetallePlanillaDePintura)
admin.site.register(PresupuestoMaterial)
admin.site.register(PresupuestoRepuesto)


