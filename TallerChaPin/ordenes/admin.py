from django.contrib import admin

from .models import (OrdenDeTrabajo, DetalleOrdenDeTrabajo, MaterialOrdenDeTrabajo, RepuestoOrdenDeTrabajo,
                     Presupuesto, PlanillaDePintura, DetallePlanillaDePintura, PresupuestoMaterial, PresupuestoRepuesto)
# Register your models here.

admin.site.register(OrdenDeTrabajo)
admin.site.register(DetalleOrdenDeTrabajo)
admin.site.register(MaterialOrdenDeTrabajo)
admin.site.register(RepuestoOrdenDeTrabajo)
admin.site.register(Presupuesto)
admin.site.register(PlanillaDePintura)
admin.site.register(DetallePlanillaDePintura)
admin.site.register(PresupuestoMaterial)
admin.site.register(PresupuestoRepuesto)
