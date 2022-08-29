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

    def total(self):
        return self.detalles.aggregate(total=models.Sum('precio'))['total']

    def pagado(self):
        return self.estado == Factura.PAGADA

    def puede_pagar(self):
        return self.no_pagada() and self.adeuda()

    def no_pagada(self):
        return self.orden.estado !=  OrdenDeTrabajo.FINALIZADA
    
    def adeuda(self):
        return self.saldo() > 0

    def agregar_detalle(self, descripcion, precio):
        return DetalleFactura.objects.create(factura=self, descripcion=descripcion, precio=precio)

    def pagar(self, monto, tipo, num_cuotas):
        if len(self.pagos.all()) == 0 and monto == self.total(): 
            self.estado = Factura.PAGADA # Si se pago la totalidad entonces la orden esta PAGADA
            self.orden.pagar_orden() # Cambia el estado de la orden a PAGADA
            if tipo == Pago.TARJETA_CREDITO:
                 self.cuotas = num_cuotas
            else:
                self.cuotas = 1
            self.save()
            
        if len(self.pagos.all()) != 0 and monto < self.total(): 
            self.estado = Factura.ACTIVA # Si no se pago toda la factura y aun hay saldo pendiente esta ACTIVA
            if monto == self.saldo(): # si el monto a pagar es igual al saldo restante significa que es lo ultimo que se adeuda
                self.estado = Factura.PAGADA # Si se pago la totalidad entonces la orden esta PAGADA
                self.orden.pagar_orden() # Cambia el estado de la orden a PAGADA
            self.save()
            self.cuotas = 1

        return Pago.objects.create(factura=self, monto=monto, tipo=tipo)
    #Nota: si se pueden simplificar mejor jaja
    def calcular_couta(monto, num_coutas): # Puede que sirva para algo
        if num_coutas == 3:
            return monto / 3
        if num_coutas == 6:
            return monto / 6
        if num_coutas == 12:
            return monto / 12
       
    # def cuotas_pagas(self):
    #     return len(self.pagos.all())

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

