from email.policy import default
from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from datetime import datetime
from TallerChaPin.utils import FiltrosForm


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
        ("#","#"),
        ("fecha", "Fecha"),
        ("cliente", "Cliente"),
        ("vehiculo", "Vehículo"),
        ("estado", "Estado")
    ]
    orden = forms.ModelChoiceField(
        queryset=OrdenDeTrabajo.objects.all().order_by('id'), required=False, label="Orden de Trabajo")
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(), required=False)
    vehiculo = forms.ModelChoiceField(
        queryset=Vehiculo.objects.all(), required=False)

    fecha__gte = forms.DateField(label="Hasta", required=False, widget=forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}))
    fecha__lte = forms.DateField(label="Desde", required=False, widget=forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}))

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
                "fecha__lte",
                "fecha__gte",
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
        ("factura","Factura"),
        ("fecha", "Fecha"),
        ("monto", "Monto"),
        ("tipo", "Tipo"),
    ]
  
    monto = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    tipo = forms.ChoiceField(choices=Pago.TIPO_PAGO, required=False, label="Tipo de pago")

    # fecha__gte = forms.DateField(label="Hasta", required=False, widget=forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}))
    # fecha__lte = forms.DateField(label="Desde", required=False, widget=forms.DateInput(format=('%d/%m/%Y'), attrs={'type': 'date'}))


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
                # "fecha__lte",
                # "fecha__gte",
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )
