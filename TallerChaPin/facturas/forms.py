from email.policy import default
from django import forms
from django.forms import ChoiceField
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from datetime import datetime
from TallerChaPin.utils import FiltrosForm
from taller.models import (
    Cliente,
    Vehiculo,
)

# Factura - Form

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = "__all__"
        exclude = ["orden"]

        labels = {

        }
        widgets = {
            "fecha": forms.DateTimeInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local', 'readonly': 'readonly'})
        }

    def save(self):
        factura = super().save()
        return factura

    def __init__(self, *args, **kwargs):
        kwargs.update(
            initial={'fecha': datetime.now().strftime('%Y-%m-%dT%H:%M')})
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


# Factura - Filtro

class FacturaFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("pk","#"),
        ("fecha", "Fecha"),
        ("get_cliente_orden", "Cliente"),
        ("get_vehiculo_orden", "Vehículo"),
        ("get_estado", "Estado")
    ]
    orden = forms.ModelChoiceField(
        queryset=OrdenDeTrabajo.objects.all().order_by('id'), required=False, label="Orden de Trabajo")
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(), required=False)
    vehiculo = forms.ModelChoiceField(
        queryset=Vehiculo.objects.all(), required=False)
    estado_choices = [('','-'*9)] + list(Factura.ESTADO_CHOICES)    
    estado = ChoiceField(choices=estado_choices, label="Estado de factura" ,required=False)

    fecha__lte = forms.DateTimeField(label="Hasta", required=False, widget=forms.DateInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local'}))
    fecha__gte= forms.DateTimeField(label="Desde", required=False, widget=forms.DateInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<div class="custom-filter"><i class="fas fa-filter"></i> Filtrar</div>'),
                "orden",
                "estado",
                HTML(
                    '<label> <b>Fecha de factura:</b> </label>'
                    ),
                "fecha__gte",
                "fecha__lte",
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Pago - Form
class PagoForm(forms.ModelForm):

    cuota = forms.ChoiceField(required=False,
                                    choices=((1,1),(3,3),(6,6),(12,12)),
                                    widget=forms.Select(attrs={'disabled': '','id':'select_cuota'})
                                    )

    class Meta:
        model = Pago
        fields = "__all__"
        exclude = ["factura"]

        labels = {
        
        }
        widgets = {
            "fecha": forms.DateTimeInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local', 'readonly': 'readonly'}),
        }

    def save(self, commit=True):
        pago = super().save()
        return pago

    def __init__(self, *args, **kwargs):
        initial = {'fecha': datetime.now().strftime('%Y-%m-%dT%H:%M')}
        if 'initial' in kwargs:
            initial.update(**kwargs['initial'])

        kwargs.update(initial=initial)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'facturaPagoForm'
        self.helper.form_action = 'crearPago'

# Pago - Filtros

class PagoFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("cliente", "Cliente"),
        ("get_nombre_factura","Factura"),
        ("fecha", "Fecha"),
        ("monto", "Monto"),
        ("get_tipo", "Tipo"),
        ("get_cuotas", "Nro. de Coutas")
    ]
  
    monto = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    tipo_choices = [('','-'*9)] + list(Pago.TIPO_PAGO)
    tipo = forms.ChoiceField(choices=tipo_choices, required=False, label="Tipo de pago")
    fecha__lte = forms.DateTimeField(label="Hasta", required=False, widget=forms.DateInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local'}))
    fecha__gte= forms.DateTimeField(label="Desde", required=False, widget=forms.DateInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<div class="custom-filter"><i class="fas fa-filter"></i> Filtrar</div>'),
                "monto",
                "tipo",
                HTML(
                    '<label> <b>Fecha de pago:</b> </label>'
                    ),
                "fecha__gte",
                "fecha__lte",
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )
