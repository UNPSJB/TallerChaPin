from django.utils.timezone import now
from django.test import TestCase
from taller.models import Cliente, Empleado, Tarea, Material, Repuesto
from ordenes.models import OrdenDeTrabajo, Presupuesto

# Create your tests here.


class PresupuestoTestCase(TestCase):
    fixtures = [
        'taller/fixtures/tests.json'
    ]

    def setUp(self) -> None:
        self.cliente = Cliente.objects.get(pk=1)
        self.vehiculo = self.cliente.vehiculos.first()
        self.presupuesto = Presupuesto.objects.create(
            cliente=self.cliente, vehiculo=self.vehiculo, validez=10)

    def test_crear_presupuesto(self):
        pintar = Tarea.objects.get(pk=3)
        cambiar = Tarea.objects.get(pk=6)
        self.presupuesto.agregar_tarea(pintar)
        self.presupuesto.agregar_tarea(cambiar)
        material = Material.objects.get(pk=1)
        self.presupuesto.agregar_material(material, 3)
        repuesto = Repuesto.objects.get(pk=1)
        self.presupuesto.agregar_repuesto(repuesto)
        self.assertEqual(self.presupuesto.precio_estimado(), 630)

    def test_confirmar_presupuesto(self):
        self.test_crear_presupuesto()
        self.presupuesto.confirmar(now())
        self.assertIsNotNone(self.presupuesto.orden)
        self.assertEqual(self.presupuesto.orden.detalles.count(), 2)
        self.assertEqual(self.presupuesto.orden.materiales.count(), 1)
        self.assertEqual(self.presupuesto.orden.repuestos.count(), 1)

    def test_turno_orden(self):
        self.test_confirmar_presupuesto()
        orden = self.presupuesto.orden
        orden.cambiar_turno(now())

    def test_orden_ingresar_vehiculo(self):
        self.test_turno_orden()
        orden = self.presupuesto.orden
        orden.registrar_ingreso(now())

    def test_orden_iniciar_trabajo(self):
        self.test_orden_ingresar_vehiculo()
        orden = self.presupuesto.orden
        empleado = Empleado.objects.get(pk=2)
        tareas = orden.tareas_para_empleado(empleado)
        self.assertEqual(len(tareas), 1)
        orden.iniciar_tarea(empleado, tareas[0], now())

    def test_orden_finalizar_trabajo(self):
        self.test_orden_iniciar_trabajo()
        orden = self.presupuesto.orden
        empleado = Empleado.objects.get(pk=2)
        pintura = Material.objects.filter(tipo=1).first()
        tareas = orden.tareas_para_empleado(empleado)
        self.assertEqual(len(tareas), 1)
        detalle = tareas[0]
        detalle.crear_planilla_de_pintura(
            pintura, [("263gs", 100), ("27dgs6", 20), ("727ey", 5)])
        orden.finalizar_tarea(tareas[0], True, "Todo bien", materiales=[
                              (1, 1)], fecha=now())
        self.assertNotEqual(orden.estado, OrdenDeTrabajo.FINALIZADA)
