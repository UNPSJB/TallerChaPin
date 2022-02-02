from django.utils.timezone import now
from django.test import TestCase
from taller.models import Cliente, Empleado, Tarea, Marca, Material, Modelo, Repuesto, TipoMaterial
from ordenes.models import OrdenDeTrabajo, Presupuesto

class OrdenTestCase(TestCase):
    def setUp(self):
        Cliente.objects.create(
            dni='12312312',
            nombre='Pepito',
            apellido='Testing',
            direccion = 'Calle 123',
            telefono='2804123456'
        )

        TipoMaterial.objects.create(
            nombre='tmat1',
            unidad_medida=1
        )
        Material.objects.create(
            nombre='mat1',
            tipo=TipoMaterial.objects.get(nombre='tmat1'),
            cantidad=10,
            precio=100
        )
        Marca.objects.create(
            nombre='mar1',
            descripcion='dmar1'
            # objects=?
        )
        Modelo.objects.create(
            nombre='mod1',
            descripcion='dmod1',
            marca=Marca.objects.get(nombre='mar1'),
            anio=2019
        )
        Repuesto.objects.create(
            nombre='rep1',
            modelo=Modelo.objects.get(nombre='mod1'),
            tipo=1,
            cantidad=20,
            precio=200
        )

        OrdenDeTrabajo.objects.create(
            # materiales=Material.objects.get(nombre='mat1'),
            # repuestos=Repuesto.objects.get(nombre='rep1'),
            turno=now(),
            ingreso=None,
            egreso=None,
            estado=0,
        )

    # Probando si los test funcionan: este método funciona
    def test_cliente_prueba(self):
        cliente1 = Cliente.objects.get(dni='12312312')
        self.assertEqual(cliente1.nombre, 'Pepito')

    def test_orden_actualizar_estado(self):
        orden1 = OrdenDeTrabajo.objects.get(estado=0)
        print(orden1)
        self.assertEqual(1,1)