from multiprocessing import context
from django.http import request
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import *
from .forms import *
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from wkhtmltopdf.views import PDFTemplateView
from django.contrib import messages
from TallerChaPin.utils import ListFilterView

class imprimirPresupuesto(PDFTemplateView):
    #filename = 'presupuesto_pedro.pdf'
    template_name = 'ordenes/template_pdf.html'
    cmd_options = {
        'margin-top': 3,
        'enable-local-file-access': True,
        'quiet': False
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get('pk')
        presupuesto = Presupuesto.objects.get(pk=pk)
        # definimos el nombre del pdf con datos del cliente.
        self.filename = presupuesto.cliente.nombre + '-' + \
            presupuesto.cliente.apellido + '-' + str(date.today()) + '.pdf'
        # pasamos el objeto presupuesto para usarlo en el template.
        context["presupuesto"] = presupuesto
        context["styles"] = 'http://127.0.0.1:8000/static/ordenes/css/presupuesto_pdf.css'
        context["logo"] = 'http://127.0.0.1:8000/static/images/chapin2.png'
        return context

# Clase repetida...


# class ListFilterView(ListView):
#     filtros = None

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.filtros:
#             context['filtros'] = self.filtros(self.request.GET)
#         return context

#     def get_queryset(self):
#         qs = super().get_queryset()
#         if self.filtros:
#             filtros = self.filtros(self.request.GET)
#             return filtros.apply(qs)
#         return qs

# ----------------------------- Presupuesto View ----------------------------------- #
class PresupuestoListView(ListFilterView):
    filtros = PresupuestoFiltrosForm
    model = Presupuesto
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de presupuestos"
        return context


class PresupuestoDetailView(DetailView):

    model = Presupuesto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "TallerChaPin"
        return context


class PresupuestoCreateView(CreateView):
    model = Presupuesto
    #form_class = PresupuestoForm
    success_url = reverse_lazy('crearPresupuesto')
    material_form = None
    repuesto_form = None

    def get_presupuesto_base(self):
        pk = self.kwargs["pk"] if "pk" in self.kwargs.keys() else None
        return Presupuesto.objects.get(pk=pk) if pk is not None else None
        
    def get_form_class(self, *args, **kwargs):
        base = self.get_presupuesto_base()
        return PresupuestoForm(base)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        base = self.get_presupuesto_base()
        if base is not None:
            kwargs['initial'] = { 
                "tareas": base.tareas.all() 
            }
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = self.get_presupuesto_base()
        
        initial_materiales = [
            {'material': pm["material_id"], "cantidad": pm["cantidad"]} for pm in base.presupuesto_materiales.all().values()] if base is not None else [{'material': None, "cantidad": 0}]
        initial_repuestos = [
            {'repuesto': pr["repuesto_id"], "cantidad": pr["cantidad"]} for pr in base.presupuesto_repuestos.all().values()] if base is not None else [{'repuesto': None, "cantidad": 0}]

        context['presupuesto_material_formset'] = self.material_form or PresupuestoMaterialInline(len(initial_materiales))(initial = initial_materiales) #pasarle las lineas previas
        context['presupuesto_material_formset_helper'] = PresupuestoMaterialFormSetHelper()
        context['presupuesto_repuesto_formset'] = self.repuesto_form or PresupuestoRepuestoInline(len(initial_repuestos))(initial = initial_repuestos) #pasarle las lineas previas
        context['presupuesto_repuesto_formset_helper'] = PresupuestoRepuestoFormSetHelper()
        
        context['titulo'] = "Registrar Presupuesto"
        return context

    def post(self, *args, **kwargs):
        self.object = None
        self.material_form = PresupuestoMaterialInline()(self.request.POST)
        self.repuesto_form = PresupuestoRepuestoInline()(self.request.POST)
        form = self.get_form_class()(self.request.POST)
        if self.repuesto_form.is_valid() and self.material_form.is_valid() and form.is_valid():
            presupuesto = form.save(
                self.material_form.cleaned_data, 
                self.repuesto_form.cleaned_data,
                form.cleaned_data['tareas'])
            return redirect('detallesPresupuesto', presupuesto.pk)
        return self.form_invalid(form=form)

class PresupuestoUpdateView(UpdateView):

    model = Presupuesto
    form_class = PresupuestoForm()
    success_url = reverse_lazy('listarPresupuestos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial_materiales = [
            {'material': pm["material_id"], "cantidad": pm["cantidad"]} for pm in self.get_object().presupuesto_materiales.all().values()]
        initial_repuestos = [
            {'repuesto': pr["repuesto_id"], "cantidad": pr["cantidad"]} for pr in self.get_object().presupuesto_repuestos.all().values()]

        context['presupuesto_material_formset'] = PresupuestoMaterialInline(len(initial_materiales))(initial=initial_materiales)  # pasarle las lineas previas
        context['presupuesto_material_formset_helper'] = PresupuestoMaterialFormSetHelper()
        context['presupuesto_repuesto_formset'] = PresupuestoRepuestoInline(len(initial_repuestos))(initial=initial_repuestos)  # pasarle las lineas previas
        context['presupuesto_repuesto_formset_helper'] = PresupuestoRepuestoFormSetHelper()
        context['titulo'] = "Modificar presupuesto"
        return context


class PresupuestoDeleteView(DeleteView):

    model = Presupuesto
    success_url = reverse_lazy('listarPresupuestos')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

# ----------------------------- Orden de trabajo View ----------------------------------- #

class OrdenTrabajoListView(ListFilterView):
    filtros = OrdenTrabajoFiltrosForm
    model = OrdenDeTrabajo
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Ordenes de trabajo"
        return context


class OrdenTrabajoDetailView(DetailView):

    model = OrdenDeTrabajo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "TallerChaPin"
        return context


class OrdenTrabajoCreateView(CreateView):
    model = OrdenDeTrabajo
    form_class = OrdenForm
    success_url = reverse_lazy('crearOrden')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Orden"
        return context

    def post(self, *args, **kwargs):
        pk = kwargs.get('pk')
        presupuesto = Presupuesto.objects.get(pk=pk)
        form = OrdenForm(self.request.POST)
        if form.is_valid():
            turno = form.cleaned_data.get('turno')
            orden = presupuesto.confirmar(turno)
            return redirect('detallesOrden', orden.pk)
        return redirect('crearOrden', presupuesto.pk)
        
class OrdenTrabajoUpdateView(UpdateView):

    model = OrdenDeTrabajo
    form_class = OrdenForm
    success_url = reverse_lazy('listarOrdenes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Cambiar turno de la orden de trabajo"
        return context


class OrdenTrabajoDeleteView(DeleteView):

    model = OrdenDeTrabajo
    success_url = reverse_lazy('listarOrdenes')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

def cancelar_orden(request, pk):
    orden = OrdenDeTrabajo.objects.get(pk=pk)
    orden.estado = OrdenDeTrabajo.CANCELADA
    orden.save()
    return redirect ('detallesOrden', orden.pk)

def pausar_orden(request, pk):
    orden = OrdenDeTrabajo.objects.get(pk=pk)
    orden.estado = OrdenDeTrabajo.PAUSADA
    orden.save()
    return redirect ('detallesOrden', orden.pk)

def reanudar_orden(request, pk):
    orden = OrdenDeTrabajo.objects.get(pk=pk)
    if orden.no_hay_tareas_iniciadas():
        orden.estado = OrdenDeTrabajo.ACTIVA
    else:
        orden.estado = OrdenDeTrabajo.INICIADA
    orden.save()
    return redirect ('detallesOrden', orden.pk)

# ----------------------------- Detalle de orden View ----------------------------------- #

class DetalleOrdenDeTrabajoListView(ListFilterView):
    # filtros = OrdenTrabajoFiltrosForm
    model = DetalleOrdenDeTrabajo
    paginate_by = 100

    def get_queryset(self):
        user = self.request.user
        try:
            return DetalleOrdenDeTrabajo.objects.para_empleado(user.empleado)
        except ObjectDoesNotExist:
            if user.is_superuser:
                return super().get_queryset()
            else:
                return DetalleOrdenDeTrabajo.objects.none()
        except AttributeError:
            return DetalleOrdenDeTrabajo.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de detalles de Orden de Trabajo"
        context['sinAsignar'] = DetalleOrdenDeTrabajo.objects.sin_asignar()
        context['sinFinalizar'] = DetalleOrdenDeTrabajo.objects.sin_finalizar()
        context['asignados'] = DetalleOrdenDeTrabajo.objects.asignados()
        context['finalizados'] = DetalleOrdenDeTrabajo.objects.finalizados()
        
        # Pasar formulario por contexto
        context['asignarEmpleadoForm'] = AsignarEmpleadoForm()
        context['finalizarTareaForm'] = FinalizarTareaForm()
        context['asignarCantidadForm'] = AsignarCantidadForm()
        return context

    def post(self, *args, **kwargs):
        pass


# ----------------------------- Iniciar Tarea ----------------------------------- #

def iniciar_tarea(request, pk):
    detalle = DetalleOrdenDeTrabajo.objects.get(pk=pk)
    detalle.iniciar(detalle.empleado)
    messages.add_message(request, messages.SUCCESS, 'Tarea iniciada!')
    return redirect('listarDetallesOrden')

# ----------------------------- Asignar Tarea a Empleado ----------------------------------- #

def asignar_empleado(request):
    form = AsignarEmpleadoForm(request.POST)
    if form.is_valid():
        form.asignar()
        messages.add_message(request, messages.SUCCESS,
                             'La tarea se asignó a un empleado exitosamente! :D')
    else:
        # TODO: mostrar form.errors
        print(form.errors)
        messages.add_message(request, messages.WARNING,
                             'El formulario tiene errores.')
    return redirect('listarDetallesOrden')

# ----------------------------- Finalizar Tarea ----------------------------------- #

def finalizar_tarea(request):
    form = FinalizarTareaForm(request.POST)
    if form.is_valid():
        form.finalizar()
        # Ver de agregar actualizar estado
        messages.add_message(request, messages.SUCCESS,
                             'La tarea finalizó exitosamente! :D')
    else:
        messages.add_message(request, messages.ERROR,
                             'El formulario tiene errores.')  # TODO: mostrar form.errors
    return redirect('listarDetallesOrden')

# ----------------------------- Asignar cantidad de insumos ----------------------------------- #

def asignar_cantidad(request):
    form = AsignarCantidadForm(request.POST)
    if form.is_valid():
        form.actualizar_cantidad()
        messages.add_message(request, messages.SUCCESS,
                             'Se registraron los insumos exitosamente! :D')
    else:
        messages.add_message(request, messages.WARNING,
                             'No se registraron los insumos el formulario tiene errores.')  # TODO: mostrar form.errors
    return redirect('listarDetallesOrden')

# ----------------------------- Resumen de orden ----------------------------------- #

def resumen_orden(request, pk):
    orden = DetalleOrdenDeTrabajo.objects.get(pk=pk).orden
    presupuesto = orden.presupuestos.first()

    materiales_orden = orden.orden_materiales.all()
    materiales_pres = presupuesto.presupuesto_materiales.all()

    materiales = []
    for i in range(0, materiales_orden.count()):
        try:
            materiales.append((
                materiales_orden[i].material.nombre, 
                materiales_pres[i].cantidad, 
                materiales_orden[i].cantidad,
                materiales_orden[i].material.tipo.get_unidad_medida_display()
                ))
        except IndexError:
            materiales.append((
                materiales_orden[i].material.nombre, 
                0, 
                materiales_orden[i].cantidad,
                materiales_orden[i].material.tipo.get_unidad_medida_display()
                ))

    repuestos_orden = orden.orden_repuestos.all()
    repuestos_pres = presupuesto.presupuesto_repuestos.all()

    repuestos = []
    for i in range(0, repuestos_orden.count()):
        try:
            repuestos.append((
                repuestos_orden[i].repuesto.nombre, 
                repuestos_pres[i].cantidad, 
                repuestos_orden[i].cantidad
                )) 
        except IndexError:
            repuestos.append((
                repuestos_orden[i].repuesto.nombre, 
                0, 
                repuestos_orden[i].cantidad
                )) 

    return render(request, 'ordenes/orden-resumen.html', {
        'orden': orden, 
        'materiales': materiales,
        'repuestos': repuestos
    })


# ----------------------------- Planilla de Pintura View ----------------------------------- #

class PlanillaCreateView(CreateView):
    model = PlanillaDePintura
    form_class = PlanillaDePinturaForm
    success_url = reverse_lazy('listarDetallesOrden')
    detalle_planilla_form = None

    def get_form_kwargs(self,*args,**kwargs) :
        kw = super().get_form_kwargs()
        kw['detalle'] = DetalleOrdenDeTrabajo.objects.get(pk=self.kwargs.get('detalle'))
        return kw

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalle_planilla_formset'] = DetallePlanillaInline()()
        context['detalle_planilla_formset_helper'] = DetallePlanillaFormSetHelper()
        context["titulo"] = "Crear Planilla de pintura"
        context['detalle'] = DetalleOrdenDeTrabajo.objects.get(pk=self.kwargs.get('detalle'))
        return context
        

    def post(self, *args, **kwargs):
        self.object = None
        self.detalle_planilla_form = DetallePlanillaInline()(self.request.POST)
        form = PlanillaDePinturaForm(self.request.POST)        
        detalle_orden = DetalleOrdenDeTrabajo.objects.get(pk=self.kwargs.get('detalle'))
        if self.detalle_planilla_form.is_valid() and form.is_valid():
            planilla = form.save(self.detalle_planilla_form.cleaned_data, detalle_orden)
            messages.add_message(self.request, messages.INFO, 'Planilla Creada')
            return redirect ('listarDetallesOrden')
        else:
            messages.add_message(self.request, messages.ERROR, form.errors)
        return self.form_invalid(form=form)



# ----------------------------- Ingreso de Vehiculo View ----------------------------------- #

class RegistrarIngresoVehiculoCreateView(CreateView):

    model = OrdenDeTrabajo
    form_class = RegistrarIngresoVehiculoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Ingreso de Vehiculo"
        context['vehiculo'] = self.model.vehiculo
        return context

    def post(self, *args, **kwargs):
        form = RegistrarIngresoVehiculoForm(self.request.POST)
        if form.is_valid():
            fecha_ingreso = form.cleaned_data.get('ingreso')
            orden = form.cleaned_data.get('orden')

            orden.registrar_ingreso(fecha_ingreso)

            return redirect('detallesOrden', orden.pk)
        return redirect('registrarIngresoDeVehiculo')


# ----------------------------- Entrega de Vehiculo View ----------------------------------- #

class RegistrarEgresoVehiculoCreateView(CreateView):

    model = OrdenDeTrabajo
    form_class = RegistrarEgresoVehiculoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar egreso de Vehículo"
        context['vehiculo'] = self.model.vehiculo
        return context

    def post(self, *args, **kwargs):
        form = RegistrarEgresoVehiculoForm(self.request.POST)
        if form.is_valid():
            fecha_egreso = form.cleaned_data.get('egreso')
            orden = form.cleaned_data.get('orden')

            orden.registrar_egreso(fecha_egreso)

            return redirect('detallesOrden', orden.pk)
        return redirect('registrarIngresoDeVehiculo')

# ----------------------------- Turnos View ----------------------------------- #

class ListarTurnosListView(ListView):

    model = OrdenDeTrabajo
    template_name = "ordenes/calendarioturno_list.html"

    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Calendario de Turnos"
        return context
    
def datoPlantilla(request, pk):
    orden = OrdenDeTrabajo.objects.get(pk=pk)
    return render (request,'ordenes/datoPlantilla.html',{'orden':orden})



    
