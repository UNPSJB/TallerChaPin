from taller.models import (
    Empleado,
    Cliente,
    Vehiculo,
    Tarea,
    Material,
    Repuesto
)
from django.db import models
# Create your models here.


class OrdenDeTrabajo(models.Model):
    CREADA = 0
    ACTIVA = 1
    CANCELADA = 2
    PAUSADA = 3
    REALIZADA = 4
    #FINALIZADA = 5
    FACTURADA = 5
    ESTADOS_CHOICES = [
        # Para cuando se crea, recien salida del presupuesto
        (CREADA, 'Creada'),
        (ACTIVA, 'Activa'),             # Para cuando se ingresa el vehiculo
        (PAUSADA, 'Pausada'),           # Cuando se amplia el presupuesto
        (CANCELADA, 'Cancelada'),       # Cuando se cancela la orden
        (REALIZADA, 'Realizada'),       # Cuando se terminan todas las tareas
        # (FINALIZADA, 'Finalizada'),    Cuando se entrega el vehiculo
        (FACTURADA, 'Facturada'),       # Cuando se entrega el vehiculo
    ]
    materiales = models.ManyToManyField(Material)
    repuestos = models.ManyToManyField(Repuesto)
    turno = models.DateTimeField(auto_now_add=True)
    ingreso = models.DateTimeField(null=True, blank=True)
    egreso = models.DateTimeField(null=True, blank=True)
    estado = models.PositiveSmallIntegerField(
        choices=ESTADOS_CHOICES, default=CREADA)

    def ampliar_presupuesto(self, tareas, materiales, repuestos):
        return Presupuesto(tareas, materiales, repuestos, self)

    def agregar_tarea(self, tarea):
        return DetalleOrdenDeTrabajo(tarea=tarea, orden=self)


class DetalleOrdenDeTrabajo(models.Model):
    orden = models.ForeignKey(
        OrdenDeTrabajo, related_name="detalles", on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    empleado = models.ForeignKey(
        Empleado, null=True, blank=True, on_delete=models.CASCADE)
    inicio = models.DateTimeField(null=True, blank=True)
    fin = models.DateTimeField(null=True, blank=True)
    exitosa = models.BooleanField(default=True)
    observaciones = models.CharField(max_length=200, null=True, blank=True)

    @classmethod
    def crear(cls, tarea):
        return cls(tarea=tarea)


class Presupuesto(models.Model):
    cliente = models.ForeignKey(
        Cliente, related_name='presupuestos', on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(
        Vehiculo, related_name='presupuestos', on_delete=models.CASCADE)
    detalles = models.CharField(max_length=200)
    tareas = models.ManyToManyField(Tarea, related_name='presupuestos')
    materiales = models.ManyToManyField(
        Material, through='PresupuestoMaterial')
    repuestos = models.ManyToManyField(Repuesto, through='PresupuestoRepuesto')
    validez = models.PositiveIntegerField(default=60)
    orden = models.ForeignKey(OrdenDeTrabajo, null=True, related_name='presupuestos',
                              blank=True, on_delete=models.SET_NULL)

    def agregar_tarea(self, tarea):
        self.tareas.add(tarea)

    def agregar_material(self, material, cantidad):
        return PresupuestoMaterial.objects.create(material=material, presupuesto=self, cantidad=cantidad)

    def agregar_repuesto(self, repuesto, cantidad=1):
        return PresupuestoRepuesto.objects.create(repuesto=repuesto, presupuesto=self, cantidad=cantidad)

    def precio_estimado(self):
        tareas = self.tareas.all().aggregate(
            models.Sum('precio'))['precio__sum']
        materiales = sum([r.precio()
                         for r in self.presupuesto_materiales.all()])
        repuestos = sum([r.precio() for r in self.presupuesto_repuestos.all()])
        return tareas + materiales + repuestos

    def confirmar(self):
        self.orden = OrdenDeTrabajo.objects.create()
        for t in self.tareas.all():
            self.orden.agregar_tarea(t)
        return self.orden


class PresupuestoMaterial(models.Model):
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name='presupuestos')
    presupuesto = models.ForeignKey(
        Presupuesto, on_delete=models.CASCADE, related_name='presupuesto_materiales')
    cantidad = models.PositiveBigIntegerField()

    def precio(self):
        return self.material.precio * self.cantidad


class PresupuestoRepuesto(models.Model):
    repuesto = models.ForeignKey(
        Repuesto, on_delete=models.CASCADE, related_name='presupuestos')
    presupuesto = models.ForeignKey(
        Presupuesto, on_delete=models.CASCADE, related_name='presupuesto_repuestos')
    cantidad = models.PositiveBigIntegerField()

    def precio(self):
        return self.repuesto.precio * self.cantidad


class PlanillaDePintura(models.Model):
    orden = models.ForeignKey(DetalleOrdenDeTrabajo, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    # Blanco nieve, Gris Topo, Azul Topo, Verde aceituna, etc
    nombre_de_color = models.CharField(max_length=100)


class DetallePlanillaDePintura(models.Model):
    planilla = models.ForeignKey(
        PlanillaDePintura, related_name="detalles", on_delete=models.CASCADE)
    formula = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()  # en gramos
