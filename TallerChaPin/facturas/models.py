from traceback import print_tb
from xml.dom import ValidationErr
from django.forms import ValidationError
from django.utils.timezone import now
from datetime import datetime, time
from django.db import models
from ordenes.models import DetalleOrdenDeTrabajo, OrdenDeTrabajo


# Aqui definimos los modelos:

#-------------------------- FACTURA -------------------------------#

class Factura(models.Model):
    CREADA = 0
    ACTIVA = 1
    CANCELADA = 2
    PAGADA = 3
    VENCIDA = 4
    ESTADO_CHOICES = [
        (CREADA, 'Creada'),
        (ACTIVA, 'Activa'),
        (CANCELADA, 'Cancelada'),
        (PAGADA, 'Pagada'),
        (VENCIDA, 'Vencida'),        
    ]

    orden = models.ForeignKey(OrdenDeTrabajo, related_name='factura', on_delete=models.CASCADE)
    fecha = models.DateField()
    estado =  models.PositiveBigIntegerField(
        choices=ESTADO_CHOICES, default=CREADA)
    cuotas = models.PositiveSmallIntegerField(default=1, blank=False, null=False)

    # @property
    # def vehiculo(self):
    #     return self.orden.vehiculo

    # @property
    # def cliente(self):
    #     return self.orden.cliente

    @staticmethod
    def facturar_orden(orden):
        factura = Factura.objects.create(orden=orden, fecha=now())
        for des, precio in [(f"{m}", m.precio()) for m in orden.orden_materiales.all()]:
            factura.agregar_detalle(des, precio)
        for desc, precio in [(f"{r}", r.precio()) for r in orden.orden_repuestos.all()]:
            factura.agregar_detalle(desc, precio)
        for desc, precio in [(f"{t}", t.precio()) for t in orden.detalles.all()]:
            factura.agregar_detalle(desc, precio)
        orden.actualizar_estado(OrdenDeTrabajo.FACTURAR_ORDEN)
        orden.save()
        
        return factura

    def total(self):
        return self.detalles.aggregate(total=models.Sum('precio'))['total']

    def pagado(self):
        return self.estado == Factura.PAGADA

    def puede_pagar(self):
        return self.adeuda()

    def get_cliente_orden(self):
        return self.orden.cliente

    def get_vehiculo_orden(self):
        return self.orden.vehiculo

    def get_cuotas(self):
        return self.cuotas

    def get_estado(self):
        return self.get_estado_display()

    def no_pagada(self):
        return self.orden.estado !=  OrdenDeTrabajo.FINALIZADA
    
    def adeuda(self):
        return self.saldo() > 0

    def agregar_detalle(self, descripcion, precio):
        return DetalleFactura.objects.create(factura=self, descripcion=descripcion, precio=precio)

    def pagar(self, monto, tipo, num_cuotas):

        if monto <= 0:
            raise ValidationError('El monto a pagar debe ser mayor.')

        if monto > self.saldo():
            raise ValidationError('El pago ingresado es mayor al saldo restante.')

        if tipo == Pago.TARJETA_CREDITO and monto != self.saldo():
            raise ValidationError('El pago con tarjeta de crédito solo está disponible para pagos totales.')

        pago = Pago.objects.create(factura=self, monto=monto, tipo=tipo)
        self.estado = Factura.ACTIVA

        if tipo == Pago.TARJETA_CREDITO:
            self.cuotas = num_cuotas
        else:
            self.cuotas = 1

        if self.saldo() <= 0:
            self.estado = Factura.PAGADA
            self.orden.pagar_orden()

        self.save()
        
        return pago

    def saldo(self):
        saldo = self.total() - (self.pagos.aggregate(total=models.Sum('monto'))['total'] or 0) 
        return saldo
 

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
    TIPO_PAGO = [
        (CONTADO, 'Contado'),
        (TARJETA_DEBITO, 'Tarjeta Debito'),
        (TARJETA_CREDITO, 'Tarjeta Credito'),
    ]
    factura = models.ForeignKey(
        Factura, on_delete=models.CASCADE, related_name="pagos")
    fecha = models.DateField(auto_now=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.PositiveSmallIntegerField(
        choices=TIPO_PAGO, default=CONTADO)

    def __str__(self):
        return f'Nro. de Factura: ({self.factura.pk})'

    def puede_eliminarse(self):
        return self.factura.estado == Factura.ACTIVA or self.factura.estado == Factura.CREADA

    @property
    def cliente(self):
        return self.factura.orden.cliente

    def get_cuotas(self):
        return self.factura.get_cuotas()

    def get_nombre_factura(self):
        return f'Nro. de Factura: ({self.factura.pk})'
    
    def get_tipo(self):
        return self.get_tipo_display()
        
    def puede_pagar(self):
        return self.factura.puede_pagar()
