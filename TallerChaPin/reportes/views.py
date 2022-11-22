from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime, timedelta
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
from numpy import mean

def reporteMarcaVehiculos(request):
    #Agregar permisos. Esto lo ve el administrativo
    context={}
    context['titulo'] = "Marcas de vehículos más recurrentes"
    return render (request, 'reportes/reporte_marcas_vehiculos.html',context)

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

def getHorasTrabajo(request):
    tareas_pintura = list(Tarea.objects.filter(tipo__planilla=True).values('id'))

    tareas_taller = [t['id'] for t in list(Tarea.objects.filter(tipo__planilla=False).values('id'))]
    tareas_pintura = [t['id'] for t in list(Tarea.objects.filter(tipo__planilla=True).values('id'))]

    trabajos = list(DetalleOrdenDeTrabajo.objects.filter(exitosa=True, fin__isnull=False).values('tarea_id', 'empleado_id', 'inicio', 'fin', 'exitosa', 'empleado_id__nombre', 'empleado_id__apellido'))
    r_taller = {}
    for t in trabajos:
        if t['tarea_id'] in tareas_taller:
            empleado = t['empleado_id']
            if r_taller.get(empleado) == None:
                r_taller[empleado] = {'cantidad': 0, 'horas': [], 'nombre': f'{t["empleado_id__nombre"]} {t["empleado_id__apellido"]}'}

            r_taller[empleado]['cantidad'] += 1
            r_taller[empleado]['horas'].append(floor((t['fin'] - t['inicio']).total_seconds()/60/60))

    r_pintura = {}
    for t in trabajos:
        if t['tarea_id'] in tareas_pintura:
            empleado = t['empleado_id']
            if r_pintura.get(empleado) == None:
                r_pintura[empleado] = {'cantidad': 0, 'horas': [], 'nombre': f'{t["empleado_id__nombre"]} {t["empleado_id__apellido"]}'}

            r_pintura[empleado]['cantidad'] += 1
            r_pintura[empleado]['horas'].append(floor((t['fin'] - t['inicio']).total_seconds()/60/60))

    for t in r_taller:
        obj = r_taller[t]
        obj['promedio'] = sum(obj['horas']) / len(obj['horas'])
        obj.pop('horas')

    for t in r_pintura:
        obj = r_pintura[t]
        obj['promedio'] = sum(obj['horas']) / len(obj['horas'])
        obj.pop('horas')

    return JsonResponse({'data_taller': r_taller, 'data_pintura': r_pintura})


def reporteOrdenes(request):
    context={}
    context['titulo'] = "Reporte de ordenes"
    return render (request, 'reportes/reporte_ordenes.html', context)
 
def getOrdenes(request, params):
    params_f = params.split(',')
    fecha_desde = datetime.strptime(params_f[0], '%Y-%m-%d').date()
    fecha_hasta = datetime.strptime(params_f[1], '%Y-%m-%d').date()
    dias_diferencia = (fecha_hasta - fecha_desde).days + 1 # +1 para incluir la fecha_hasta

    labels = [l.reporte_id() for l in OrdenDeTrabajo.objects.all()]
    dias_orden = []
    media = []

    for i in range(dias_diferencia):
        fecha = (fecha_desde+timedelta(days=i))

        ordenes = OrdenDeTrabajo.objects.filter(turno=fecha)
        for o in ordenes:
            dias_orden.append( ( o.ingreso - o.egreso).days * -1)

    a = round(mean(dias_orden))

    for i in range(len(dias_orden)):
        media.append(a)

    
    return JsonResponse({'labels' : labels, 'dias_orden': dias_orden, 'media' : media})

def reporteClientes(request):
    context = {}
    context['titulo'] = "Reporte de clientes"
    return render (request, 'reportes/reporte_clientes.html', context)

def getClientes(request):

    ordenes = OrdenDeTrabajo.objects.all()
    
    clientes = []
    for o in ordenes:
        clientes.append(o.cliente.pk)

    d_clientes = {}
    for c in clientes:
        if d_clientes.get(c) == None:
            d_clientes[c] = {}
            d_clientes[c]['cantidad'] = 1
            d_clientes[c]['facturado'] = 0
            cliente = Cliente.objects.get(pk=c)
            d_clientes[c]['nombre'] = f'{cliente.nombre} {cliente.apellido}'
            d_clientes[c]['vip'] = cliente.vip()
        else :
            d_clientes[c]['cantidad'] += 1

    facturas = Factura.objects.all()
    for f in facturas:
        d_clientes[f.orden.cliente.pk]['facturado'] += f.total()

    
    return JsonResponse({'d_clientes': d_clientes})