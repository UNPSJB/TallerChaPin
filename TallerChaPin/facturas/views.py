from multiprocessing import context, get_context
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from wkhtmltopdf.views import PDFTemplateView
from datetime import date
from .models import *
from .forms import * 
from django.urls import reverse_lazy
from django.contrib import messages
from TallerChaPin.utils import ListFilterView

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

# ----------------------------- Factura View ----------------------------------- #

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
        context['facturaPagoForm'] = PagoForm(initial={'monto': kwargs['object'].saldo()})

        return context

    def post(self, *args, **kwargs):
        form = PagoForm(self.request.POST)
        print(form.is_valid(), form.errors)
        if form.is_valid():
            form.save()
            return redirect('listarPagos')
        else:
            messages.add_message(self.request, messages.WARNING,
                             'Algo esta mal que no esta bien.')
            return redirect ('listarFacturas')



def crearFactura(request, pk):
    orden = OrdenDeTrabajo.objects.get(pk=pk)
    if orden.estado == OrdenDeTrabajo.REALIZADA:
        factura = Factura.facturar_orden(orden)
        messages.add_message(request, messages.SUCCESS, 'Factura Creada')
        return redirect ('detallesFactura', factura.pk)
    if orden.estado == OrdenDeTrabajo.FACTURADA:
        messages.add_message(request, messages.WARNING, 'La orden ya ha sido facturada')
        return redirect ('detallesOrden', orden.pk)
    messages.add_message(request, messages.WARNING, 'La orden de trabajo no esta terminada')
    return redirect ('detallesOrden', orden.pk)

class FacturaUpdateView(UpdateView):

    model = Factura
    form_class = FacturaForm
    success_url = reverse_lazy('listarFacturas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class FacturaDeleteView(DeleteView):

    model = Factura
    success_url = reverse_lazy('listarFacturas')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

class ImprimirFactura(PDFTemplateView):
 
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
        self.filename = factura.orden.cliente.nombre + '-' + factura.orden.cliente.apellido + '-'+ str(date.today()) + '.pdf' # definimos el nombre del pdf con datos del cliente.
        context["factura"] = factura # pasamos el objeto presupuesto para usarlo en el template.
        context["styles"] = 'http://127.0.0.1:8000/static/ordenes/css/presupuesto_pdf.css'
        context["logo"] = 'http://127.0.0.1:8000/static/images/chapin2.png'
        return context
        
# ----------------------------- Pago View ----------------------------------- #

class PagoCreateView(CreateView):

    model = Pago
    form_class = PagoForm
    success_url = reverse_lazy ('listarPagos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Ingresar Monto a Pagar"
        return context
    
    # def get_pago(self):
    #     pk = self.kwargs["pk"] if "pk" in self.kwargs.keys() else None
    #     return Pago.objects.get(pk=pk) if pk is not None else None
    
    # def get_form_class(self):
    #     pago = self.get_pago()

    #     return PagoForm(pago)

    def post(self, *args, **kwargs):
        form_class = self.get_form_class()
        pk = kwargs.get('pk')
        factura = Factura.objects.get(pk=pk)
        form = form_class(self.request.POST)
        if form.is_valid():
            monto = form.cleaned_data.get('monto')
            tipo = form.cleaned_data.get('tipo')
            cuota = form.cleaned_data.get('cuota')
            if monto > factura.total():
                messages.add_message(self.request, messages.WARNING, "El monto ingresado supera el total de la factura")
                return redirect ('detallesFactura', factura.pk)
            else:
                factura.pagar(monto,tipo,cuota)
                messages.add_message(self.request, messages.SUCCESS, "Pago registrado exitosamente")
                return redirect ('listarPagos')
        return self.form_invalid(form=form)

class PagoDetailView(DetailView):

    model = Pago

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "TallerChaPin"
        return context

class PagoUpdateView(UpdateView):

    model = Factura
    form_class = FacturaForm
    success_url = reverse_lazy('crearFactura')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PagoListView(ListFilterView):
    filtros = PagoFiltrosForm
    model = Pago
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de pagos"
        return context
