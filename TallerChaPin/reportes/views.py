from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
# from .models import *
# from .forms import *
from datetime import date, datetime, timedelta
from django.contrib import messages
from TallerChaPin.utils import ListFilterView, export_list
from math import floor
from taller.models import (
    Empleado,
    Cliente,
    Vehiculo,
    Tarea,
    Material,
    Repuesto,
    Marca,
    TipoTarea
)
from ordenes.models import DetalleOrdenDeTrabajo, OrdenDeTrabajo
from facturas.models import Factura, Pago

def reporteMarcaVehiculos(request):
    #Agregar permisos. Esto lo ve el administrativo
    context={}
    context['titulo'] = "Reporte 1"
    return render (request, 'reportes/reporte_marcas_vehiculos_recurrentes.html',context)

def getMarcasVehiculos(request):
    #Agregar permisos. Esto lo ve dios unicamente
    marcas = list(Marca.objects.all().values('pk','nombre'))
    r = []
    for marca in marcas:
        cantidad = Vehiculo.objects.filter(modelo__marca = marca['pk']).count()
        r.append({'cantidad': cantidad , 'nombre':marca['nombre']})
    r.sort(key=lambda c : c['cantidad'], reverse=True)

    return JsonResponse({'vehiculos' : r })


def reporteFacturacion(request):
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
        
        semanas_diferencia = (fecha_hasta - fecha_desde).days // 7 +1
        anio = fecha_desde.year
        for i in range (semanas_diferencia):
            fecha = (fecha_desde+timedelta(days=i*7))
            semana = fecha.isocalendar()[1]
            anio = fecha.isocalendar()[0]
            labels.append(f'S{semana} ({anio})')

            facturacion_semanal = 0
            facturas = Factura.objects.filter(fecha__week=semana, fecha__year=anio)
            for f in facturas:
                facturacion_semanal += f.total()
            if len(facturado) > 0:
                facturado.append(facturado[len(facturado)-1] + facturacion_semanal)
            else:
                facturado.append(facturacion_semanal)

            pagos_semanales = 0
            pagos = Pago.objects.filter(fecha__week=semana, fecha__year=anio)
            for p in pagos:
                pagos_semanales += p.monto
            if len(pagado) > 0:
                pagado.append(pagado[len(pagado)-1] + pagos_semanales)
            else:
                pagado.append(pagos_semanales)

    elif periodicidad == "3": # Mensualmente

        meses_diferencia = 1 + (fecha_hasta.year * 12 + fecha_hasta.month - (fecha_desde.year * 12 + fecha_desde.month))
        # print(f'DEBUG: Entre ambas fechas hay {(fecha_hasta - fecha_desde).days} días')
        # print(f'DEBUG: Entre ambas fechas hay {meses_diferencia} meses de diferencia.')
        anio = fecha_desde.year
        for i in range (meses_diferencia):
            # print(f'DEBUG: inicio de loop, i={i}.')
            mes = (fecha_desde.month+i) % 12
            if mes == 0:
                mes = 12
            # print(f'DEBUG: mes es {mes}.')
            labels.append(f'{mes}/{anio}')
            # print(f'DEBUG: agrego label {mes}/{anio}.')
            if mes == 12: 
                anio += 1
                # print(f'DEBUG: mes es 12 -> ahora anio es {anio}')

            facturacion_mensual = 0
            facturas = Factura.objects.filter(fecha__year=anio, fecha__month=mes)
            for f in facturas:
                facturacion_mensual += f.total()
            if len(facturado) > 0:
                facturado.append(facturado[len(facturado)-1] + facturacion_mensual)
            else:
                facturado.append(facturacion_mensual)

            pagos_mensuales = 0
            pagos = Pago.objects.filter(fecha__year=anio, fecha__month=mes)
            for p in pagos:
                pagos_mensuales += p.monto
            if len(pagado) > 0:
                pagado.append(pagado[len(pagado)-1] + pagos_mensuales)
            else:
                pagado.append(pagos_mensuales)



    return JsonResponse({'labels' : labels, 'facturado': facturado, 'pagado': pagado })

def reporteHorasTrabajo(request):
    context={}
    context['titulo'] = "Reporte de productividad de los empleados"
    return render (request, 'reportes/reporte_horas_trabajo.html',context)

def getHorasTrabajo(request, tipo):
    tareas_pintura = list(Tarea.objects.filter(tipo__planilla=True).values('id'))

    tareas_taller = [t['id'] for t in list(Tarea.objects.filter(tipo__planilla=False).values('id'))]
    tareas_pintura = [t['id'] for t in list(Tarea.objects.filter(tipo__planilla=True).values('id'))]

    trabajos = list(DetalleOrdenDeTrabajo.objects.filter(exitosa=True).values('tarea_id', 'empleado_id', 'inicio', 'fin', 'exitosa', 'empleado_id__nombre', 'empleado_id__apellido'))
    
    r_taller = {}
    for t in trabajos:
        if t['tarea_id'] in tareas_taller:
            empleado = t['empleado_id']
            if r_taller.get(empleado) == None:
                r_taller[empleado] = {'cantidad': 0, 'horas': [], 'nombre': f'{t["empleado_id__nombre"]} {t["empleado_id__apellido"]}'}

            r_taller[empleado]['cantidad'] += 1
            r_taller[empleado]['horas'].append(floor((t['fin'] - t['inicio']).total_seconds()/60/60))

    for t in r_taller:
        obj = r_taller[t]
        obj['promedio'] = sum(obj['horas']) / len(obj['horas'])
        obj.pop('horas')

    return JsonResponse({'resultado': r_taller,'taller': tareas_taller, 'pintura': tareas_pintura, 'trabajos': trabajos})


def reporteOrdenes(request):
    context={}
    context['titulo'] = "Reporte de ordenes"
    return render (request, 'reportes/reporte_ordenes.html', context)
 
def getOrdenes(request, params):
    params_f = params.split(',')
    periodicidad = params_f[0]
    fecha_desde = datetime.strptime(params_f[1], '%Y-%m-%d').date()
    fecha_hasta = datetime.strptime(params_f[2], '%Y-%m-%d').date()
    dias_diferencia = (fecha_hasta - fecha_desde).days + 1 # +1 para incluir la fecha_hasta
   
    labels = []
 
    ordenes = OrdenDeTrabajo.objects.all().values("turno")
 
 
    return JsonResponse
