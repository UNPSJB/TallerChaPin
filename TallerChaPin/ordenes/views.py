from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import *
from .forms import * 
from datetime import date

from wkhtmltopdf.views import PDFTemplateView


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['presupuesto_material_formset'] = PresupuestoMaterialInline()()
        context['presupuesto_material_formset_helper'] = PresupuestoMaterialFormSetHelper()
        context['presupuesto_repuesto_formset'] = PresupuestoRepuestoInline()()
        context['presupuesto_repuesto_formset_helper'] = PresupuestoRepuestoFormSetHelper()
        context['titulo'] = "Registrar Presupuesto"
        return context

    def post(self, *args, **kwargs):
        pmi = PresupuestoMaterialInline()(self.request.POST)
        pri = PresupuestoRepuestoInline()(self.request.POST)
        form = PresupuestoForm(self.request.POST)
        print(pmi.cleaned_data,pri.cleaned_data)
        if pmi.is_valid() and pri.is_valid() and form.is_valid():
            # TODO: obtener listados de materiales y repuestos (y sus cantidades) y pasarselos al save del Form.
            presupuesto = form.save(pmi.cleaned_data, pri.cleaned_data)
        return redirect ('detallesPresupuesto',presupuesto.pk)



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
            # TODO: obtener listados de materiales y repuestos (y sus cantidades) y pasarselos al save del Form.
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
        context['titulo'] = "Modificar Orden de trabajo"
        return context

class OrdenTrabajoDeleteView(DeleteView):

    model = OrdenDeTrabajo
    success_url = reverse_lazy('listarOrdenes')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
