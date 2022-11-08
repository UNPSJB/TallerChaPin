from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
# from .models import *
# from .forms import *
from datetime import date, datetime, timedelta
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
from facturas.models import Factura, Pago

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


def ReporteFacturacion(request):
    context={}
    context['titulo'] = "Reporte de facturación"
    return render (request, 'reportes/reporte_facturacion.html', context)

def getFacturacion(request, params):
    params_f = params.split(',')
    periodicidad = params_f[0]
    fecha_desde = datetime.strptime(params_f[1], '%Y-%m-%d').date()
    fecha_hasta = datetime.strptime(params_f[2], '%Y-%m-%d').date()
    dias_diferencia = (fecha_hasta - fecha_desde).days + 1 # +1 para incluir la fecha_hasta
    
    labels = []
    facturado = []
    pagado = []

    if periodicidad == "1": # Día a día
        for i in range(dias_diferencia):
            fecha = (fecha_desde+timedelta(days=i))
            labels.append(fecha.strftime("%d-%m-%Y"))

            facturacion_diaria = 0
            facturas = Factura.objects.filter(fecha=fecha)
            for f in facturas:
                facturacion_diaria += f.total()
            if len(facturado) > 0:
                facturado.append(facturado[len(facturado)-1] + facturacion_diaria)
            else:
                facturado.append(facturacion_diaria)

            pagos_diarios = 0
            pagos = Pago.objects.filter(fecha=fecha)
            for p in pagos:
                pagos_diarios += p.monto
            if len(pagado) > 0:
                pagado.append(pagado[len(pagado)-1] + pagos_diarios)
            else:
                pagado.append(pagos_diarios)

    elif periodicidad == "2": # Semanalmente
        pass
    elif periodicidad == "3": # Mensualmente
        pass

    return JsonResponse({'labels' : labels, 'facturado': facturado, 'pagado': pagado })