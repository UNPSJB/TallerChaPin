from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import *
from .forms import * 
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from wkhtmltopdf.views import PDFTemplateView
from django.contrib import messages


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
        self.filename = presupuesto.cliente.nombre + '-' + presupuesto.cliente.apellido + '-'+ str(date.today()) + '.pdf' # definimos el nombre del pdf con datos del cliente.
        context["presupuesto"] = presupuesto # pasamos el objeto presupuesto para usarlo en el template.
        context["styles"] = 'http://127.0.0.1:8000/static/ordenes/css/presupuesto_pdf.css'
        context["logo"] = 'http://127.0.0.1:8000/static/images/chapin2.png'
        return context

#Clase repetida... 
class ListFilterView(ListView):
    filtros = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.filtros:
            context['filtros'] = self.filtros(self.request.GET)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if self.filtros:
            filtros = self.filtros(self.request.GET)
            return filtros.apply(qs)
        return qs

# Presupuesto

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
    form_class = PresupuestoForm
    success_url = reverse_lazy('crearPresupuesto')
    material_form = None
    repuesto_form = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['presupuesto_material_formset'] = self.material_form or PresupuestoMaterialInline()()
        context['presupuesto_material_formset_helper'] = PresupuestoMaterialFormSetHelper()
        context['presupuesto_repuesto_formset'] = self.repuesto_form or PresupuestoRepuestoInline()()
        context['presupuesto_repuesto_formset_helper'] = PresupuestoRepuestoFormSetHelper()
        context['titulo'] = "Registrar Presupuesto"
        return context

    def post(self, *args, **kwargs):
        self.object = None
        self.material_form = PresupuestoMaterialInline()(self.request.POST)
        self.repuesto_form = PresupuestoRepuestoInline()(self.request.POST)
        form = PresupuestoForm(self.request.POST)
        if self.repuesto_form.is_valid() and self.material_form.is_valid() and form.is_valid():
            print(self.material_form.cleaned_data, self.repuesto_form.cleaned_data)
            # TODO: obtener listados de materiales y repuestos (y sus cantidades) y pasarselos al save del Form.
            presupuesto = form.save(self.material_form.cleaned_data, self.repuesto_form.cleaned_data)
            return redirect ('detallesPresupuesto',presupuesto.pk)
        return self.form_invalid(form=form)



class PresupuestoUpdateView(UpdateView):

    model = Presupuesto
    form_class = PresupuestoForm
    success_url = reverse_lazy('listarPresupuestos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial_materiales = [
            {'material': pm["material_id"], "cantidad": pm["cantidad"]} for pm in self.get_object().presupuesto_materiales.all().values()]
        initial_repuestos = [
            {'repuesto': pr["repuesto_id"], "cantidad": pr["cantidad"]} for pr in self.get_object().presupuesto_repuestos.all().values()]

        print(f"{initial_materiales=}")
        print(f"{initial_repuestos=}")
        context['presupuesto_material_formset'] = PresupuestoMaterialInline(len(initial_materiales))(initial = initial_materiales) #pasarle las lineas previas
        context['presupuesto_material_formset_helper'] = PresupuestoMaterialFormSetHelper()
        context['presupuesto_repuesto_formset'] = PresupuestoRepuestoInline(len(initial_repuestos))(initial = initial_repuestos) #pasarle las lineas previas
        context['presupuesto_repuesto_formset_helper'] = PresupuestoRepuestoFormSetHelper()
        context['titulo'] = "Modificar presupuesto"
        return context

class PresupuestoDeleteView(DeleteView):

    model = Presupuesto
    success_url = reverse_lazy('listarPresupuestos')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

# Orden de trabajo

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
            return redirect ('detallesOrden', orden.pk)
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

# Detalle de orden
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
        # context['enProceso'] = DetalleOrdenDeTrabajo.objects.en_proceso()
        context['asignados'] = DetalleOrdenDeTrabajo.objects.asignados()
        context['finalizados'] = DetalleOrdenDeTrabajo.objects.finalizados()
        # Pasar formulario por contexto
        context['asignarEmpleadoForm'] = AsignarEmpleadoForm()
        context['finalizarTareaForm'] = FinalizarTareaForm()
        context['asignarCantidadForm'] = AsignarCantidadForm()
        return context

    def post(self, *args, **kwargs):
        pass


def iniciar_tarea(request, pk):
    detalle = DetalleOrdenDeTrabajo.objects.get(pk=pk)
    if detalle.tarea.tipo.planilla:
        redirect('cargarPlanillaParaTarea', detalle.pk)
    else:
        detalle.iniciar(detalle.empleado)
        messages.add_message(request, messages.SUCCESS, 'Tarea iniciada!')
        return redirect('listarDetallesOrden')

def asignar_empleado(request):
    form = AsignarEmpleadoForm(request.POST)
    if form.is_valid():
        form.asignar()
        messages.add_message(request, messages.SUCCESS,
                             'La tarea se asignó a un empleado exitosamente! :D')
    else:
        messages.add_message(request, messages.WARNING, 'El formulario tiene errores.')  # TODO: mostrar form.errors
    return redirect('listarDetallesOrden')

def finalizar_tarea(request):
    form = FinalizarTareaForm(request.POST)
    if form.is_valid():
        form.finalizar()
        messages.add_message(request, messages.SUCCESS,
                             'La tarea finalizó exitosamente! :D')
    else:
        print(form.errors)
        messages.add_message(request, messages.WARNING,
                             'El formulario tiene errores.')  # TODO: mostrar form.errors
    return redirect('listarDetallesOrden')


class PlanillaCreateView(CreateView):
    model = PlanillaDePintura
    #form_class = PlanillaDePinturaForm # TODO

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Crear Planilla de pintura"
        return context


class RegistrarIngresoVehiculoCreateView(CreateView):
    
    model= OrdenDeTrabajo
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

            return redirect ('detallesOrden', orden.pk)
        return redirect ('registrarIngresoDeVehiculo')

class RegistrarEgresoVehiculoCreateView(CreateView):
    
    model= OrdenDeTrabajo
    form_class = RegistrarEgresoVehiculoForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar egreso de Vehiculo"
        context['vehiculo'] = self.model.vehiculo
        return context

    def post(self, *args, **kwargs):
        form = RegistrarEgresoVehiculoForm(self.request.POST)
        if form.is_valid():
            fecha_egreso = form.cleaned_data.get('egreso')
            orden = form.cleaned_data.get('orden')
            
            orden.registrar_egreso(fecha_egreso)

            return redirect ('detallesOrden', orden.pk)
        return redirect ('registrarIngresoDeVehiculo')

class ListarTurnosListView(ListView):
    
    model = OrdenDeTrabajo
    template_name = "ordenes/calendarioturno_list.html"
 
    paginate_by = 100
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Calendario de Turnos"
        return context
 
    
