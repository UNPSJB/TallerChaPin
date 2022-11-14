from django.urls import path
from .views import *


urlpatterns = [
    path('reporte_prueba', ReporteMarcaVehiculos, name="reporteMarcasVehiculos"),
    path('reporte_marcas_vehiculos', reporte_marcas_vehiculos_recurrentes, name="reporte_marcas_vehiculos"),
    path('reporte_facturacion', ReporteFacturacion, name='reporte_facturacion'),
    path('get_facturacion/<str:params>', getFacturacion),
]
