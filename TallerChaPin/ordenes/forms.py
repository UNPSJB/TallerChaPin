
from django import forms
from django.utils.regex_helper import Choice
from . import models as ordenes
import taller.models as taller
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from django.forms import inlineformset_factory
from TallerChaPin.utils import FiltrosForm


# Presupuesto

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = ordenes.Presupuesto
        fields = "__all__"
        exclude = ["orden", "materiales", "repuestos"]

        labels = {
            "detalles": "Observaciones:"
        }
        widgets = {
            "tareas": forms.SelectMultiple(attrs={'size': '10'}),
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

# Presupuesto - Material - Inlines

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

# Presupuesto - Material - Form Helper

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

# Presupuesto - Repuesto - Inlines

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


# Presupuesto - Repuesto - Form Helper

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
        ("detalles","Observación"),
        ("validez","Validez (días)"),

    ]

    cliente = forms.ModelChoiceField(
        queryset=taller.Cliente.objects.all(), required=False)
    vehiculo = forms.ModelChoiceField(
        queryset=taller.Vehiculo.objects.all(), required=False)
    observacion = forms.CharField(required=False, max_length=200)
    tareas = forms.ModelChoiceField(
        queryset=taller.Tarea.objects.all(), required=False)
    materiales = forms.ModelChoiceField(
        queryset=taller.Material.objects.all(), required=False)
    repuestos = forms.ModelChoiceField(
        queryset=taller.Repuesto.objects.all(), required=False)


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
        ("estado", "Estado")
    ]

    cliente = forms.ModelChoiceField(
        queryset=taller.Cliente.objects.all(), required=False)
    vehiculo = forms.ModelChoiceField(
        queryset=taller.Vehiculo.objects.all(), required=False)
    detalles = forms.CharField(required=False, max_length=200)
    estado = forms.ChoiceField(choices=ordenes.OrdenDeTrabajo.ESTADOS_CHOICES, required=False)
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
                "estado",
                "tareas",
                "materiales",
                "repuestos",

            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Registrar Ingreso de Vehículo

class RegistrarIngresoVehiculoForm(forms.ModelForm):
    orden = forms.ModelChoiceField(
        queryset=ordenes.OrdenDeTrabajo.objects.all(),
        required=True,
        widget=forms.Select(),
        label="Orden de trabajo"  # TODO: verificar que el layout muestre un label
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

# Registrar egreso de Vehículo


class RegistrarEgresoVehiculoForm(forms.ModelForm):

    orden = forms.ModelChoiceField(
        queryset=ordenes.OrdenDeTrabajo.objects.all(),
        required=True,
        widget=forms.Select(),
        label="Orden de trabajo"  # TODO: verificar que el layout muestre un label
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

# Listar Turno

class TurnosFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("turno", "Turno"),
        ("cliente", "Cliente"),
        ("vehiculo", "Vehiculo"),
    ]

    cliente = forms.ModelChoiceField(
        queryset=taller.Cliente.objects.all(), required=False)
    vehiculo = forms.ModelChoiceField(
        queryset=taller.Vehiculo.objects.all(), required=False)

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
                "cliente",
                "vehiculo",
                "fecha__lte",
                "fecha__gte"

            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Asignar Tarea a Empleado

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
        detalle = ordenes.DetalleOrdenDeTrabajo.objects.get(
            pk=detalle_tarea_pk)
        detalle.asignar(empleado)

# Finalizar Tarea

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
                "tarea",
            )
        )

    def finalizar(self):
        exitosa = self.cleaned_data.get('exitosa')
        exitosa = int(exitosa) == 1
        observaciones = self.cleaned_data.get('observaciones')
        detalle_tarea_pk = self.cleaned_data.get('tarea')
        detalle = ordenes.DetalleOrdenDeTrabajo.objects.get(
            pk=detalle_tarea_pk)
        detalle.finalizar(exitosa, observaciones)

# Asignar Cantidad

class AsignarCantidadForm(forms.Form):

    material = forms.ModelChoiceField(
        queryset=taller.Material.objects.all(),
        required=False,
        label="Material"
    )
    cantidad_material = forms.IntegerField(
        required=False,
        label="Cantidad utilizada",
    )

    repuesto = forms.ModelChoiceField(
        queryset=taller.Repuesto.objects.all(),
        required=False,
        label="Repuesto"
    )
    cantidad_repuesto = tarea = forms.IntegerField(
        required=False,
        label="Cantidad utilizada"
    )

    tarea = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        kwargs['prefix'] = 'cantidad'
        kwargs['initial'] = {'cantidad_material': 0, 'cantidad_repuesto': 0}
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'cantidadForm'
        self.helper.form_action = 'asignarCantidad'
        self.helper.layout = Layout(
            Fieldset(
                "",
                "material",
                "cantidad_material",
                HTML('<hr>'),
                "repuesto",
                "cantidad_repuesto",
                "tarea"
            )
        )

    def actualizar_cantidad(self):
        material = self.cleaned_data.get('material')
        cantidad_material = self.cleaned_data.get('cantidad_material')

        repuesto = self.cleaned_data.get('repuesto')
        cantidad_repuesto = self.cleaned_data.get('cantidad_repuesto')

        detalle_tarea_pk = self.cleaned_data.get('tarea')
        detalle = ordenes.DetalleOrdenDeTrabajo.objects.get(
            pk=detalle_tarea_pk)
        detalle.actualizar_cantidad(
            material, cantidad_material, repuesto, cantidad_repuesto)


# Planilla de pintura

class PlanillaDePinturaForm (forms.ModelForm):

    class Meta:
        model = ordenes.PlanillaDePintura
        fields = "__all__"
        exclude = ["orden","fecha"]

        # labels = {

        # }
        # widgets = {
                        
        # }

    def save(self, detalle_planilla, detalle_orden):
        planilla = super().save(commit=False)
        planilla.orden = detalle_orden
        planilla.save()
        for detalle in detalle_planilla:
            cantidadDetalle = detalle["cantidad"]
            formulaDetalle = detalle["formula"]
            planilla.agregar(formulaDetalle, cantidadDetalle)
        return planilla

    def __init__(self, *args, **kwargs):
        if "detalle" in kwargs:
            detalle = kwargs.pop('detalle')
            kwargs['initial']['nombre_de_color']= detalle.color_de_pintura()
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

# Detalles de la Planilla de Pintura

class DetallePlanillaForm(forms.ModelForm):

    class Meta:
        model = ordenes.DetallePlanillaDePintura
        fields = ("formula",
                  "cantidad",
                  )
        # widgets = {
            
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

# Detalle Planilla - Inline

def DetallePlanillaInline(extra=1):
    return inlineformset_factory(
        ordenes.PlanillaDePintura,
        ordenes.DetallePlanillaDePintura,
        form=DetallePlanillaForm,
        extra=extra,
        # max_num=10,
        # fk_name=None,
        # fields=None, exclude=None, can_order=False,
        # can_delete=True, max_num=None, formfield_callback=None,
        # widgets=None, validate_max=False, localized_fields=None,
        # labels=None, help_texts=None, error_messages=None,
        # min_num=None, validate_min=False, field_classes=None
    )

# Detalle Planilla - Form Helper

class DetallePlanillaFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_tag = False
        self.template = 'bootstrap5/table_inline_formset.html'
        self.layout = Layout(
            'formula',
            'cantidad'
        )
        self.render_required_fields = True
