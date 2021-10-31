from django import forms
from .models import *
from django.db.models.query import QuerySet
from django.db.models import Q, Model, fields
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div, HTML
from decimal import Decimal
from django.conf import settings
from django.forms import inlineformset_factory


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


# Presupuesto

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = "__all__"
        exclude = ["orden", "materiales", "repuestos"]

        labels = {

        }
        widgets = {
            "tareas": forms.CheckboxSelectMultiple(),
        }

    def save(self, commit=True):
        presupuesto = super().save()
        return presupuesto

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

# Presupuesto - Material

class PresupuestoMaterialForm(forms.ModelForm):
    class Meta:
        model = PresupuestoMaterial
        fields = ("material",
                  "cantidad")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        


PresupuestoMaterialInline = inlineformset_factory(
    Presupuesto,
    PresupuestoMaterial,
    form=PresupuestoMaterialForm,
    extra=1,
    # max_num=5,
    # fk_name=None,
    # fields=None, exclude=None, can_order=False,
    # can_delete=True, max_num=None, formfield_callback=None,
    # widgets=None, validate_max=False, localized_fields=None,
    # labels=None, help_texts=None, error_messages=None,
    # min_num=None, validate_min=False, field_classes=None
)

class PresupuestoMaterialFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_tag = False
        self.template = 'bootstrap5/table_inline_formset.html'
        self.layout = Layout(
            'material',
            'cantidad'
        )
        self.render_required_fields = True
       
# Presupuesto - Repuesto

class PresupuestoRepuestoForm(forms.ModelForm):
    class Meta:
        model = PresupuestoRepuesto
        fields = ("repuesto",
                  "cantidad")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Guardar'))


PresupuestoRepuestoInline = inlineformset_factory(
    Presupuesto,
    PresupuestoRepuesto,
    form=PresupuestoRepuestoForm,
    extra=1,
    # max_num=5,
    # fk_name=None,
    # fields=None, exclude=None, can_order=False,
    # can_delete=True, max_num=None, formfield_callback=None,
    # widgets=None, validate_max=False, localized_fields=None,
    # labels=None, help_texts=None, error_messages=None,
    # min_num=None, validate_min=False, field_classes=None
)


class PresupuestoRepuestoFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_tag = False
        self.template = 'bootstrap5/table_inline_formset.html'
        self.layout = Layout(
            'repuesto',
            'cantidad'
        )
        self.render_required_fields = True
        self.add_input(Submit('submit', 'Guardar'))

# Presupuesto - Filtro

class PresupuestoFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("cliente", "Cliente"),
        ("vehiculo", "Vehiculo"),
        ("detalles", "Detalles"),
        ("tareas", "Tareas"),
        ("repuestos", "Repuestos"),
        ("materiales", "Materiales"),
        ("validez", "Validez"),

    ]

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(), required=False)
    vehiculo = forms.ModelChoiceField(
        queryset=Vehiculo.objects.all(), required=False)
    detalles = forms.CharField(required=False, max_length=200)
    tareas = forms.ModelChoiceField(
        queryset=Tarea.objects.all(), required=False)
    materiales = forms.ModelChoiceField(
        queryset=Material.objects.all(), required=False)
    repuestos = forms.ModelChoiceField(
        queryset=Repuesto.objects.all(), required=False)
    validez = forms.IntegerField(
        min_value=0, max_value=settings.CANTIDAD_VALIDEZ_PRESUPUESTO)

    orden = forms.CharField(
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<div class="custom-filter"><i class="fas fa-filter"></i> Filtrar</div>'),
                "cliente",
                "vehiculo",
                "detalles",
                "tareas",
                "materiales",
                "repuestos",
                "validez",
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )
