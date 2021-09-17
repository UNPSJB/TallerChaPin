from django.db import models
from ordenes.models import DetalleOrdenDeTrabajo, OrdenDeTrabajo

# Create your models here.


class Factura(models.Model):
    orden = models.ForeignKey(OrdenDeTrabajo, on_delete=models.CASCADE)
    fecha = models.DateField()

    def total(self):
        return sum([d.precio for d in self.detalles.all()])


class DetalleFactura(models.Model):
    factura = models.ForeignKey(
        Factura, related_name="detalles", on_delete=models.CASCADE)
    detalle = models.ForeignKey(
        DetalleOrdenDeTrabajo, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)


class Pago(models.Model):
    CONTADO = 0
    TARJETA_DEBITO = 1
    TARJETA_CREDITO = 2
    TIPO_CHOICES = [
        (CONTADO, 'Contado'),
        (TARJETA_DEBITO, 'Tarjeta Debito'),
        (TARJETA_CREDITO, 'Tarjeta Credito'),
    ]
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    tipo = models.PositiveSmallIntegerField(
        choices=TIPO_CHOICES, default=CONTADO)
