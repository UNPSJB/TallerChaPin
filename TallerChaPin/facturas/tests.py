from django.test import TestCase

from ordenes.models import OrdenDeTrabajo
from .models import Factura
from decimal import Decimal

# Create your tests here.


class FacturaTestCase(TestCase):
    fixtures = [
        'taller/fixtures/all.json',
    ]

    def setUp(self) -> None:
        self.orden = OrdenDeTrabajo.objects.get(pk=1)

    def test_todobien(self):
        self.factura = Factura.facturar_orden(self.orden)
        self.assertEqual(self.factura.total(), Decimal("780.00"))

    def test_pagos(self):
        self.test_todobien()
        self.factura.pagar(Decimal("500.00"))
        self.assertEqual(self.factura.saldo(), Decimal("280.00"))
