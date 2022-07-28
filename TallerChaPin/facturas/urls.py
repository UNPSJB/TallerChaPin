from django.urls import path
from .views import *


urlpatterns = [
    # ----------------Factura-------------------------
    path('facturas/crear/<int:pk>', crearFactura, name="crearFactura"),
    path('facturas/listar', FacturaListView.as_view(), name="listarFacturas"),
    path('facturas/detalle/<int:pk>',
         FacturaDetailView.as_view(), name="detallesFactura"),
    path('facturas/modificar/<int:pk>',
         FacturaUpdateView.as_view(), name="modificarFactura"),  # Solo se puede modificar el modo de pago... El pago creado se debe eliminar UNICAMENTE si no ha sido PAGADO
    path('facturas/eliminar/<int:pk>',
         FacturaDeleteView.as_view(), name="eliminarFactura"),
    # ----------------Pago-------------------------
    path('pagos/crear/<int:pk>', PagoCreateView.as_view(), name="crearPago"),
#     path('pagos/crear/<int:pk>/debito', PagoDebitoView.as_view(), name="pagoDebito"),
#     path('pagos/crear/<int:pk>/credito', PagoCreditoView.as_view(), name="pagoCredito"),
#     path('pagos/crear/<int:pk>/contado', PagoContadoView.as_view(), name="pagoContado"),
    path('pagos/detalle/<int:pk>', PagoDetailView.as_view(), name="detallesPago"),
    path('pagos/modificar/<int:pk>', PagoUpdateView.as_view(), name="modificarPago"),
    path('pagos/listar', PagoListView.as_view(), name="listarPagos"), 
    path('pagos/eliminar/<int:pk>', FacturaDeleteView.as_view(), name="eliminarPago"),
    # ----------------PDF-------------------------
    path('facturas/pdf/<int:pk>', imprimirFactura.as_view(),
         name='imprimirFactura')

]
