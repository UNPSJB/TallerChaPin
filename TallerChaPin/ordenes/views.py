from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import *
from .forms import * 

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
        context['presupuesto_material_formset'] = PresupuestoMaterialInline()
        context['presupuesto_material_formset_helper'] = PresupuestoMaterialFormSetHelper()
        context['presupuesto_repuesto_formset'] = PresupuestoRepuestoInline()
        context['presupuesto_repuesto_formset_helper'] = PresupuestoRepuestoFormSetHelper()
        context['titulo'] = "Registrar Presupuesto"
        return context

    def post(self, *args, **kwargs):
        pmi = PresupuestoMaterialInline(self.request.POST)
        pri = PresupuestoRepuestoInline(self.request.POST)
        form = PresupuestoForm(self.request.POST)
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
        print(self.get_object().presupuesto_materiales.all().values())
        context['presupuesto_material_formset'] = PresupuestoMaterialInline(initial = self.get_object().presupuesto_materiales.all().values()) #pasarle las lineas previas
        context['presupuesto_material_formset_helper'] = PresupuestoMaterialFormSetHelper()
        context['presupuesto_repuesto_formset'] = PresupuestoRepuestoInline(initial = self.get_object().presupuesto_repuestos.all().values()) #pasarle las lineas previas
        context['presupuesto_repuesto_formset_helper'] = PresupuestoRepuestoFormSetHelper()
        context['titulo'] = "Modificar presupuesto"
        return context

class PresupuestoDeleteView(DeleteView):

    model = Presupuesto
    success_url = reverse_lazy('listarPresupuestos')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
