from django.urls import path
from .views import *


urlpatterns = [
    # ----------------Factura-------------------------
    path('facturas/crear/<int:pk>', crearFactura, name="crearFactura"),
    path('facturas/listar', FacturaListView.as_view(), name="listarFacturas"),
    path('facturas/detalle/<int:pk>',
         FacturaDetailView.as_view(), name="detallesFactura"),
    path('facturas/modificar/<int:pk>',
         FacturaUpdateView.as_view(), name="modificarFactura"),  # Solo se puede modificar el modo de pago
    path('facturas/eliminar/<int:pk>',
         FacturaDeleteView.as_view(), name="eliminarFactura"),
    # ----------------Pago-------------------------
    path('pagos/crear/<int:pk>', PagoCreateView.as_view(), name="crearPago"),
    path('pagos/modificar/<int:pk>',
         PagoUpdateView.as_view(), name="modificarPago"),
    path('pagos/listar', PagoListView.as_view(), name="listarPagos"),
    # ----------------PDF-------------------------
    path('facturas/pdf/<int:pk>', imprimirFactura.as_view(),
         name='imprimirFactura')
]
