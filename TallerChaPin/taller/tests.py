from django.test import TestCase
from .models import Modelo, Marca, Empleado

# Create your tests here.


class MarcaTestCase(TestCase):
    def setUp(self):
        Marca.objects.create(nombre='Ford')

    def test_marca_para_filtro_texto(self):
        modelos = Marca.objects.filtrar(
            "nombre__startswith=F")
        self.assertEqual(len(modelos), 1)
        #try:
        #    raise ValueError()
        #except (ValueError, TypeError) as e:
        #    self.assertRaises(ValueError, e)


class ModeloTestCase(TestCase):
    def setUp(self):
        Modelo.objects.create(
            nombre='Focus', marca=Marca.objects.create(nombre='Ford'))

    def test_modelos_para_filtro_texto(self):
        modelos = Modelo.objects.filtrar(
            "nombre__icontains=o&marca__id__exact=1")
        self.assertEqual(len(modelos), 1)
        self.assertEqual(modelos[0].nombre, "Focus")

    def test_obtener_los_modelos_de_una_marca(self):
        # Paso 1 aislamos el test
        modelos = Modelo.objects.filter(marca__nombre='Ford')
        # Paso 2 hactamos el test
        # Paso 3 verificamos que el test se ejecute correctamente
        self.assertEqual(len(modelos), 1)


class EmpleadoTestCase(TestCase):
    def setUp(self):
        Empleado.objects.create(nombre="Pepe", apellido="Perez", legajo=1)

    def test_crear_usuario(self):
        empleado = Empleado.objects.get(nombre="Pepe")
        self.assertIsNone(empleado.usuario)
        empleado.crear_usuario()
        self.assertIsNotNone(empleado.usuario)
        self.assertEqual(empleado.usuario.username, "pperez")
