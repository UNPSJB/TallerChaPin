from django.urls import path
from .views import *


urlpatterns = [
    path('reporte_prueba', ReportePrueba, name="reporte_prueba"),
    path('reporte_json', traerJson, name="json"),
]
