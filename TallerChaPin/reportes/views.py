from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
# from .models import *
# from .forms import *
from datetime import date
from django.contrib import messages
from TallerChaPin.utils import ListFilterView, export_list
from taller.models import (
    Empleado,
    Cliente,
    Vehiculo,
    Tarea,
    Material,
    Repuesto,
    Marca
)

def ReporteMarcaVehiculos(request):
    #Agregar permisos. Esto lo ve el administrativo
    context={}
    context['titulo'] = "Reporte 1"
    return render (request, 'reportes/reporte_marcas_vehiculos_recurrentes.html',context)

def reporte_marcas_vehiculos_recurrentes(request):
    #Agregar permisos. Esto lo ve dios unicamente
    marcas = list(Marca.objects.all().values('pk','nombre'))
    r = []
    for marca in marcas:
        cantidad = Vehiculo.objects.filter(modelo__marca = marca['pk']).count()
        r.append({'cantidad': cantidad , 'nombre':marca['nombre']})
    r.sort(key=lambda c : c['cantidad'], reverse=True)

    return JsonResponse({'vehiculos' : r })