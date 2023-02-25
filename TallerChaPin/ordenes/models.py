from datetime import timedelta
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
from django.contrib.auth.models import Permission
# from facturas.models import Factura
# Create your models here.

class OrdenDeTrabajoManager(models.Manager):
    def para_el_dia(self, fecha):
        return self.filter(turno__date=fecha.date())

    def sin_ingresar(self):
        no_ha_ingresado = models.Q(ingreso__isnull=True)
        qs = self.filter(no_ha_ingresado)
        return qs


class OrdenDeTrabajoQuerySet(models.QuerySet):
    pass


class NoEntregoVehiculoException(Exception):
    def __init__(self, message, estado) -> None:
        super().__init__(message)
        self.estado = estado

def fecha_es_futura(fecha):
    ahora = timezone.now() - timedelta(hours=4)
    if fecha < ahora:
        raise ValidationError('Fecha no válida')
class OrdenDeTrabajo(models.Model):
    INICIAR_TAREA = 0
    PAUSAR_ORDEN = 1
    REANUDAR_ORDEN = 2
    FINALIZAR_ORDEN = 3
    FACTURAR_ORDEN = 4
    FINALIZAR_TAREA_EXITOSA = 5
    CANCELAR_ORDEN = 6
    FINALIZAR_TAREA_NO_EXITOSA = 7 
    
    CREADA = 0
    ACTIVA = 1
    CANCELADA = 2
    PAUSADA = 3
    REALIZADA = 4
    FACTURADA = 5
    FINALIZADA = 6
    INICIADA = 7
    PAGADA = 8
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
        (PAGADA, 'Pagada')              # Cuando se registra la factura tanto la factura como la orden quedan PAGADAS
    ]
    materiales = models.ManyToManyField(
        Material, through='MaterialOrdenDeTrabajo')
    repuestos = models.ManyToManyField(
        Repuesto, through='RepuestoOrdenDeTrabajo')
    turno = models.DateTimeField(validators=[fecha_es_futura])
    ingreso = models.DateTimeField(null=True, blank=False)
    egreso = models.DateTimeField(null=True, blank=False)
    estado = models.PositiveSmallIntegerField(
        choices=ESTADOS_CHOICES, default=CREADA)
    objects = OrdenDeTrabajoManager.from_queryset(OrdenDeTrabajoQuerySet)()

    @property
    def cliente(self):
        presupuesto = self.presupuestos.all().first()
        return presupuesto.cliente if presupuesto is not None else None

    @property
    def vehiculo(self):
        vehiculo = self.presupuestos.all().first()
        return vehiculo.vehiculo if vehiculo is not None else None

    class Meta:
        permissions = [
            ('can_registrar_ingreso','Puede registrar el ingreso de un vehículo al taller'),
            ('can_registrar_egreso', 'Puede registrar el egreso de un vehículo al taller')
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
        return MaterialOrdenDeTrabajo.objects.create(material=material, orden=self, cantidad_presupuestada=cantidad)

    def agregar_repuesto(self, repuesto, cantidad):
        if not any([d.tarea.tipo.repuestos for d in self.detalles.all()]):
            raise Exception('La orden no requiere repuestos')
        return RepuestoOrdenDeTrabajo.objects.create(repuesto=repuesto, orden=self, cantidad_presupuestada=cantidad)

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

        if fecha < self.ingreso:
            raise ValidationError('La fecha de egreso no puede ser menor a la fecha de ingreso')

        if self.puede_retirar_vehiculo() :
            if self.estado == OrdenDeTrabajo.PAGADA or self.cliente.vip(): 
                self.egreso = fecha
                self.estado = OrdenDeTrabajo.FINALIZADA if self.estado == OrdenDeTrabajo.FACTURADA or self.estado == OrdenDeTrabajo.PAGADA else self.estado
                self.save()
            else:
                raise NoEntregoVehiculoException(
                    'No se puede entregar el vehículo si el cliente no paga o no es VIP', self.estado)
        else:
            raise NoEntregoVehiculoException(
                'No se puede entregar el vehículo. Ver estado de la orden.', self.estado)

    def no_hay_tareas_iniciadas(self):
        for detalle in self.detalles.all():
            if detalle.inicio != None:
                return False
        return True

    def esta_pausada(self):
        return self.estado == OrdenDeTrabajo.PAUSADA

    def puede_cancelarse(self):
        return self.estado == OrdenDeTrabajo.CREADA or self.estado == OrdenDeTrabajo.PAUSADA

    def puede_cambiar_turno(self):
        return self.estado == OrdenDeTrabajo.CREADA

    # Método para dar estilos a los eventos del calendario de turnos
    def get_class_dot(self):
        estado = self.estado
        if estado == OrdenDeTrabajo.PAUSADA:
            return 'orden_pausada'
        elif estado == OrdenDeTrabajo.CANCELADA:
            return 'orden_cancelada'
        elif estado == OrdenDeTrabajo.CREADA:
            return 'orden_creada'
        elif estado == OrdenDeTrabajo.INICIADA or estado == OrdenDeTrabajo.ACTIVA:
            return 'orden_iniciada'
        else: 
            return 'orden_default'
        
    def actualizar_estado(self, evento):
        # Si la evento fue INICIAR_TAREA paso el estado a iniciada
        if evento == self.INICIAR_TAREA and self.estado == OrdenDeTrabajo.ACTIVA:
            self.estado = OrdenDeTrabajo.INICIADA
        # Si la evento fue FINALIZAR_TAREA_EXITOSA y esta Tarea fue la ultima, paso el estado a REALIZADA 
        elif evento == self.FINALIZAR_TAREA_EXITOSA and self.estado == OrdenDeTrabajo.INICIADA and self.detalles_por_finalizar() == 0:
            self.estado = OrdenDeTrabajo.REALIZADA
        # Si la evento fue FINALIZAR_TAREA_NO_EXITOSA y el estado de la Orden es INICIADA, paso el estado a PAUSADA  
        elif evento == self.FINALIZAR_TAREA_NO_EXITOSA and self.estado == OrdenDeTrabajo.INICIADA:
            self.estado = OrdenDeTrabajo.PAUSADA
        # Si la evento fue PAUSAR_ORDEN, paso el estado PAUSADA (cuando se presiona el boton "Pausar Orden")
        elif evento == self.PAUSAR_ORDEN:
            self.estado = OrdenDeTrabajo.PAUSADA
        # Si la evento fue REANUDAR_ORDEN:
        # En el caso de haber Tareas terminadas la orden pasa a estado REALIZADA
        # En el caso que haya tareas no iniciadas la orden pasa a ACTIVA
        # Si no es niguno de los anteriores pasa a INICIADA (cuando se presiona el boton "Reanudar Orden")
        elif evento == self.REANUDAR_ORDEN:
            if self.detalles_por_finalizar() == 0:
                self.estado = OrdenDeTrabajo.REALIZADA
            elif self.no_hay_tareas_iniciadas():
                self.estado = OrdenDeTrabajo.ACTIVA
            else:
                self.estado = OrdenDeTrabajo.INICIADA
        # Si la evento fue FINALIZAR_ORDEN, paso el estado a FINALIZADA (cuando se terminaron todas las tareas, se facturo, se pago y se entrego el vehiculo) 
        elif evento == self.FINALIZAR_ORDEN:
            self.estado = OrdenDeTrabajo.FINALIZADA
        # Si la evento fue FACTURAR_ORDEN, paso el estado a FACTURADA que quiere decir que se creo una factura asociada a la orden 
        elif evento == self.FACTURAR_ORDEN:
            self.estado = OrdenDeTrabajo.FACTURADA
        # Si la evento fue CANCELAR_ORDEN, paso el estado a CANCELADA 
        elif evento == self.CANCELAR_ORDEN:
            self.estado = OrdenDeTrabajo.CANCELADA
        # Guardo cambio de estado 
        self.save()

    def puede_facturarse(self):
        return self.estado == OrdenDeTrabajo.REALIZADA

    def puede_pausarse(self):
        return (self.estado == OrdenDeTrabajo.ACTIVA) or (self.estado == OrdenDeTrabajo.INICIADA)

    # Retorna verdadero si está esperando que su último presupuesto sea confirmado (ampliación)
    def esperando_confirmacion(self):
        ultimo_presupuesto = self.get_ultimo_presupuesto()
        return not ultimo_presupuesto.confirmado  

    def puede_reanudarse(self):
        esta_pausada = self.estado == OrdenDeTrabajo.PAUSADA
        return esta_pausada and not self.esperando_confirmacion()
    
    def puede_ampliarse(self):
        esta_pausada = self.estado == OrdenDeTrabajo.PAUSADA
        return esta_pausada and not self.esperando_confirmacion()

    def puede_ingresar_vehiculo(self):
        return (self.estado == OrdenDeTrabajo.CREADA)

    def puede_retirar_vehiculo(self):
        return  ((self.estado == OrdenDeTrabajo.FACTURADA) and (self.cliente.vip())) or (self.estado == OrdenDeTrabajo.PAGADA)

    def tareas_para_empleado(self, empleado):
        return [d for d in self.detalles.all() if empleado.puede_hacer(d.tarea.tipo)]


    # Esta funcion no esta siendo utilizada
    # def iniciar_tarea(self, empleado, tarea, fecha=now()):
    #         if self.estado == OrdenDeTrabajo.ACTIVA:
    #         tarea.iniciar(empleado, fecha)
    #         self.estado = OrdenDeTrabajo.INICIADA
    #         self.save()
    
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

    def actualizar_material(self, material, cantidad):
        materiales = self.orden_materiales.filter(material=material)
        if materiales.exists():
            material = materiales.first()
            material.actualizar(cantidad)
        elif cantidad > 0:
            material = Material.objects.get(pk=material.pk)
            MaterialOrdenDeTrabajo.objects.create(
                material=material, orden=self, cantidad_presupuestada=0 ,cantidad_utilizada=cantidad)

    def actualizar_repuesto(self, repuesto, cantidad):
        repuestos = self.orden_repuestos.filter(repuesto=repuesto)
        if repuestos.exists():
            repuesto = repuestos.first()
            repuesto.actualizar(cantidad)
        elif cantidad > 0:
            repuesto = Repuesto.objects.get(pk=repuesto.pk)
            RepuestoOrdenDeTrabajo.objects.create(
                repuesto=repuesto, orden=self, cantidad_presupuestada=0, cantidad_utilizada=cantidad)

    def get_ultimo_presupuesto(self):
        return self.presupuestos.all().order_by('fecha').last()

    def get_estado(self):
        return self.get_estado_display()

    def tiene_factura(self):
        return self.factura.exists()
    
    def get_factura(self):
        return self.factura.get(orden=self)

    def pagado(self):
        return self.estado == OrdenDeTrabajo.PAGADA
    
    def vehiculo_ingreso(self):
        return self.ingreso is not None

    def vehiculo_egreso(self):
        return self.egreso is not None

    #Solo cambia el estado cuando se paga el total de la factura
    def pagar_orden(self): 
        self.estado = OrdenDeTrabajo.PAGADA
        self.save()

    def aplicar_ampliacion(self, presupuesto):
        tareas_presupuesto = presupuesto.tareas.all()
        detalles_orden = self.detalles.all()

        # Elimino las tareas no exitosas
        for d in detalles_orden:
            if not d.exitosa:
                d.delete()

        # De las tareas del presupuesto, agrego las que no existen
        for t in tareas_presupuesto:
            if t.pk not in detalles_orden.values_list('tarea', flat=True):
                self.agregar_tarea(t)

        # De las tareas de la orden, quito las que no están en el nuevo presupuesto
        for t in detalles_orden:
            if t.tarea not in tareas_presupuesto and not t.esta_finalizado():
                t.delete()
    
        # De los materiales del presupuesto, solo agrego a la orden los que son nuevos
        materiales_orden = list(self.orden_materiales.all().values_list('material__pk', flat=True))
        for m in presupuesto.presupuesto_materiales.all():
            if m.material.pk not in materiales_orden:
                self.agregar_material(m.material, m.get_cantidad())

        # De los repuestos del presupuesto, solo agrego a la orden los que son nuevos
        repuestos_orden = list(self.orden_repuestos.all().values_list('repuesto__pk', flat=True))
        for r in presupuesto.presupuesto_repuestos.all():
            if r.repuesto.pk not in repuestos_orden:
                self.agregar_repuesto(r.repuesto, r.get_cantidad())
 
        # Elimino los materiales que están en la orden pero no en el presupuesto
        materiales_presupuesto = list(presupuesto.presupuesto_materiales.all().values_list('material__pk', flat=True))
        for om in self.orden_materiales.all():
            if om.material.pk not in materiales_presupuesto:
                om.delete()

        # Elimino los repuestos que están en la orden pero no en el presupuesto
        repuestos_presupuesto = list(presupuesto.presupuesto_repuestos.all().values_list('repuesto__pk', flat=True))
        for rm in self.orden_repuestos.all():
            if rm.repuesto.pk not in repuestos_presupuesto:
                rm.delete() 
        presupuesto.confirmado = True
        presupuesto.save()
        self.save()

    def get_tareas_finalizadas(self):
        tareas_finalizadas = []
        detalles = self.detalles.all()

        for d in detalles:
            if d.fin is not None and d.exitosa:
                tareas_finalizadas.append(d.tarea.pk)
        
        return tareas_finalizadas

    def __str__(self):
        if self.cliente and self.vehiculo:
            return f"{self.pk} | {self.cliente.nombre} - {self.vehiculo.modelo.marca} {self.vehiculo.modelo.nombre} ({self.vehiculo.patente})"
        else:
            return f"{self.pk} | (inconsistencia en cliente/vehiculo)" # Agregado ya que al haber inconsistencias se rompía en /admin

    def reporte_id(self):
        return f"Orden Nº:{self.pk} | {self.cliente.nombre } {self.cliente.apellido}"

    def get_planillas_pintura(self):
        planillas = PlanillaDePintura.objects.filter(orden__orden=self.pk)
        return planillas

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
        
        qs = self.filter(no_tiene_empleado & ha_ingresado).order_by('orden__turno')
        return qs

    def asignados(self, user):
        tiene_empleado = models.Q(empleado__isnull=False)
        no_esta_iniciado = models.Q(inicio__isnull=True)
        es_del_usuario = models.Q(empleado__usuario=user)

        permisos = user.get_user_permissions()

        if 'ordenes.can_ver_asignados' in permisos:
            qs = self.filter(tiene_empleado & no_esta_iniciado).order_by(
            'orden__turno')
        else:
            qs = self.filter(tiene_empleado & no_esta_iniciado & es_del_usuario).order_by(
            'orden__turno')

        return qs

    def sin_finalizar(self, user):
        tiene_empleado = models.Q(empleado__isnull=False)
        esta_iniciado = models.Q(inicio__isnull=False)
        no_esta_finalizado = models.Q(fin__isnull=True)
        es_del_usuario = models.Q(empleado__usuario=user)

        permisos = user.get_user_permissions()

        if 'ordenes.can_ver_sin_finalizar' in permisos:
            qs = self.filter(tiene_empleado & no_esta_finalizado &
                            esta_iniciado).order_by('orden__turno')
        else:
            qs = self.filter(tiene_empleado & no_esta_finalizado &
                            esta_iniciado & es_del_usuario).order_by('orden__turno')

        return qs

    def finalizados(self, user):
        esta_finalizado = models.Q(fin__isnull=False)
        es_del_usuario = models.Q(empleado__usuario=user)

        permisos = user.get_user_permissions()

        if 'ordenes.can_ver_finalizados' in permisos:
            qs = self.filter(esta_finalizado).order_by('-fin')
        else:
            qs = self.filter(esta_finalizado & es_del_usuario).order_by('-fin')

        return qs

    def todos(self, user):
        no_ha_ingresado = models.Q(orden__ingreso__isnull=True)
        es_del_usuario = models.Q(empleado__usuario=user)

        permisos = user.get_user_permissions()

        if 'ordenes.can_ver_todos' in permisos:
            qs = self.all().exclude(no_ha_ingresado).order_by('-fin')
        else:
            qs = self.all().filter(es_del_usuario).exclude(no_ha_ingresado).order_by('-fin')
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

    class Meta:
        permissions = [
            ('can_asignar_trabajo', 'Puede asignar trabajo a empleados'),
            ('can_ver_asignados', 'Puede ver listado de trabajos asignados'),
            ('can_ver_sin_finalizar', 'Puede ver listado de trabajos sin finalizar'),
            ('can_ver_finalizados', 'Puede ver listado de trabajos finalizados'),
            ('can_ver_todos', 'Puede ver todos de trabajos')
        ]

    def precio(self):
        return self.tarea.precio

    def iniciar(self, empleado, fecha=None):
        self.empleado = empleado
        self.inicio = fecha or now() #Comprueba si fecha es 'None' entonces devuelve la hora actual.
        self.save()
        self.orden.actualizar_estado(OrdenDeTrabajo.INICIAR_TAREA)

    def asignar(self, empleado):
        self.empleado = empleado
        self.save()

    def finalizar(self, exitosa, observaciones, fecha=None):
        self.exitosa = exitosa
        self.observaciones = observaciones
        self.fin = fecha or now() #Comprueba si fecha es 'None' entonces devuelve la hora actual.
        self.save()
        self.orden.actualizar_estado(exitosa and OrdenDeTrabajo.FINALIZAR_TAREA_EXITOSA or OrdenDeTrabajo.FINALIZAR_TAREA_NO_EXITOSA)

    # Usado para el modal de asignar empleados a trabajo
    def get_empleados_aptos(self):
        tipo = self.tarea.tipo.pk

        empleados = [str(e['pk']) for e in Empleado.objects.filter(tareas=tipo).values('pk')]
        string = ','.join(empleados)

        return string

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

    def get_string_estado(self):

        if not self.inicio:
            return 'sin iniciar'
        if self.fin and self.exitosa:
            return 'finalizada'
        if not self.exitosa:
            return 'fallida'
        
        return 'iniciada'

    def puedo_agregar_insumos(self):
        return (self.tarea.tipo.materiales or self.tarea.tipo.repuestos) and self.fin is None



class MaterialOrdenDeTrabajo(models.Model):
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name='ordenes_de_trabajo')
    orden = models.ForeignKey(
        OrdenDeTrabajo, on_delete=models.CASCADE, related_name='orden_materiales')
    cantidad_presupuestada = models.PositiveBigIntegerField()
    cantidad_utilizada = models.PositiveBigIntegerField(default=0)

    def precio(self):
        return self.material.precio * self.cantidad_utilizada

    def actualizar(self, cantidad):
        self.cantidad_utilizada += cantidad
        if self.cantidad_utilizada >= 0:
            self.save()


    def decrementar_materiales(self, material):
        if self.cantidad_utilizada > 0 or self.cantidad_presupuestada > 0: 
            m = Material.objects.get(pk=material.material.pk)
            m.decrementar_stock(self.cantidad_utilizada)

class RepuestoOrdenDeTrabajo(models.Model):
    repuesto = models.ForeignKey(
        Repuesto, on_delete=models.CASCADE, related_name='ordenes_de_trabajo')
    orden = models.ForeignKey(
        OrdenDeTrabajo, on_delete=models.CASCADE, related_name='orden_repuestos')
    cantidad_presupuestada = models.PositiveBigIntegerField()
    cantidad_utilizada = models.PositiveBigIntegerField(default=0)

    def precio(self):
        return self.repuesto.precio * self.cantidad_utilizada

    def actualizar(self, cantidad):
        self.cantidad_utilizada += cantidad
        if self.cantidad_utilizada >= 0:
            self.save()
    
    def decrementar_repuesto(self, repuesto):
        if self.cantidad_utilizada > 0 or self.cantidad_presupuestada > 0: 
            r = Repuesto.objects.get(pk=repuesto.repuesto.pk)
            r.decrementar_stock(self.cantidad_utilizada)

class Presupuesto(models.Model):
    cliente = models.ForeignKey(
        Cliente, related_name='presupuestos', on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(
        Vehiculo, related_name='presupuestos', on_delete=models.RESTRICT)
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
    confirmado = models.BooleanField(default=False)

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
        self.orden = OrdenDeTrabajo.objects.create(turno=turno)

        for t in self.tareas.all():
            self.orden.agregar_tarea(t)
        for m in self.presupuesto_materiales.all():
            self.orden.agregar_material(m.material, m.get_cantidad())
        for r in self.presupuesto_repuestos.all():
            self.orden.agregar_repuesto(r.repuesto, r.get_cantidad())
        
        self.confirmado = True

        self.save()
        return self.orden

    def get_confirmado(self):
        return self.confirmado

    def get_ampliado(self):
        return self.ampliado

    def cantidad_detalles(self):
        return self.tareas.count() + self.materiales.count() + self.repuestos.count()

    def puede_eliminarse(self):
        return not self.confirmado 
        
    def puede_confirmarse(self):
        return not self.confirmado and not self.esta_expirado()

    def puede_modificarse(self):
        return self.orden is None and not self.esta_expirado()

    def tiene_orden(self):
        return self.orden is not None   

    def puede_cancelarse(self):
        return not self.confirmado and not self.esta_expirado()

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

    def get_fecha_vencimiento(self):
        return (self.fecha + timedelta(days=self.validez)).date()

    def esta_expirado(self):
        return self.get_fecha_vencimiento() < timezone.now().date() and not self.confirmado


def cantidad_positiva(v):
    if v <= 0:
        raise ValidationError('La cantidad de un insumo debe ser mayor a 0')

class PresupuestoMaterial(models.Model):
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name='presupuestos', null=True, blank=True)
    presupuesto = models.ForeignKey(
        Presupuesto, on_delete=models.CASCADE, related_name='presupuesto_materiales')
    cantidad = models.PositiveBigIntegerField(validators=[], null=True, blank=True, default=1)

    def __str__(self) -> str:
        return f'{self.material.nombre} (cantidad: {self.cantidad})'

    def precio(self):
        return self.material.precio * self.cantidad
    
    def get_cantidad(self):
        return self.cantidad

class PresupuestoRepuesto(models.Model):
    repuesto = models.ForeignKey(
        Repuesto, on_delete=models.CASCADE, related_name='presupuestos', null=True, blank=True)
    presupuesto = models.ForeignKey(
        Presupuesto, on_delete=models.CASCADE, related_name='presupuesto_repuestos')
    cantidad = models.PositiveBigIntegerField(validators=[], null=True, blank=True, default=1)   # cantidad debe ser positiva

    def precio(self):
        return self.repuesto.precio * self.cantidad

    def get_cantidad(self):
        return self.cantidad


class PlanillaDePintura(models.Model):
    orden = models.ForeignKey(
        DetalleOrdenDeTrabajo, on_delete=models.CASCADE, related_name='planillas')
    fecha = models.DateTimeField(auto_now_add=True)
    nombre_de_color = models.CharField(max_length=100)

    def vaciar(self):
        DetallePlanillaDePintura.objects.filter(planilla=self).delete()

    def agregar(self, formula, cantidad):
        return DetallePlanillaDePintura.objects.create(planilla=self, formula=formula, cantidad=cantidad)

    def eliminar(self):
        self.delete()

    def puedo_eliminar_planilla(self):
        detalle = self.orden
        return detalle.fin is None

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
