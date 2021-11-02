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
        initial_materiales = [
            {'material': pm["material_id"], "cantidad": pm["cantidad"]} for pm in self.get_object().presupuesto_materiales.all().values()]
        initial_repuestos = [
            {'repuesto': pr["repuesto_id"], "cantidad": pr["cantidad"]} for pr in self.get_object().presupuesto_repuestos.all().values()]

        print(f"{initial_materiales=}")
        print(f"{initial_repuestos=}")
        context['presupuesto_material_formset'] = PresupuestoMaterialInline(initial = initial_materiales) #pasarle las lineas previas
        context['presupuesto_material_formset_helper'] = PresupuestoMaterialFormSetHelper()
        context['presupuesto_repuesto_formset'] = PresupuestoRepuestoInline(initial = initial_repuestos) #pasarle las lineas previas
        context['presupuesto_repuesto_formset_helper'] = PresupuestoRepuestoFormSetHelper()
        context['titulo'] = "Modificar presupuesto"
        return context

class PresupuestoDeleteView(DeleteView):

    model = Presupuesto
    success_url = reverse_lazy('listarPresupuestos')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
