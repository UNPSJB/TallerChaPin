from multiprocessing import context, get_context
import os
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
from django.http import Http404
# ----------------------------- Factura View ----------------------------------- #

class FacturaListView(ListFilterView):
    filtros = FacturaFiltrosForm
    model = Factura
    paginate_by = 100  # if pagination is desired
    ordering = ['id']

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

    # Revisar
    # def get(self, *args, **kwargs):
    #     pk = kwargs.get('pk')
    #     try:
    #         factura = Factura.objects.get(pk=pk)
    #     except Factura.DoesNotExist:
    #         raise Http404('Factura no existe')
    #     return render(self.request, 'facturas/factura_detail.html', {'factura': factura})
    
    def post(self, *args, **kwargs):
        form = PagoForm(self.request.POST)
        if form.is_valid():
            form.save()
            return redirect('listarPagos')
        else:
            messages.add_message(self.request, messages.WARNING, form.errors)
            return redirect ('listarFacturas')


#Mejorar
def crearFactura(request, pk):
    try:
        orden = OrdenDeTrabajo.objects.get(pk=pk)
    except OrdenDeTrabajo.DoesNotExist:
        raise Http404("Orden no existe")

    if not orden.puede_facturarse():
        messages.add_message(request, messages.ERROR, "La orden no se puede facturar.")
        return redirect('detallesOrden', orden.pk)
    if orden.puede_facturarse():
        factura = Factura.facturar_orden(orden)
        messages.add_message(request, messages.SUCCESS, 'Factura Creada')
        return redirect ('detallesFactura', factura.pk)

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

class imprimirFactura(PDFTemplateView):
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
        cliente = factura.orden.get_ultimo_presupuesto().cliente

        # definimos el nombre del pdf con datos del cliente.
        self.filename = f'factura {cliente.nombre} {cliente.apellido} ({str(date.today())}).pdf'

        # pasamos el objeto factura para usarlo en el template.
        context["factura"] = factura
        context["styles"] = os.path.abspath("./ordenes/static/ordenes/css/styles_pdf.css")
        context["logo"] = os.path.abspath("./static/images/chapin2.png")
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

    def get(self, *args, **kwargs):
        form = self.get_form()
        pk = kwargs.get('pk')
        try:
            pago = Pago.objects.get(pk=pk)
        except Pago.DoesNotExist:
            raise Http404('Pago no existe')
        return render(self.request, 'facturas/pago_form.html', {'form': form})


    def post(self, *args, **kwargs):
        form_class = self.get_form_class()
        pk = kwargs.get('pk')
        try:
            factura = Factura.objects.get(pk=pk)
        except Factura.DoesNotExist:
            raise Http404("No existe factura")
        form = form_class(self.request.POST)
        if form.is_valid():
            monto = form.cleaned_data.get('monto')
            tipo = form.cleaned_data.get('tipo')
            cuota = form.cleaned_data.get('cuota')

            try:
                factura.pagar(monto,tipo,cuota)
                messages.add_message(self.request, messages.SUCCESS, "Pago registrado exitosamente")
                return redirect ('listarPagos')
            except ValidationError as err:
                messages.add_message(self.request, messages.ERROR, err.message)
                return redirect ('detallesFactura', factura.pk)

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
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de pagos"
        return context
