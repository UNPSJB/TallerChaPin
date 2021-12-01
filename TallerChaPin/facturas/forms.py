from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from datetime import datetime
from TallerChaPin.utils import FiltrosForm


# Factura Form

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
    ]
    orden = forms.ModelChoiceField(
        queryset=OrdenDeTrabajo.objects.all(), required=False, label="Orden de Trabajo")
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
    class Meta:
        model = Pago
        fields = "__all__"
        exclude = ["factura"]

        labels = {
            
            # "tipo": forms.ModelChoiceField(queryset=Pago.objects.all(), label="Pagar al/con:")
        }
        widgets = {
            "fecha": forms.DateTimeInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local', 'readonly': 'readonly'}),
            
        }

    def save(self):
        pago = super().save()
        return pago

    def __init__(self, *args, **kwargs):
        kwargs.update(
            initial={'fecha': datetime.now().strftime('%Y-%m-%dT%H:%M')})
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'Guardar'))
        

# Pago - Filtros

class PagoFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("fecha", "fecha"),
        ("monto", "monto"),
        ("tipo", "tipo"),
    ]
    monto = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    tipo = forms.ModelChoiceField(
        queryset=Pago.objects.all(), required=False, label="Tipo de pago")

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
                "monto",
                "tipo",
                "fecha__lte",
                "fecha__gte",
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )
