from django import forms
from django.db.models import query
from . import models as ordenes
import taller.models as taller 
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
        model = ordenes.Presupuesto
        fields = "__all__"
        exclude = ["orden", "materiales", "repuestos"]

        labels = {

        }
        widgets = {
            "tareas": forms.CheckboxSelectMultiple(),
        }

    def save(self, materiales, repuestos):
        presupuesto = super().save()
        for material in materiales:
            if "material" in material:
                matObj = material["material"]
                matCantidad = material["cantidad"]
                presupuesto.agregar_material(matObj, matCantidad)
        for repuesto in repuestos:
            if "repuesto" in repuesto:
                repObj = repuesto["repuesto"]
                repCantidad = repuesto["cantidad"]
                presupuesto.agregar_repuesto(repObj, repCantidad)
        return presupuesto

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

# Presupuesto - Material


class PresupuestoMaterialForm(forms.ModelForm):
    # Amigabilidad 10/10
    unidad_medida = forms.ChoiceField(required=False,
        choices=taller.TipoMaterial.UNIDADES_BASICAS,
        widget=forms.Select(attrs={'disabled': ''}))

    class Meta:
        model = ordenes.PresupuestoMaterial
        fields = ("material",
                  "cantidad",
                  )

        widgets = {
            'material': forms.Select(attrs={'autocomplete': 'off'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


def PresupuestoMaterialInline(extra=1):
    return inlineformset_factory(
        ordenes.Presupuesto,
        ordenes.PresupuestoMaterial,
        form=PresupuestoMaterialForm,
        extra=extra,
        # max_num=10,
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
        model = ordenes.PresupuestoRepuesto
        fields = ("repuesto",
                  "cantidad")

        widgets = {
            'repuesto': forms.Select(attrs={'autocomplete': 'off'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Guardar'))


def PresupuestoRepuestoInline(extra=1):
    return inlineformset_factory(
        ordenes.Presupuesto,
        ordenes.PresupuestoRepuesto,
        form=PresupuestoRepuestoForm,
        extra=extra,
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
        ("vehiculo", "Vehículo"),
        ("detalles", "Detalles"),
        ("tareas", "Tareas"),
        ("repuestos", "Repuestos"),
        ("materiales", "Materiales")
        # ("validez", "Validez"),

    ]

    cliente = forms.ModelChoiceField(
        queryset=taller.Cliente.objects.all(), required=False)
    vehiculo = forms.ModelChoiceField(
        queryset=taller.Vehiculo.objects.all(), required=False)
    detalles = forms.CharField(required=False, max_length=200)
    tareas = forms.ModelChoiceField(
        queryset=taller.Tarea.objects.all(), required=False)
    materiales = forms.ModelChoiceField(
        queryset=taller.Material.objects.all(), required=False)
    repuestos = forms.ModelChoiceField(
        queryset=taller.Repuesto.objects.all(), required=False)
    # validez = forms.IntegerField(
    #     min_value=0, max_value=settings.CANTIDAD_VALIDEZ_PRESUPUESTO)

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
                # "validez",
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Orden de trabajo - Form


class OrdenForm(forms.ModelForm):

    class Meta:
        model = ordenes.OrdenDeTrabajo
        fields = "__all__"
        exclude = ["egreso", "estado", "ingreso", "materiales", "repuestos"]

        # labels = {

        # }
        widgets = {
            "turno": forms.DateTimeInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local'})
            
        }

    def save(self, tareas, repuestos, materiales):
        orden = super().save()
        for tarea in tareas:
            orden.agregar_tarea(tarea)
        for material in materiales:
            if "material" in material:
                matObj = material["material"]
                matCantidad = material["cantidad"]
                orden.agregar_material(matObj, matCantidad)
        for repuesto in repuestos:
            if "repuesto" in repuesto:
                repObj = repuesto["repuesto"]
                repCantidad = repuesto["cantidad"]
                orden.agregar_repuesto(repObj, repCantidad)
        return orden

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'Guardar'))


class OrdenTrabajoFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("cliente", "Cliente"),
        ("vehiculo", "Vehiculo"),
        ("detalles", "Detalles"),
        ("tareas", "Tareas"),
        ("repuestos", "Repuestos"),
        ("materiales", "Materiales")
    ]

    cliente = forms.ModelChoiceField(
        queryset=taller.Cliente.objects.all(), required=False)
    vehiculo = forms.ModelChoiceField(
        queryset=taller.Vehiculo.objects.all(), required=False)
    detalles = forms.CharField(required=False, max_length=200)
    tareas = forms.ModelChoiceField(
        queryset=taller.Tarea.objects.all(), required=False)
    materiales = forms.ModelChoiceField(
        queryset=taller.Material.objects.all(), required=False)
    repuestos = forms.ModelChoiceField(
        queryset=taller.Repuesto.objects.all(), required=False)

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

            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Registrar Ingreso Vehículo


class RegistrarIngresoVehiculoForm(forms.ModelForm):
    orden = forms.ModelChoiceField(
        queryset = ordenes.OrdenDeTrabajo.objects.all(), 
        required = True,
        widget = forms.Select(),
        label="Orden de trabajo" #TODO: verificar que el layout muestre un label
    )

    class Meta:
        model = ordenes.OrdenDeTrabajo
        fields = "__all__"
        exclude = ["egreso", "estado", "turno", "materiales", "repuestos"]

        widgets = {
            "ingreso": forms.DateTimeInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local'})
        }

    def save(self, commit=True):
        registrarIngresoVehiculo = super().save()
        return registrarIngresoVehiculo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                "orden",
                "ingreso"
            ),
            Div(Submit('submit', 'Guardar'), css_class='filter-btn-container')
        )

# Registrar egreso Vehículo

class RegistrarEgresoVehiculoForm(forms.ModelForm):

    orden = forms.ModelChoiceField(
        queryset = ordenes.OrdenDeTrabajo.objects.all(), 
        required = True,
        widget = forms.Select(),
        label= "Orden de trabajo" #TODO: verificar que el layout muestre un label
    )

    class Meta:
        model = ordenes.OrdenDeTrabajo
        fields = "__all__"
        exclude = ["ingreso", "estado", "turno", "materiales", "repuestos"]

        widgets = {
            "egreso": forms.DateTimeInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local'})
        }

    def save(self, commit=True):
        registrarEgresoVehiculo = super().save()
        return registrarEgresoVehiculo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                "orden",
                "egreso"
            ),
            Div(Submit('submit', 'Guardar'), css_class='filter-btn-container')
        )

# listar turno

class TurnosFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("turno", "Turno"),
        ("cliente", "Cliente"),
        ("vehiculo", "Vehículo"),
        ]

    
    turno = forms.DateTimeField(required=False)
    cliente = forms.ModelChoiceField(
        queryset=taller.Cliente.objects.all(), required=False)
    vehiculo = forms.ModelChoiceField(
        queryset=taller.Vehiculo.objects.all(), required=False)

   
    
    turno__gte = forms.DateTimeField(label="Mayor o igual que", required=False)
    turno__lte = forms.DateTimeField(label="Menor o igual que", required=False)
   
   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<div class="custom-filter"><i class="fas fa-filter"></i> Filtrar</div>'),
                "turno",
                "cliente",
                "vehiculo",
                "turno__gte",
                "turno__lte"
                
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

class AsignarEmpleadoForm(forms.Form):
    empleado = forms.ModelChoiceField(
        queryset=taller.Empleado.objects.all(),
        required=True, 
        label="Asignar tarea a: "
    )

    tarea = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        kwargs['prefix'] = 'asignar'
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'asignarEmpleadoForm'
        self.helper.form_action = 'asignarEmpleado'
        self.helper.layout = Layout(
            Fieldset(
                "", 
                "empleado",
                "tarea"
            )
        )

    def asignar(self):
        empleado = self.cleaned_data.get('empleado')
        detalle_tarea_pk = self.cleaned_data.get('tarea')
        detalle = ordenes.DetalleOrdenDeTrabajo.objects.get(pk = detalle_tarea_pk)
        detalle.asignar(empleado)


class FinalizarTareaForm(forms.Form):
    exitosa = forms.ChoiceField(
        choices=[(1, 'exitosa'), (2, 'no exitosa')], 
        widget=forms.RadioSelect, 
        label="Finalización:")
    observaciones = forms.CharField(
        widget=forms.Textarea(), 
        label='Observaciones:')
    tarea = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        kwargs['prefix'] = 'finalizar'
        kwargs['initial'] = {'exitosa': 1}
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'finalizarTareaForm'
        self.helper.form_action = 'finalizarTarea'
        self.helper.layout = Layout(
            Fieldset(
                "",
                "exitosa",
                "observaciones",
                "tarea"
            )
        )

    def finalizar(self):
        exitosa = self.cleaned_data.get('exitosa')
        exitosa = int(exitosa) == 1
        observaciones = self.cleaned_data.get('observaciones')
        detalle_tarea_pk = self.cleaned_data.get('tarea')
        detalle = ordenes.DetalleOrdenDeTrabajo.objects.get(pk=detalle_tarea_pk)
        detalle.finalizar(exitosa, observaciones)
