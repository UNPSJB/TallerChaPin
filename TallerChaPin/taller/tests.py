from django.test import TestCase
from taller.models import *
from ordenes.models import *
# Create your tests here.


# class MarcaTestCase(TestCase):
#     def setUp(self):
#         Marca.objects.create(nombre='Ford')

#     def test_marca_para_filtro_texto(self):
#         modelos = Marca.objects.filtrar(
#             "nombre__startswith=F")
#         self.assertEqual(len(modelos), 1)
#         # try:
#         #    raise ValueError()
#         # except (ValueError, TypeError) as e:
#         #    self.assertRaises(ValueError, e)


# class ModeloTestCase(TestCase):
#     def setUp(self):
#         Modelo.objects.create(
#             nombre='Focus', anio=2030, marca=Marca.objects.create(nombre='Ford'))

#     def test_modelos_para_filtro_texto(self):
#         modelos = Modelo.objects.filtrar(
#             "nombre__icontains=o&marca__id__exact=1")
#         self.assertEqual(len(modelos), 1)
#         self.assertEqual(modelos[0].nombre, "Focus")

#     def test_obtener_los_modelos_de_una_marca(self):
#         # Paso 1 aislamos el test
#         modelos = Modelo.objects.filter(marca__nombre='Ford')
#         # Paso 2 hactamos el test
#         # Paso 3 verificamos que el test se ejecute correctamente
#         self.assertEqual(len(modelos), 1)


# class EmpleadoTestCase(TestCase):
#     def setUp(self):
#         Empleado.objects.create(nombre="Pepe", apellido="Perez", legajo=1)

#     def test_crear_usuario(self):
#         empleado = Empleado.objects.get(nombre="Pepe")
#         self.assertIsNone(empleado.usuario)
#         empleado.crear_usuario()
#         self.assertIsNotNone(empleado.usuario)
#         self.assertEqual(empleado.usuario.username, "pperez")


# class MaterialTestCase(TestCase):
#     fixtures = [
#         'taller/fixtures/tests.json'
#     ]

#     def test_marcas(self):
#         marcas = Marca.objects.all()
#         self.assertEqual(len(marcas), 7)

#     def test_decrementar_stock(self):
#         material = Material.objects.filter(cantidad=3000).first()
#         material.menos_stock(10)
#         self.assertEqual(material.stock(), 2990)

#     def test_calcular_precio(self):
#         material = Material.objects.filter(precio=10).first()
#         self.assertEqual(material.calcular_precio(2), 20)


class ClienteTestCase(TestCase):
    fixtures = [
        'taller/fixtures/all.json'
    ]
    
    
    # Clientes que tienen al menos 3 facturas pagadas (vip)
    def test_es_vip(self):
        clientes = [] 
        clientes.extend(Cliente.objects.all())
        for i in clientes: 
            print(i.vip())

