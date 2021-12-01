from django import forms
from django.forms import widgets
from .models import *
from taller.models import TipoMaterial
from django.db.models.query import QuerySet
from django.db.models import Q, Model, fields
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div, HTML
from decimal import Decimal
from datetime import datetime


def dict_to_query(filtros_dict):
    filtro = Q()
    for attr, value in filtros_dict.items():
        if not value:
            continue
        if type(value) == str:
            if value.isdigit():
                prev_value = value
                value = int(value)
                filtro &= Q(**{attr: value}) | Q(**
                                                 {f'{attr}__icontains': prev_value})
            else:
                attr = f'{attr}__icontains'
                filtro &= Q(**{attr: value})
        elif isinstance(value, Model) or isinstance(value, int) or isinstance(value, Decimal):
            filtro &= Q(**{attr: value})
    return filtro


class FiltrosForm(forms.Form):
    ORDEN_CHOICES = []
    orden = forms.CharField(required=False)

    def filter(self, qs, filters):
        return qs.filter(dict_to_query(filters))  # aplicamos filtros

    def sort(self, qs, ordering):
        for o in ordering.split(','):
            qs = qs.order_by(o)  # aplicamos ordenamiento
        return qs

    def apply(self, qs):
        if self.is_valid():
            cleaned_data = self.cleaned_data
            ordering = cleaned_data.pop("orden", None)
            if len(cleaned_data) > 0:
                qs = self.filter(qs, cleaned_data)
            if ordering:
                qs = self.sort(qs, ordering)
        return qs

    def sortables(self):
        return self.ORDEN_CHOICES

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
        ("fecha", "Fecha"),
        ("orden", "Orden"),
        ("cliente", "Cliente"),
        ("vehiculo", "Vehículo"),

    ]
    # fecha = forms.DateTimeInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local', 'readonly': 'readonly'})
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
    fecha = forms.DateField(required=False)
    monto = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    tipo = forms.ModelChoiceField(
        queryset=Pago.objects.all(), required=False, label="Tipo de pago")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<div class="custom-filter"><i class="fas fa-filter"></i> Filtrar</div>'),
                "fecha",
                "monto",
                "tipo",
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )
