from django.urls import path
from .views import *


urlpatterns = [
    # ----------------Factura-------------------------
    path('facturas/crear/<int:pk>', crearFactura, name="crearFactura"),
    path('facturas/listar', FacturaListView.as_view(), name="listarFacturas"),
    path('facturas/detalle/<int:pk>',
         FacturaDetailView.as_view(), name="detallesFactura"),
    path('facturas/exportar',
         exportar_listado_facturas, name='exportarFacturas'),
    # ----------------Pago-------------------------
    path('pagos/crear/<int:pk>', PagoCreateView.as_view(), name="crearPago"),
    path('pagos/detalle/<int:pk>', PagoDetailView.as_view(), name="detallesPago"),
    # Solo se puede modificar el modo de pago...
    path('pagos/modificar/<int:pk>',
         PagoUpdateView.as_view(), name="modificarPago"),
    path('pagos/listar', PagoListView.as_view(), name="listarPagos"),
    path('pagos/eliminar/<int:pk>', PagoDeleteView.as_view(), name="eliminarPago"),
    path('pagos/exportar',
         exportar_listado_pagos, name='exportarPagos'),
    # ----------------PDF-------------------------
    path('factura/pdf/<int:pk>', imprimirFactura.as_view(),
         name='imprimirFactura'),
    path('pago/pdf/<int:pk>', imprimirPago.as_view(),
         name='imprimirPago'),

]
