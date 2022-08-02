from django.utils.timezone import now
from django.utils import timezone
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
from django.core.exceptions import ValidationError
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

def fecha_es_futura(fecha):
    if fecha < timezone.now():
        raise ValidationError('Fecha no válida')

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
    turno = models.DateTimeField(validators=[fecha_es_futura])
    ingreso = models.DateTimeField(null=True, blank=True)
    egreso = models.DateTimeField(null=True, blank=True)
    estado = models.PositiveSmallIntegerField(
        choices=ESTADOS_CHOICES, default=CREADA)
    objects = OrdenDeTrabajoManager.from_queryset(OrdenDeTrabajoQuerySet)()

    class Meta:
        permissions = [
            ('can_registrar_ingreso',
             'Puede registrar el ingreso de un vehículo al taller'),
            ('can_asignar_trabajo', 'Puede asignar trabajo a empleados'),
        ]

    def detalles_por_finalizar(self):
        por_finalizar = 0

        for detalle in self.detalles.all():
            if not detalle.esta_finalizado():
                por_finalizar += 1

        return por_finalizar

    def cancelar_orden_creada(self):
        orden_cancelada = models.Q(orden__estado=OrdenDeTrabajo.CANCELADA)
        self.estado = orden_cancelada
        self.save()
    

    def precio_total_presupuestado(self):
        # Toma el valor del primer presupuesto realizado
        return self.presupuestos.first().precio_estimado()

    # Se cambio porque el sumar todos los presupuestos no refleja el total de la orden 
    # def precio_total(self): 
    #     # Toma el valor del presupuesto + sus ampliaciones realizadas
    #     return sum([p.precio_estimado() for p in self.presupuestos.all()]) 

    # Toma el valor de lo que se utilizo en la orden de trabajo para calcular el precio total de los trabajos realizados y materiales/repuestos usados
    def precio_orden(self):
        tareas = sum([t.precio() for t in self.detalles.all()])
        materiales = sum([m.precio() for m in self.orden_materiales.all()])
        repuestos = sum([r.precio() for r in self.orden_repuestos.all()])        
        return tareas + materiales + repuestos

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
                'No se puede entregar el vehículo o me pagas o sos vip', self.estado)

    def no_hay_tareas_iniciadas(self):
        for detalle in self.detalles.all():
            if detalle.inicio != None:
                return False
        return True

    def puede_cancelarse(self):
        return (self.estado == OrdenDeTrabajo.CREADA) or (self.estado == OrdenDeTrabajo.PAUSADA)

    def puede_cambiar_turno(self):
        return self.estado == OrdenDeTrabajo.CREADA

    def puede_facturarse(self):
        return self.estado == OrdenDeTrabajo.REALIZADA

    def puede_pausarse(self):
        return (self.estado == OrdenDeTrabajo.ACTIVA) or (self.estado == OrdenDeTrabajo.INICIADA)

    def puede_reanudarse(self):
        return (self.estado == OrdenDeTrabajo.PAUSADA)
    
    def puede_ampliarse(self):
        return (self.estado == OrdenDeTrabajo.PAUSADA)

    @property
    def cliente(self):
        presupuesto = self.presupuestos.all().first()
        return presupuesto.cliente if presupuesto is not None else None

    @property
    def vehiculo(self):
        vehiculo = self.presupuestos.all().first()
        return vehiculo.vehiculo if vehiculo is not None else None

    def tareas_para_empleado(self, empleado):
        return [d for d in self.detalles.all() if empleado.puede_hacer(d.tarea.tipo)]

    # Método que no se está ejecutando nunca
    def iniciar_tarea(self, empleado, tarea, fecha=now()):
        if self.estado == OrdenDeTrabajo.ACTIVA:
            tarea.iniciar(empleado, fecha)
            self.estado = OrdenDeTrabajo.INICIADA
            self.save()
    
    # Ver si de verdad lo necesitamos
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
                self.estado = OrdenDeTrabajo.REALIZADA  # VER ESTO
            self.save()

    def ampliar_presupuesto(self):
        return Presupuesto.objects.create(
            orden=self,
            cliente=self.cliente,
            vehiculo=self.vehiculo
        )

    def __str__(self):
        if self.cliente and self.vehiculo:
            return f"{self.pk} | {self.cliente.nombre} - {self.vehiculo.modelo.marca} {self.vehiculo.modelo.nombre} ({self.vehiculo.patente})"
        else:
            return f"{self.pk} | (inconsistencia en cliente/vehiculo)" # Agregado ya que al haber inconsistencias se rompía en /admin

    def actualizar_material(self, material, cantidad):
        materiales = self.orden_materiales.filter(material=material)
        if materiales.exists():
            material = materiales.first()
            material.actualizar(cantidad)
        elif cantidad > 0:
            material = Material.objects.get(pk=material.pk)
            MaterialOrdenDeTrabajo.objects.create(
                material=material, orden=self, cantidad=cantidad)

    def actualizar_repuesto(self, repuesto, cantidad):
        repuestos = self.orden_repuestos.filter(repuesto=repuesto)
        if repuestos.exists():
            repuesto = repuestos.first()
            repuesto.actualizar(cantidad)
        elif cantidad > 0:
            repuesto = Repuesto.objects.get(pk=repuesto.pk)
            RepuestoOrdenDeTrabajo.objects.create(
                repuesto=repuesto, orden=self, cantidad=cantidad)

    def actualizar_estado(self):
        print(self.detalles.all())

    def get_ultimo_presupuesto(self):
        return self.presupuestos.all().order_by('fecha').last()
        

class DetalleOrdenDeTrabajoManager(models.Manager):
    def para_empleado(self, empleado):
        no_tiene_empleado = models.Q(empleado__isnull=True)
        tiene_empleado = models.Q(empleado__isnull=False)
        soy_empleado = models.Q(empleado__pk=empleado.pk)
        no_iniciada = models.Q(inicio__isnull=True)
        orden_pausada = models.Q(orden__estado=OrdenDeTrabajo.PAUSADA)
        empleado_realiza_tarea = models.Q(tarea__tipo__empleados=empleado)

        qs = self.filter(
            ((no_tiene_empleado | orden_pausada |
             (tiene_empleado & soy_empleado & no_iniciada))
             & empleado_realiza_tarea)
        ).order_by('orden__turno')

        return qs


    def para_empleado_hoy(self, empleado):
        return self.para_empleado(empleado).filter(inicio__date=now().date())

    def sin_asignar(self):
        no_tiene_empleado = models.Q(empleado__isnull=True)
        ha_ingresado = models.Q(orden__ingreso__isnull=False)
        print("test:")
        qs = self.filter(no_tiene_empleado and ha_ingresado).order_by('orden__turno')
        print(qs)
        # print(qs.first().orden.ingreso)
        return qs

    def asignados(self):
        tiene_empleado = models.Q(empleado__isnull=False)
        no_esta_iniciado = models.Q(inicio__isnull=True)

        qs = self.filter(tiene_empleado & no_esta_iniciado).order_by(
            'orden__turno')
        return qs

    def sin_finalizar(self):
        tiene_empleado = models.Q(empleado__isnull=False)
        esta_iniciado = models.Q(inicio__isnull=False)
        no_esta_finalizado = models.Q(fin__isnull=True)
        qs = self.filter(tiene_empleado & no_esta_finalizado &
                         esta_iniciado).order_by('orden__turno')
        return qs

    # def en_proceso(self):
    #     esta_empezado = models.Q(inicio__isnull=False)
    #     no_esta_finalizado = models.Q(fin__isnull=True)
    #     qs = self.filter(esta_empezado & no_esta_finalizado).order_by('orden__turno')
    #     return qs

    def finalizados(self):
        esta_finalizado = models.Q(fin__isnull=False)
        qs = self.filter(esta_finalizado).order_by('orden__turno')
        return qs


class DetalleOrdenDeTrabajoQuerySet(models.QuerySet):
    pass


class DetalleOrdenDeTrabajo(models.Model):
    orden = models.ForeignKey(
        OrdenDeTrabajo, related_name="detalles", on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name="detallesorden")
    empleado = models.ForeignKey(
        Empleado, null=True, blank=True, related_name="trabajo", on_delete=models.CASCADE)
    inicio = models.DateTimeField(null=True, blank=True)
    fin = models.DateTimeField(null=True, blank=True)
    exitosa = models.BooleanField(default=True)
    observaciones = models.CharField(max_length=200, null=True, blank=True)
    objects = DetalleOrdenDeTrabajoManager.from_queryset(
        DetalleOrdenDeTrabajoQuerySet)()

    @classmethod
    def crear(cls, tarea):
        return cls(tarea=tarea)

    def precio(self):
        return self.tarea.precio

    def iniciar(self, empleado, fecha=now()):
        self.empleado = empleado
        self.inicio = fecha
        self.save()
        if self.orden.estado == OrdenDeTrabajo.ACTIVA:
            self.orden.estado = OrdenDeTrabajo.INICIADA
            self.orden.save()

    def asignar(self, empleado):
        self.empleado = empleado
        self.save()

    def finalizar(self, exitosa, observaciones, fecha=now()):
        self.exitosa = exitosa
        self.observaciones = observaciones
        self.fin = fecha
        self.save()

        if self.orden.estado == OrdenDeTrabajo.INICIADA and self.orden.detalles_por_finalizar() == 0:
            self.orden.estado = OrdenDeTrabajo.REALIZADA
            self.orden.save()


    def crear_planilla_de_pintura(self, material, componentes):
        # Componentes es una lista de la forma [(formula, cantidad)...]
        planilla = PlanillaDePintura.objects.create(
            orden=self, nombre_de_color=material.nombre)
        for formula, cantidad in componentes:
            planilla.agregar(formula, cantidad)

    def color_de_pintura (self):
        material = self.orden.materiales.filter(tipo__nombre__icontains = 'pintura').first() 
        return material.nombre if material is not None else "Pintura original"


    def precio(self):
        return self.tarea.precio

    def puedo_iniciar(self):
        return self.orden.estado == OrdenDeTrabajo.ACTIVA or OrdenDeTrabajo.INICIADA and self.inicio is None

    def puedo_finalizar(self):
        requiere_planilla = self.tarea.tipo.planilla
        tiene_planilla = self.planillas.exists()
        esta_iniciada = self.inicio is not None
        no_esta_finalizada = self.fin is None
        return no_esta_finalizada and esta_iniciada and (requiere_planilla and tiene_planilla or not requiere_planilla)
    
    def requiere_planilla (self):
        return self.tarea.tipo.planilla

    def puedo_asignar(self):
        return self.empleado is None

    def esta_sin_iniciar(self):
        return self.inicio is None

    def esta_en_proceso(self):
        return self.inicio is not None and self.fin is None

    def esta_finalizado(self):
        return self.fin is not None

    def requiere_planilla(self):
        return self.tarea.tipo.planilla

    def esta_pausado(self):
        return self.orden.estado == OrdenDeTrabajo.PAUSADA and self.fin == None # Si el detalle ya se finalizó, se muestra como finalizado y no como pausado.

    def actualizar_cantidad(self, material, cantidad_material, repuesto, cantidad_repuesto):
        orden = self.orden
        if material is not None:
            orden.actualizar_material(material, cantidad_material)
        if repuesto is not None:
            orden.actualizar_repuesto(repuesto, cantidad_repuesto)

    def get_titulo(self):
        return f"{self.tarea} (#{self.orden.pk})"



class MaterialOrdenDeTrabajo(models.Model):
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name='ordenes_de_trabajo')
    orden = models.ForeignKey(
        OrdenDeTrabajo, on_delete=models.CASCADE, related_name='orden_materiales')
    cantidad = models.PositiveBigIntegerField()

    def precio(self):
        return self.material.precio * self.cantidad

    def actualizar(self, cantidad):
        self.cantidad += cantidad
        if self.cantidad >= 0:
            self.save()


class RepuestoOrdenDeTrabajo(models.Model):
    repuesto = models.ForeignKey(
        Repuesto, on_delete=models.CASCADE, related_name='ordenes_de_trabajo')
    orden = models.ForeignKey(
        OrdenDeTrabajo, on_delete=models.CASCADE, related_name='orden_repuestos')
    cantidad = models.PositiveBigIntegerField()

    def precio(self):
        return self.repuesto.precio * self.cantidad

    def actualizar(self, cantidad):
        self.cantidad += cantidad
        if self.cantidad >= 0:
            self.save()

# class PresupuestoAmpliado(model.Model): tentativo

class Presupuesto(models.Model):
    cliente = models.ForeignKey(
        Cliente, related_name='presupuestos', on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(
        Vehiculo, related_name='presupuestos', on_delete=models.CASCADE)
    detalles = models.CharField(max_length=200, blank=True)
    tareas = models.ManyToManyField(Tarea, related_name='presupuestos')
    materiales = models.ManyToManyField(
        Material, through='PresupuestoMaterial')
    repuestos = models.ManyToManyField(Repuesto, through='PresupuestoRepuesto')
    fecha = models.DateTimeField(auto_now_add=True)
    validez = models.PositiveIntegerField(
        default=settings.CANTIDAD_VALIDEZ_PRESUPUESTO)
    orden = models.ForeignKey(OrdenDeTrabajo, null=True, related_name='presupuestos',
                              blank=True, on_delete=models.SET_NULL)
    ampliado = models.BooleanField(default=False)

    def agregar_tarea(self, tarea):
        self.tareas.add(tarea)

    def agregar_material(self, material, cantidad):
        lista_materiales = list(self.materiales.all())
        if material in lista_materiales:
            pm_qs = PresupuestoMaterial.objects.filter(material=material, presupuesto=self)
            cantidad_existente = pm_qs.first().cantidad
            pm_qs.update(cantidad=cantidad_existente+cantidad)
        else: 
            return PresupuestoMaterial.objects.create(material=material, presupuesto=self, cantidad=cantidad)

    def agregar_repuesto(self, repuesto, cantidad=1):
        lista_repuestos = list(self.repuestos.all())
        if repuesto in lista_repuestos:
            pr_qs = PresupuestoRepuesto.objects.filter(repuesto=repuesto, presupuesto=self)
            cantidad_existente = pr_qs.first().cantidad
            pr_qs.update(cantidad=cantidad_existente+cantidad)
        else: 
            return PresupuestoRepuesto.objects.create(repuesto=repuesto, presupuesto=self, cantidad=cantidad)

    def vaciar(self):
        self.materiales.clear()
        self.repuestos.clear()
        self.tareas.clear()

    def precio_estimado(self):
        tareas = self.tareas.all().aggregate(models.Sum('precio'))['precio__sum']
        materiales = sum([r.precio() for r in self.presupuesto_materiales.all()])
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
            self.orden.agregar_material(m.material, 0)
        for r in self.presupuesto_repuestos.all():
            self.orden.agregar_repuesto(r.repuesto, 0)
        self.save()
        return self.orden

    def cantidad_detalles(self):
        return self.tareas.count() + self.materiales.count() + self.repuestos.count()

    def puede_confirmarse(self):
        return self.orden is None

    def puede_modificarse(self):
        return self.orden is None

    def tiene_orden(self):
        return self.orden is not None   

    def puede_cancelarse(self):
        return self.orden is None

    def tiene_anterior(self):
        if self.orden is None:
            return False

        presupuestos = list(self.orden.presupuestos.all().order_by('fecha'))
        if presupuestos.index(self) > 0:
            return True
        else:
            return False
        
    def get_diferencia_con_anterior(self):
        presupuestos = list(self.orden.presupuestos.all().order_by('fecha'))
        indice = presupuestos.index(self)
        anterior = presupuestos[indice-1]

        diferencia = presupuestos[indice].precio_estimado() - anterior.precio_estimado()
        if diferencia > 0:
            return f'+${diferencia}'
        else: 
            return f'-${abs(diferencia)}'

    def es_mas_caro(self):
        presupuestos = list(self.orden.presupuestos.all().order_by('fecha'))
        indice = presupuestos.index(self)
        anterior = presupuestos[indice-1]
        return presupuestos[indice].precio_estimado() - anterior.precio_estimado() > 0


def cantidad_positiva(v):
    if v <= 0:
        raise ValidationError('La cantidad de un insumo debe ser mayor a 0')

class PresupuestoMaterial(models.Model):
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name='presupuestos', null=True, blank=True)
    presupuesto = models.ForeignKey(
        Presupuesto, on_delete=models.CASCADE, related_name='presupuesto_materiales')
    cantidad = models.PositiveBigIntegerField(validators=[], null=True, blank=True, default=1)

    def precio(self):
        return self.material.precio * self.cantidad

class PresupuestoRepuesto(models.Model):
    repuesto = models.ForeignKey(
        Repuesto, on_delete=models.CASCADE, related_name='presupuestos', null=True, blank=True)
    presupuesto = models.ForeignKey(
        Presupuesto, on_delete=models.CASCADE, related_name='presupuesto_repuestos')
    cantidad = models.PositiveBigIntegerField(validators=[], null=True, blank=True, default=1)   # cantidad debe ser positiva

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


class TurnoOrden(models.Model):

    cliente = models.ForeignKey(
        Cliente, related_name='turno', on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(
        Vehiculo, related_name='turno', on_delete=models.CASCADE)
