from django.urls import path
from .views import *


urlpatterns = [
    #-------------------Reporte de vehiculos recurrentes-------------------#
    path('reporte_vehiculos', reporteMarcaVehiculos, name="reporte_marcas_vehiculos"),
    path('get_marcas_vehiculos', getMarcasVehiculos),
    #-------------------Reporte de recaudacion-------------------#
    path('reporte_facturacion', reporteFacturacion, name='reporte_facturacion'),
    path('get_facturacion/<str:params>', getFacturacion),
    #-------------------Reporte de productividad-------------------#
    path('reporte_productividad', reporteHorasTrabajo, name='reporte_productividad'),
    path('get_horas_trabajo/<str:tipo>', getHorasTrabajo),
    #-------------------Reporte de ordenes-------------------#
    path('reporte_ordenes', reporteOrdenes, name='reporte_ordenes'),
    path('get_ordenes/<str:params>', getOrdenes),
]
