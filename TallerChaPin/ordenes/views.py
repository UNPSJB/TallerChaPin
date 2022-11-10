from tkinter import E
from turtle import update
from django.http import Http404, JsonResponse
# from django.http.response import HttpResponse 
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
import json
from functools import reduce
from .utils import requiere_insumo
import os
from django.core.exceptions import ObjectDoesNotExist


def requerimientos_tareas(request):
    """
        Recibe el pk de una o mas tareas y se retorna un diccionario como:
        { "materiales": <True|False>, "repuestos": <True|False> } 
        según si alguna de ellas requiere o no materiales y/o repuestos.
    """
    pks = json.load(request)['tareas']
    tareas = [Tarea.objects.get(pk=pk) for pk in pks]
    return JsonResponse(requiere_insumo(tareas))

def tareasFinalizadas(request, pk):

    orden = Presupuesto.objects.get(pk=pk).orden
    tareas_finalizadas = orden.get_tareas_finalizadas()
            
    return JsonResponse({'tareas_finalizadas': tareas_finalizadas})

class imprimirPresupuesto(PDFTemplateView):
    template_name = 'ordenes/presupuesto_pdf.html'
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
        self.filename = f'pres. {presupuesto.cliente.nombre} {presupuesto.cliente.apellido} ({str(date.today())}).pdf'

        # pasamos el objeto presupuesto para usarlo en el template.
        context["presupuesto"] = presupuesto
        context["styles"] = os.path.abspath("./ordenes/static/ordenes/css/styles_pdf.css")
        context["logo"] = os.path.abspath("./static/images/chapin2.png")
        return context

class imprimirOrdenDeTrabajo(PDFTemplateView):
    template_name = 'ordenes/ordendetrabajo_pdf.html'
    cmd_options = {
        'margin-top': 3,
        'enable-local-file-access': True,
        'quiet': False
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get('pk')
        orden = OrdenDeTrabajo.objects.get(pk=pk)
        vehiculo = orden.get_ultimo_presupuesto().vehiculo

        # definimos el nombre del pdf con datos del cliente.
        self.filename = f'orden {vehiculo.modelo} {vehiculo.patente} ({str(date.today())}).pdf'

        # pasamos el objeto orden para usarlo en el template.
        context["orden"] = orden
        context["vehiculo"] = vehiculo
        context["styles"] = os.path.abspath("./ordenes/static/ordenes/css/styles_pdf.css")
        context["logo"] = os.path.abspath("./static/images/chapin2.png")
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
    # model = Presupuesto
    queryset = Presupuesto.objects.filter(ampliado=False)
    paginate_by = 100 
    ordering = ['-id']

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

    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            presupuesto = Presupuesto.objects.get(pk=pk)
        except Presupuesto.DoesNotExist:
            raise Http404('No existe presupuesto')
        return render(self.request, 'ordenes/presupuesto_detail.html', {'presupuesto':presupuesto})

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
            {'material': pm["material_id"], "cantidad": pm["cantidad"]} for pm in base.presupuesto_materiales.all().values()] if base is not None else [{'material': None, "cantidad": 1}]
        initial_repuestos = [
            {'repuesto': pr["repuesto_id"], "cantidad": pr["cantidad"]} for pr in base.presupuesto_repuestos.all().values()] if base is not None else [{'repuesto': None, "cantidad": 1}]

        context['presupuesto_material_formset'] = self.material_form or PresupuestoMaterialInline(len(initial_materiales))(initial = initial_materiales) #pasarle las lineas previas
        context['presupuesto_material_formset_helper'] = PresupuestoMaterialFormSetHelper()
        context['presupuesto_repuesto_formset'] = self.repuesto_form or PresupuestoRepuestoInline(len(initial_repuestos))(initial = initial_repuestos) #pasarle las lineas previas
        context['presupuesto_repuesto_formset_helper'] = PresupuestoRepuestoFormSetHelper()
        
        context['titulo'] = "Registrar Presupuesto"
        context['ayuda'] = 'presupuestos.html#creacion-de-un-presupuesto'
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

        context['presupuesto_material_formset'] = PresupuestoMaterialInline(max(len(initial_materiales), 1))(initial=initial_materiales)  # pasarle las lineas previas
        context['presupuesto_material_formset_helper'] = PresupuestoMaterialFormSetHelper()
        context['presupuesto_repuesto_formset'] = PresupuestoRepuestoInline(max(len(initial_repuestos), 1))(initial=initial_repuestos)  # pasarle las lineas previas
        context['presupuesto_repuesto_formset_helper'] = PresupuestoRepuestoFormSetHelper()

        context['titulo'] = "Modificar presupuesto"
        context['ayuda'] = 'presupuestos.html#modificacion-de-un-presupuesto'
        return context
    

    def get(self, *args, **kwargs):
        #Control para que no se pueda modificar desde una URL
        pk = kwargs.get('pk')
        try:
            presupuesto = Presupuesto.objects.get(pk=pk)
        except Presupuesto.DoesNotExist:
            raise Http404("Presupuesto no existe")
        if not presupuesto.puede_modificarse():
            messages.add_message(self.request, messages.ERROR, "El presupuesto no se puede modificar.")
            return redirect('detallesPresupuesto',presupuesto.pk)
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        p = Presupuesto.objects.get(id=kwargs['pk'])
        self.object = None
        self.material_form = PresupuestoMaterialInline()(self.request.POST)
        self.repuesto_form = PresupuestoRepuestoInline()(self.request.POST)
        form = self.get_form_class()(self.request.POST, instance=p)
        if self.repuesto_form.is_valid() and self.material_form.is_valid() and form.is_valid():
            presupuesto = form.save(
                self.material_form.cleaned_data, 
                self.repuesto_form.cleaned_data,
                form.cleaned_data['tareas'],
                update=True
            )
            return redirect('detallesPresupuesto', presupuesto.pk)
        return self.form_invalid(form=form)

class PresupuestoDeleteView(DeleteView):

    model = Presupuesto
    success_url = reverse_lazy('listarPresupuestos')

    def get(self, *args, **kwargs):
        pk= kwargs.get('pk')
        try:
            presupuesto =Presupuesto.objects.get(pk=pk)
        except Presupuesto.DoesNotExist:
            raise Http404 ("El presupuesto no existe")
        if not presupuesto.puede_eliminarse():
            messages.add_message(self.request, messages.ERROR, "El presupuesto no se puede eliminar.")
            return redirect('detallesPresupuesto',presupuesto.pk)
        return self.post(*args, **kwargs)


def confirmar_ampliacion(request, pk):
    presupuesto = Presupuesto.objects.get(pk=pk)
    orden = presupuesto.orden

    orden.aplicar_ampliacion(presupuesto)

    messages.add_message(request, messages.SUCCESS, 'La ampliación se ha aplicado correctamente.')
    return redirect ('detallesOrden', presupuesto.orden.pk)

# ----------------------------- Orden de trabajo View ----------------------------------- #

class OrdenTrabajoListView(ListFilterView):
    filtros = OrdenTrabajoFiltrosForm
    model = OrdenDeTrabajo
    paginate_by = 100  # if pagination is desired
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de órdenes de trabajo"
        return context


class OrdenTrabajoDetailView(DetailView):

    model = OrdenDeTrabajo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "TallerChaPin"
        return context

    def get (self, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            orden = OrdenDeTrabajo.objects.get(pk=pk)
        except OrdenDeTrabajo.DoesNotExist:
            raise Http404('Orden no existe')
        return render(self.request, 'ordenes/ordendetrabajo_detail.html', {'object' : orden})

class OrdenTrabajoCreateView(CreateView):
    model = OrdenDeTrabajo
    form_class = OrdenForm
    success_url = reverse_lazy('crearOrden')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Orden"
        context['ayuda'] = 'presupuestos.html#confirmacion-de-un-presupuesto'
        return context

    def get (self, *args, **kwargs):
        pk_presupuesto = kwargs.get('pk')
        form = self.get_form()
        try:
            presupuesto = Presupuesto.objects.get(pk=pk_presupuesto)
        except Presupuesto.DoesNotExist:
            raise Http404('Presupuesto no existe')
        
        if not presupuesto.puede_confirmarse():
            messages.add_message(self.request, messages.ERROR, "Orden de trabajo ya confirmada.")
            return redirect('detallesPresupuesto',presupuesto.pk)
        return render(self.request, 'ordenes/ordendetrabajo_form.html', {'form' : form ,
                                                                        'titulo': "Registrar Orden" })

    def post(self, *args, **kwargs):
        pk = kwargs.get('pk')
        presupuesto = Presupuesto.objects.get(pk=pk)
        form = OrdenForm(self.request.POST)
        if form.is_valid():
            turno = form.cleaned_data.get('turno')
            orden = presupuesto.confirmar(turno)
            return redirect('detallesOrden', orden.pk)
        else:
            messages.add_message(self.request, messages.ERROR, form.errors)
            return redirect('crearOrden', presupuesto.pk)
        
class OrdenTrabajoUpdateView(UpdateView):

    model = OrdenDeTrabajo
    form_class = OrdenUpdateForm
    success_url = reverse_lazy('calendarioTurnos')
    context_object_name = "orden"

    def get(self, *args, **kwargs):
        #Control para que no se pueda modificar desde una URL
        pk = kwargs.get('pk')
        try:
            orden = OrdenDeTrabajo.objects.get(pk=pk)
        except OrdenDeTrabajo.DoesNotExist:
            raise Http404("Orden de trabajo no existe")
        if not orden.puede_cambiar_turno():
            messages.add_message(self.request, messages.ERROR, "La orden de trabajo no se puede modificar.")
            return redirect('detallesOrden', orden.pk)
        return self.post(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Cambiar turno de la orden de trabajo"
        return context

class OrdenTrabajoDeleteView(DeleteView):

    model = OrdenDeTrabajo
    success_url = reverse_lazy('listarOrdenes')

    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            orden = OrdenDeTrabajo.objects.get(pk=pk)
        except OrdenDeTrabajo.DoesNotExist:
            raise Http404("Orden de trabajo no existe")
        if not orden.puede_cancelarse() :
            messages.add_message(self.request, messages.ERROR, "La orden de trabajo no se puede cancelar.")
            return redirect('detallesOrden', orden.pk)

        return self.post(*args, **kwargs)


def cancelar_orden(request, pk):
    try:
            orden = OrdenDeTrabajo.objects.get(pk=pk)
    except OrdenDeTrabajo.DoesNotExist:
        raise Http404("Orden de trabajo no existe")
    if not orden.puede_cancelarse() :
            messages.add_message(request, messages.ERROR, "La orden de trabajo no se puede cancelar.")
            return redirect('detallesOrden', orden.pk)
    orden.actualizar_estado(OrdenDeTrabajo.CANCELAR_ORDEN)
    return redirect ('detallesOrden', orden.pk)

def pausar_orden(request, pk):
    #Control para que no pausar desde la url
    try:
        orden = OrdenDeTrabajo.objects.get(pk=pk)
    except OrdenDeTrabajo.DoesNotExist:
        raise Http404("Orden de trabajo no existe")
    if not orden.puede_pausarse() :
        messages.add_message(request, messages.ERROR, "La orden de trabajo no se puede pausar.")
        return redirect('detallesOrden', orden.pk)    

    orden.actualizar_estado(OrdenDeTrabajo.PAUSAR_ORDEN)
    return redirect ('detallesOrden', orden.pk)

def reanudar_orden(request, pk):
    #Control para que no reanudar desde la url
    try:
        orden = OrdenDeTrabajo.objects.get(pk=pk)
    except OrdenDeTrabajo.DoesNotExist:
        raise Http404("Orden de trabajo no existe")
    if not orden.puede_reanudarse() :
        messages.add_message(request, messages.ERROR, "La orden de trabajo no se puede reanudar.")
        return redirect('detallesOrden', orden.pk)

    orden.actualizar_estado(OrdenDeTrabajo.REANUDAR_ORDEN)
    return redirect ('detallesOrden', orden.pk)

# ----------------------------- Detalle de orden View ----------------------------------- #

class DetalleOrdenDeTrabajoListView(ListFilterView):
    model = DetalleOrdenDeTrabajo
    paginate_by = 100
    ordering = ['id']

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
        context['titulo'] = "Listado de detalles de orden de trabajo"
        context['ayuda'] = 'home.html#trabajos'
        context['sinAsignar'] = DetalleOrdenDeTrabajo.objects.sin_asignar()
        context['sinFinalizar'] = DetalleOrdenDeTrabajo.objects.sin_finalizar()
        context['asignados'] = DetalleOrdenDeTrabajo.objects.asignados()
        context['finalizados'] = DetalleOrdenDeTrabajo.objects.finalizados()
        context['todos'] = DetalleOrdenDeTrabajo.objects.todos()
        
        # Pasar formulario por contexto
        context['asignarEmpleadoForm'] = AsignarEmpleadoForm()
        context['finalizarTareaForm'] = FinalizarTareaForm()
        context['asignarCantidadForm'] = AsignarCantidadForm()
        return context

    def post(self, *args, **kwargs):
        pass


# ----------------------------- Iniciar Tarea ----------------------------------- #

def iniciar_tarea(request, pk):
    try:
        detalle = DetalleOrdenDeTrabajo.objects.get(pk=pk)
    except DetalleOrdenDeTrabajo.DoesNotExist:
        raise Http404("No existe detalle de orden de trabajo")
    if not detalle.puedo_iniciar():
        messages.add_message(request, messages.WARNING, 'No se puede iniciar la tarea')
        return redirect('listarDetallesOrden')
    detalle.iniciar(detalle.empleado)
    messages.add_message(request, messages.SUCCESS, 'La tarea se inició exitosamente')
    return redirect('listarDetallesOrden')

# ----------------------------- Asignar Tarea a Empleado ----------------------------------- #

def asignar_empleado(request):
    form = AsignarEmpleadoForm(request.POST)
    if form.is_valid():
        form.asignar()
        messages.add_message(request, messages.SUCCESS,
                             'La tarea se asignó a un empleado exitosamente')
    else:
        messages.add_message(request, messages.WARNING,
                             'El formulario tiene errores.')
    return redirect('listarDetallesOrden')

# ----------------------------- Finalizar Tarea ----------------------------------- #

def finalizar_tarea(request):
    form = FinalizarTareaForm(request.POST)
    if form.is_valid():
        form.finalizar()
        messages.add_message(request, messages.SUCCESS,
                             'La tarea finalizó exitosamente!')
    else:
        messages.add_message(request, messages.ERROR, form.errors) 
    return redirect('listarDetallesOrden')

# ----------------------------- Asignar cantidad de insumos ----------------------------------- #

def asignar_cantidad(request):
    form = AsignarCantidadForm(request.POST)
    if form.is_valid():
        form.actualizar_cantidad()
        messages.add_message(request, messages.SUCCESS,
                             'Se registraron los insumos exitosamente')
    else:
        messages.add_message(request, messages.WARNING, form.errors) 
    return redirect('listarDetallesOrden')

# ----------------------------- Resumen de orden ----------------------------------- #

def resumen_orden(request, pk):
    try:
        orden = DetalleOrdenDeTrabajo.objects.get(pk=pk).orden
    except OrdenDeTrabajo.DoesNotExist:
        raise Http404("Orden no existe")
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
        context["titulo"] = "Crear planilla de pintura"
        context['detalle'] = DetalleOrdenDeTrabajo.objects.get(pk=self.kwargs.get('detalle'))
        return context

    #Mejorar
    def post(self, *args, **kwargs):
        self.object = None
        self.detalle_planilla_form = DetallePlanillaInline()(self.request.POST)
        form = PlanillaDePinturaForm(self.request.POST)        
        detalle_orden = DetalleOrdenDeTrabajo.objects.get(pk=self.kwargs.get('detalle'))
        if self.detalle_planilla_form.is_valid() and form.is_valid():
            planilla = form.save(self.detalle_planilla_form.cleaned_data, detalle_orden) # VER
            messages.add_message(self.request, messages.SUCCESS, 'La planilla de pintura se ha registrado exitosamente')
            return redirect ('listarDetallesOrden')
        else:
            messages.add_message(self.request, messages.ERROR, form.errors)
        return self.form_invalid(form=form)

class PlanillaUpdateView(UpdateView):

    model = PlanillaDePintura
    form_class = PlanillaDePinturaForm
    success_url = reverse_lazy("listarVehiculos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar planilla de pintura"
        context['modificando'] = True
        context['pk_planilla'] = self.kwargs['pk']

        initial_detalles = [
            {'formula': p["formula"], "cantidad": p["cantidad"]} for p in self.get_object().detalles.all().values()]

        context['detalle_planilla_formset'] = DetallePlanillaInline(len(initial_detalles))(initial=initial_detalles)
        context['detalle_planilla_formset_helper'] = DetallePlanillaFormSetHelper()

        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Planilla modificada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

    def post(self, *args, **kwargs):
        self.object = None
        self.detalle_planilla_form = DetallePlanillaInline()(self.request.POST)
        print('form:')
        print(self.detalle_planilla_form)
        form = PlanillaDePinturaForm(self.request.POST)        
        planilla = PlanillaDePintura.objects.get(pk=self.kwargs.get('pk'))
        if self.detalle_planilla_form.is_valid() and form.is_valid():
            planilla = form.save(self.detalle_planilla_form.cleaned_data, update=True, planilla_pintura=planilla)
            messages.add_message(self.request, messages.SUCCESS, 'La planilla de pintura se ha registrado exitosamente')
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

    def get_orden(self):
        
        pk = self.kwargs["pk"] if "pk" in self.kwargs.keys() else None
        return OrdenDeTrabajo.objects.get(pk=pk) if pk is not None else None

    def get_form_class(self, *args, **kwargs):
        orden = self.get_orden()
        return RegistrarIngresoVehiculoForm(orden)
    
    #Carga el formulario pero no el titulo del formulario
    def get(self, *args, **kwargs):
        form = self.get_form()
        try:
            orden = self.get_orden()
        except OrdenDeTrabajo.DoesNotExist:
            raise Http404("Orden no existe")
        if orden is not None:
            if not orden.puede_ingresar_vehiculo():
                messages.add_message(self.request, messages.ERROR, "No se puede registrar ingreso del vehiculo.")
                return redirect('detallesPresupuesto',orden.pk)
        return render(self.request, 'ordenes/registraringresovehiculo_form.html', {'form' : form,
                                                                                    'titulo' : "Registrar Ingreso de Vehiculo"})

    def post(self, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(self.request.POST)
        if form.is_valid():
            fecha_ingreso = form.cleaned_data.get('ingreso')
            orden = form.cleaned_data.get('orden', self.get_orden())
            orden.registrar_ingreso(fecha_ingreso)
            return redirect('detallesOrden', orden.pk)
        return redirect('registrarIngresoVehiculo')


# ----------------------------- Entrega de Vehiculo View ----------------------------------- #

class RegistrarEgresoVehiculoCreateView(CreateView):

    model = OrdenDeTrabajo
    form_class = RegistrarEgresoVehiculoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar egreso de Vehículo"
        context['vehiculo'] = self.model.vehiculo
        return context

    def get_orden(self):
        pk = self.kwargs["pk"] if "pk" in self.kwargs.keys() else None
        return OrdenDeTrabajo.objects.get(pk=pk) if pk is not None else None
        
    def get_form_class(self, *args, **kwargs):
        orden = self.get_orden()
        return RegistrarEgresoVehiculoForm(orden)
    #Carga el formulario pero no el titulo del formulario
    def get(self, *args, **kwargs):
        form = self.get_form()
        try:
            orden = self.get_orden()
        except OrdenDeTrabajo.DoesNotExist:
            raise Http404("Orden no existe")
        if orden is not None:
            if not orden.puede_retirar_vehiculo():
                messages.add_message(self.request, messages.ERROR, "No se puede registrar retiro del vehiculo.")
                return redirect('detallesPresupuesto',orden.pk)
        return render(self.request, 'ordenes/registraringresovehiculo_form.html', {'form' : form,
                                                                                    'titulo' : "Registrar Ingreso de Vehiculo"})
    
    def post(self, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(self.request.POST)
        if form.is_valid():
            fecha_egreso = form.cleaned_data.get('egreso')
            orden = form.cleaned_data.get('orden', self.get_orden())
            try:
                orden.registrar_egreso(fecha_egreso)
            except NoEntregoVehiculoException as err:
                messages.add_message(self.request, messages.ERROR, err)
                return redirect('detallesOrden', orden.pk)

            return redirect('detallesOrden', orden.pk)
        return redirect('registrarIngresoVehiculo')

# ----------------------------- Turnos View ----------------------------------- #

class ListarTurnosListView(ListView):

    model = OrdenDeTrabajo
    template_name = "ordenes/calendarioturno_list.html"
    ordering = ['id']
    paginate_by = 100

    def get_turnos(self):
        return {'test': 'true', 'attribute': 'pepe'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Calendario de Turnos"
        context['turnos'] = self.get_turnos()
        context['ayuda'] = 'turnos.html'
        return context
    
def datoPlantilla(request, pk):
    orden = OrdenDeTrabajo.objects.get(pk=pk)
    return render (request,'ordenes/datoPlantilla.html',{'orden':orden})
