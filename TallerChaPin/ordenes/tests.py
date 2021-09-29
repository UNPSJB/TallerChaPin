from django.test import TestCase
from taller.models import Cliente, Tarea, Material, Repuesto
from ordenes.models import Presupuesto

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
        tarea = Tarea.objects.get(pk=3)
        self.presupuesto.agregar_tarea(tarea)
        material = Material.objects.get(pk=1)
        self.presupuesto.agregar_material(material, 3)
        repuesto = Repuesto.objects.get(pk=1)
        self.presupuesto.agregar_repuesto(repuesto)
        self.assertEqual(self.presupuesto.precio_estimado(), 550)

    def test_confirmar_presupuesto(self):
        self.test_crear_presupuesto()
        self.presupuesto.confirmar()
        self.assertIsNotNone(self.presupuesto.orden)
        self.assertEqual(self.presupuesto.orden.detalles.count(), 1)
        self.assertEqual(self.presupuesto.orden.materiales.count(), 1)
        self.assertEqual(self.presupuesto.orden.repuestos.count(), 1)
