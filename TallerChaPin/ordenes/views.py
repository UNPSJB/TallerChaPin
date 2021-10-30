from django.urls import reverse_lazy
from django.shortcuts import render
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

    

class PresupuestoUpdateView(UpdateView):

    model = Presupuesto
    form_class = PresupuestoForm
    success_url = reverse_lazy('listarPresupuestos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar presupuesto"
        return context

class PresupuestoDeleteView(DeleteView):

    model = Presupuesto
    success_url = reverse_lazy('listarPresupuestos')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
