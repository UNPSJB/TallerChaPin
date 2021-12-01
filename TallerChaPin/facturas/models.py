from django.utils.timezone import now
from datetime import datetime, time
from django.db import models
from ordenes.models import DetalleOrdenDeTrabajo, OrdenDeTrabajo
from taller.models import (
    Empleado,
    Cliente,
    Vehiculo,
    Tarea,
    Material,
    Repuesto
)

# Aqui definimos los modelos:

#-------------------------- FACTURA -------------------------------#

class Factura(models.Model):
    orden = models.ForeignKey(OrdenDeTrabajo, on_delete=models.CASCADE)
    fecha = models.DateField()

    def total(self):
        return self.detalles.aggregate(total=models.Sum('precio'))['total']

    @staticmethod
    def facturar_orden(orden):
        factura = Factura.objects.create(orden=orden, fecha=now())
        for des, precio in [(f"{m}", m.precio()) for m in orden.orden_materiales.all()]:
            factura.agregar_detalle(des, precio)
        for desc, precio in [(f"{r}", r.precio()) for r in orden.orden_repuestos.all()]:
            factura.agregar_detalle(desc, precio)
        for desc, precio in [(f"{t}", t.precio()) for t in orden.detalles.all()]:
            factura.agregar_detalle(desc, precio)
        orden.estado = OrdenDeTrabajo.FACTURADA
        orden.save()
        return factura

    def puede_pagar(self):
        return self.no_pagada() and self.adeuda()

    def no_pagada(self):
        return self.orden.estado !=  OrdenDeTrabajo.FINALIZADA
    
    def adeuda(self):
        return self.saldo() > 0

    def agregar_detalle(self, descripcion, precio):
        return DetalleFactura.objects.create(factura=self, descripcion=descripcion, precio=precio)

    def pagar(self, monto, tipo):
        return Pago.objects.create(factura=self, monto=monto, tipo=tipo)

    def saldo(self):
        if len(self.pagos.all()) > 0:
            return self.total() - self.pagos.all().aggregate(total=models.Sum('monto'))['total']
        else:
            return self.total()
 

#-------------------------- DETALLE FACTURA -------------------------------#

class DetalleFactura(models.Model):
    factura = models.ForeignKey(
        Factura, related_name="detalles", on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)


#-------------------------------- PAGO -----------------------------------#

class Pago(models.Model):
    
    CONTADO = 0
    TARJETA_DEBITO = 1
    TARJETA_CREDITO = 2
    TIPO_CHOICES = [
        (CONTADO, 'Contado'),
        (TARJETA_DEBITO, 'Tarjeta Debito'),
        (TARJETA_CREDITO, 'Tarjeta Credito'),
    ]
    factura = models.ForeignKey(
        Factura, on_delete=models.CASCADE, related_name="pagos")
    fecha = models.DateField(auto_now=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.PositiveSmallIntegerField(
        choices=TIPO_CHOICES, default=CONTADO)

    @property
    def vehiculo(self):
        return self.factura.orden.vehiculo

    @property
    def cliente(self):
        return self.factura.orden.cliente
