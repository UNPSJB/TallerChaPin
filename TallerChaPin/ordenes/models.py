from django.utils.timezone import now
from taller.models import (
    Empleado,
    Cliente,
    Vehiculo,
    Tarea,
    Material,
    Repuesto
)
from django.db import models
from django.conf import settings
# Create your models here.


class OrdenDeTrabajoManager(models.Manager):
    def para_el_dia(self, fecha):
        return self.filter(turno__date=fecha.date())


class OrdenDeTrabajoQuerySet(models.QuerySet):
    pass


class NoEntregoVehiculoException(Exception):
    def __init__(self, message, estado) -> None:
        super().__init__(message)
        self.estado = estado


class OrdenDeTrabajo(models.Model):
    CREADA = 0
    ACTIVA = 1
    CANCELADA = 2
    PAUSADA = 3
    REALIZADA = 4
    FACTURADA = 5
    FINALIZADA = 6
    INICIADA = 7
    ESTADOS_CHOICES = [
        # Para cuando se crea, recien salida del presupuesto
        (CREADA, 'Creada'),
        (ACTIVA, 'Activa'),             # Para cuando se ingresa el vehiculo
        (INICIADA, 'Iniciada'),         # Cuando se inicia la primera tarea
        (PAUSADA, 'Pausada'),           # Cuando se amplia el presupuesto
        (CANCELADA, 'Cancelada'),       # Cuando se cancela la orden
        (REALIZADA, 'Realizada'),       # Cuando se terminan todas las tareas
        (FACTURADA, 'Facturada'),       # Cuando se factura la orden
        (FINALIZADA, 'Finalizada'),     # Cuando se entrega el vehiculo
    ]
    materiales = models.ManyToManyField(
        Material, through='MaterialOrdenDeTrabajo')
    repuestos = models.ManyToManyField(
        Repuesto, through='RepuestoOrdenDeTrabajo')
    turno = models.DateTimeField()
    ingreso = models.DateTimeField(null=True, blank=True)
    egreso = models.DateTimeField(null=True, blank=True)
    estado = models.PositiveSmallIntegerField(
        choices=ESTADOS_CHOICES, default=CREADA)
    objects = OrdenDeTrabajoManager.from_queryset(OrdenDeTrabajoQuerySet)()

    def agregar_tarea(self, tarea):
        return DetalleOrdenDeTrabajo.objects.create(tarea=tarea, orden=self)

    def agregar_material(self, material, cantidad):
        if not any([d.tarea.tipo.materiales for d in self.detalles.all()]):
            raise Exception('La orden no requiere materiales')
        return MaterialOrdenDeTrabajo.objects.create(material=material, orden=self, cantidad=cantidad)

    def agregar_repuesto(self, repuesto, cantidad):
        if not any([d.tarea.tipo.repuestos for d in self.detalles.all()]):
            raise Exception('La orden no requiere repuestos')
        return RepuestoOrdenDeTrabajo.objects.create(repuesto=repuesto, orden=self, cantidad=cantidad)

    def cambiar_turno(self, fecha):
        otras = OrdenDeTrabajo.objects.para_el_dia(fecha)
        otras = otras.exclude(pk=self.pk)
        if len(otras) >= settings.CAPACIDAD_TALLER:
            raise Exception(
                'Ya existen vehiculos para esa fecha por sobre la capacidad del taller')
        self.turno = fecha
        self.save()

    def registrar_ingreso(self, fecha):
        self.ingreso = fecha
        self.estado = OrdenDeTrabajo.ACTIVA
        self.save()

    def registrar_egreso(self, fecha):
        if self.estado == OrdenDeTrabajo.FACTURADA or self.cliente.vip():
            self.egreso = fecha
            self.estado = OrdenDeTrabajo.FINALIZADA if self.estado == OrdenDeTrabajo.FACTURADA else self.estado
            self.save()
        else:
            raise NoEntregoVehiculoException(
                'No se puede entregar el vehiculo o me pagas o sos vip', self.estado)

    @property
    def cliente(self):
        return self.presupuestos.all().first().cliente

    @property
    def vehiculo(self):
        return self.presupuestos.all().first().vehiculo

    def tareas_para_empleado(self, empleado):
        return [d for d in self.detalles.all() if empleado.puede_hacer(d.tarea.tipo)]

    def iniciar_tarea(self, empleado, tarea, fecha=now()):
        if self.estado == OrdenDeTrabajo.ACTIVA:
            tarea.iniciar(empleado, fecha)
            self.estado = OrdenDeTrabajo.INICIADA
            self.save()

    def finalizar_tarea(self, detalle, exitosa, observacion, materiales=None, repuestos=None, fecha=now()):
        # Materiales y repuestos son listas de la forma [(material, cantidad)...]
        if detalle.tarea.tipo.materiales and materiales is None:
            raise Exception('Tarea requiere materiales')
        elif detalle.tarea.tipo.materiales:
            for material, cantidad in materiales:
                self.orden_materiales.filter(
                    pk=material).update(cantidad=cantidad)
        if detalle.tarea.tipo.repuestos and repuestos is None:
            raise Exception('Tarea requiere repuestos')
        elif detalle.tarea.tipo.repuestos:
            for repuesto, cantidad in repuestos:
                self.orden_repuestos.filter(
                    pk=repuesto).update(cantidad=cantidad)
        if detalle.tarea.tipo.planilla and not detalle.planillas.exists():
            raise Exception('La orden requiere planilla de pintura')
        if self.estado == OrdenDeTrabajo.INICIADA:
            detalle.finalizar(exitosa, observacion, fecha)
            un_problema = any([not d.exitosa for d in self.detalles.all()])
            todo_terminado = all([d.fin != None for d in self.detalles.all()])
            if un_problema:
                self.estado = OrdenDeTrabajo.PAUSADA
            elif todo_terminado:
                self.estado = OrdenDeTrabajo.REALIZADA
            self.save()

    def ampliar_presupuesto(self):
        return Presupuesto.objects.create(
            orden=self,
            cliente=self.cliente,
            vehiculo=self.vehiculo
        )


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

    def iniciar(self, empleado, fecha=now()):
        self.empleado = empleado
        self.inicio = fecha
        self.save()

    def finalizar(self, exitosa, observaciones, fecha=now()):
        self.exitosa = exitosa
        self.observaciones = observaciones
        self.fin = fecha
        self.save()

    def crear_planilla_de_pintura(self, material, componentes):
        # Componentes es una lista de la forma [(formula, cantidad)...]
        planilla = PlanillaDePintura.objects.create(
            orden=self, nombre_de_color=material.nombre)
        for formula, cantidad in componentes:
            planilla.agregar(formula, cantidad)

    def precio(self):
        return self.tarea.precio


class MaterialOrdenDeTrabajo(models.Model):
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name='ordenes_de_trabajo')
    orden = models.ForeignKey(
        OrdenDeTrabajo, on_delete=models.CASCADE, related_name='orden_materiales')
    cantidad = models.PositiveBigIntegerField()

    def precio(self):
        return self.material.precio * self.cantidad


class RepuestoOrdenDeTrabajo(models.Model):
    repuesto = models.ForeignKey(
        Repuesto, on_delete=models.CASCADE, related_name='ordenes_de_trabajo')
    orden = models.ForeignKey(
        OrdenDeTrabajo, on_delete=models.CASCADE, related_name='orden_repuestos')
    cantidad = models.PositiveBigIntegerField()

    def precio(self):
        return self.repuesto.precio * self.cantidad


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
    validez = models.PositiveIntegerField(default=settings.CANTIDAD_VALIDEZ_PRESUPUESTO)
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

    def confirmar(self, turno):
        if self.orden is None:
            self.orden = OrdenDeTrabajo.objects.create(turno=turno)
        else:
            # FIXME: Que pasa si una tarea se bloquea o no es exitosa por otra cosa que no implique ampliar el presupuesto?
            self.orden.estado = OrdenDeTrabajo.INICIADA
            self.orden.detalles.all().update(exitosa=True)
            self.orden.save()
        for t in self.tareas.all():
            self.orden.agregar_tarea(t)
        for m in self.presupuesto_materiales.all():
            self.orden.agregar_material(m.material, m.cantidad)
        for r in self.presupuesto_repuestos.all():
            self.orden.agregar_repuesto(r.repuesto, r.cantidad)
        self.save()
        return self.orden

    def cantidad_detalles(self):
        return self.tareas.count() + self.materiales.count() + self.repuestos.count()


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
    orden = models.ForeignKey(
        DetalleOrdenDeTrabajo, on_delete=models.CASCADE, related_name='planillas')
    fecha = models.DateTimeField(auto_now_add=True)
    # Blanco nieve, Gris Topo, Azul Topo, Verde aceituna, etc
    nombre_de_color = models.CharField(max_length=100)

    def agregar(self, formula, cantidad):
        return DetallePlanillaDePintura.objects.create(planilla=self, formula=formula, cantidad=cantidad)


class DetallePlanillaDePintura(models.Model):
    planilla = models.ForeignKey(
        PlanillaDePintura, related_name="detalles", on_delete=models.CASCADE)
    formula = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()  # en gramos
