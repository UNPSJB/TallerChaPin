from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from wkhtmltopdf.views import PDFTemplateView
from datetime import date
from .models import *
from .forms import * 
from django.urls import reverse_lazy

# Create your views here.

class imprimirFactura(PDFTemplateView):
    #filename = 'presupuesto_pedro.pdf'
    template_name = 'facturas/factura_pdf.html'
    cmd_options = {
        'margin-top': 3,
        'enable-local-file-access': True,
        'quiet': False
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get('pk')
        factura = Factura.objects.get(pk=pk)
        self.filename = factura.cliente.nombre + '-' + factura.cliente.apellido + '-'+ str(date.today()) + '.pdf' # definimos el nombre del pdf con datos del cliente.
        context["factura"] = factura # pasamos el objeto presupuesto para usarlo en el template.
        context["styles"] = 'http://127.0.0.1:8000/static/ordenes/css/factura_pdf.css' # no esta creado el archivo
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

class FacturaListView(ListFilterView):
    filtros = FacturaFiltrosForm
    model = Factura
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de facturas"
        return context

class FacturaDetailView(DetailView):

    model = Factura

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "TallerChaPin"
        return context

def crearFactura(request, pk):
    orden = OrdenDeTrabajo.objects.get(pk=pk)
    factura = Factura.facturar_orden(orden)
    return redirect ('detallesFactura', factura.pk)

class FacturaUpdateView(UpdateView):

    model = Factura
    form_class = FacturaForm
    success_url = reverse_lazy('listarFacturas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # initial_materiales = [
        #     {'material': pm["material_id"], "cantidad": pm["cantidad"]} for pm in self.get_object().presupuesto_materiales.all().values()]
        # initial_repuestos = [
        #     {'repuesto': pr["repuesto_id"], "cantidad": pr["cantidad"]} for pr in self.get_object().presupuesto_repuestos.all().values()]

        # print(f"{initial_materiales=}")
        # print(f"{initial_repuestos=}")
        # context['presupuesto_material_formset'] = PresupuestoMaterialInline(len(initial_materiales))(initial = initial_materiales) #pasarle las lineas previas
        # context['presupuesto_material_formset_helper'] = PresupuestoMaterialFormSetHelper()
        # context['presupuesto_repuesto_formset'] = PresupuestoRepuestoInline(len(initial_repuestos))(initial = initial_repuestos) #pasarle las lineas previas
        # context['presupuesto_repuesto_formset_helper'] = PresupuestoRepuestoFormSetHelper()
        # context['titulo'] = "Modificar presupuesto"
        return context

class FacturaDeleteView(DeleteView):

    model = Factura
    success_url = reverse_lazy('listarFacturas')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

