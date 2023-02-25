from django.urls import reverse
from django.utils.http import urlencode
from django import forms
from . import models as ordenes
import taller.models as taller
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from django.forms import BooleanField, inlineformset_factory
from TallerChaPin.utils import FiltrosForm
from datetime import datetime
from .utils import requiere_insumo

def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    '''Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    '''
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url
    
# Presupuesto

def PresupuestoForm(base = None): 
    class PresupuestoForm(forms.ModelForm):
        class Meta:
            model = ordenes.Presupuesto
            fields = "__all__" if base is None else ["detalles", "tareas"]
            exclude = ["orden", "materiales", "repuestos", "ampliado", "confirmado"] if base is None else ["orden", "materiales", "repuestos", "cliente", "vehiculo", "validez", "ampliado", "confirmado"]

            labels = {

            }
            widgets = {
                "tareas": forms.CheckboxSelectMultiple(),
            }

        def save(self, materiales, repuestos, tareas, update=False):
            presupuesto = super().save(commit=False)
            tareas_para_agregar = list(tareas).copy()

            if base is not None:
                presupuesto.cliente = base.cliente
                presupuesto.vehiculo = base.vehiculo
                presupuesto.orden = base.orden
                presupuesto.validez = base.validez
                base.ampliado = True
                base.save()

                # Control realizado para evitar que personas malintencionadas eliminen tareas que no se deben eliminar
                tareas_finalizadas = base.orden.get_tareas_finalizadas()

                for t in tareas_finalizadas:
                    tarea = taller.Tarea.objects.get(pk=t)
                    
                    if tarea not in tareas_para_agregar:
                        tareas_para_agregar.append(tarea)
                #presupuesto.orden.actualizar_estado()

            presupuesto.save()

            if update:
                presupuesto.vaciar()
            
            for tarea in tareas_para_agregar:
                presupuesto.agregar_tarea(tarea)

            if self.requiere("materiales", tareas_para_agregar):
                for material in materiales:
                    if "material" in material and material["material"] is not None and material["cantidad"] is not 0:
                        matObj = material["material"]
                        matCantidad = material["cantidad"]
                        presupuesto.agregar_material(matObj, matCantidad)

            if self.requiere("repuestos", tareas_para_agregar):
                for repuesto in repuestos:
                    if "repuesto" in repuesto and repuesto["repuesto"] is not None and repuesto["cantidad"] is not 0:
                        repObj = repuesto["repuesto"]
                        repCantidad = repuesto["cantidad"]
                        presupuesto.agregar_repuesto(repObj, repCantidad)
            
            return presupuesto

        def requiere(self, insumo, tareas):

            requerimientos = requiere_insumo(tareas)
            
            if insumo not in requerimientos.keys():
                return False

            return requerimientos[insumo]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = False
            if base is not None:
                self.helper.form_action = reverse_querystring('ampliarPresupuesto', args=[base.pk])

    return PresupuestoForm

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
            'material': forms.Select(attrs={'autocomplete': 'off'}),
            'cantidad': forms.NumberInput(attrs={'min': 1})
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
            'repuesto': forms.Select(attrs={'autocomplete': 'off'}),
            'cantidad': forms.TextInput(attrs={'type': 'number', 'min':'0'})
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
        #self.add_input(Submit('submit', 'Guardar'))

# Presupuesto - Filtro

class PresupuestoFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ('fecha', 'Fecha'),
        ("cliente", "Cliente"),
        ("vehiculo", "Vehículo"),
        ("validez","Validez (días)"),
        ("confirmado","Confirmado"),
        ("ampliado","Ampliado")
    ]
    ATTR_CHOICES = [
        ('fecha', 'Fecha'),
        ("cliente", "Cliente"),
        ("vehiculo", "Vehículo"),
        ("validez","Validez (días)"),
        ("get_confirmado","Confirmado"),
        ("get_ampliado","Ampliado") 
    ]

    cliente = forms.ModelChoiceField(
        queryset=taller.Cliente.objects.all().order_by('nombre'), required=False)
    vehiculo = forms.ModelChoiceField(
        queryset=taller.Vehiculo.objects.all().order_by('id'), required=False)
    observacion = forms.CharField(
        required=False, max_length=200)
    tareas = forms.ModelChoiceField(
        queryset=taller.Tarea.objects.all().order_by('nombre'), required=False)
    materiales = forms.ModelChoiceField(
        queryset=taller.Material.objects.all().order_by('id'), required=False)
    repuestos = forms.ModelChoiceField(
        queryset=taller.Repuesto.objects.all().order_by('id'), required=False)
    
    confirmado = BooleanField(required=False)
    ampliado = BooleanField(required=False)

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
                "cliente",
                "vehiculo",
                "tareas",
                "materiales",
                "repuestos",
                "confirmado",
                "ampliado",
                HTML(
                    '<label> <b>Fecha de confirmacion:</b> </label>'
                    ),
                "fecha__gte",
                "fecha__lte",
            ),

            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Orden de trabajo - Form


class OrdenUpdateForm(forms.ModelForm):
    class Meta:
        model = ordenes.OrdenDeTrabajo
        fields = "__all__"
        exclude = ["egreso", "estado", "ingreso", "materiales", "repuestos"]
   
        widgets = {
            "turno": forms.DateTimeInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local', 'min': datetime.strftime(datetime.now(),'%Y-%m-%dT%H:%M')})

        }
    def save(self):
        orden = super().save()
        return orden

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'Guardar'))


class OrdenForm(forms.ModelForm):

    class Meta:
        model = ordenes.OrdenDeTrabajo
        fields = "__all__"
        exclude = ["egreso", "estado", "ingreso", "materiales", "repuestos"]

        widgets = {
            # "turno": forms.DateTimeInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local', 'min': datetime.strftime(datetime.now(),'%Y-%m-%dT%H:%M'), 'value': datetime.strftime(datetime.now(),'%Y-%m-%dT%H:%M')})
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
        self.fields['turno'].widget.attrs['min'] = datetime.now().strftime('%Y-%m-%dT%H:%M')
        self.fields['turno'].widget.attrs['value'] = datetime.now().strftime('%Y-%m-%dT%H:%M')
        self.helper.add_input(Submit('submit', 'Guardar'))


class OrdenTrabajoFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("pk", '#'),
        ("turno", "Fecha"),
        ("presupuestos__cliente", "Cliente"),
        ("presupuestos__vehiculo", "Vehiculo"),
        ("estado", "Estado"),
    ]

    ATTR_CHOICES = [
        ("cliente", "Cliente"),
        ("vehiculo", "Vehiculo"),
        ("get_estado", "Estado"),
    ]

    presupuestos__cliente = forms.ModelChoiceField(
        queryset=taller.Cliente.objects.all(), label="Cliente",required=False)
    presupuestos__vehiculo = forms.ModelChoiceField(
        queryset=taller.Vehiculo.objects.all(), label="Vehiculo", required=False)
    estado_choices = [('','-'*9)] + list(ordenes.OrdenDeTrabajo.ESTADOS_CHOICES)
    estado = forms.ChoiceField(choices=estado_choices, required=False)
    tareas = forms.ModelChoiceField(
        queryset=taller.Tarea.objects.all(), required=False)
    materiales = forms.ModelChoiceField(
        queryset=taller.Material.objects.all(), required=False)
    repuestos = forms.ModelChoiceField(
        queryset=taller.Repuesto.objects.all(), required=False)

    turno__lte= forms.DateTimeField(label="Hasta", required=False, widget=forms.DateInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local'}))
    turno__gte= forms.DateTimeField(label="Desde", required=False, widget=forms.DateInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<div class="custom-filter"><i class="fas fa-filter"></i> Filtrar</div>'),
                "presupuestos__cliente",
                "presupuestos__vehiculo",
                "estado",
                "tareas",
                "materiales",
                "repuestos",
                HTML(
                    '<label> <b>Fecha de Turno:</b> </label>'
                    ),
                "turno__gte",
                "turno__lte",
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )


# Registrar Ingreso de Vehículo
def RegistrarIngresoVehiculoForm(model=None):
    class RegistrarIngresoVehiculoForm(forms.ModelForm):
       
        if model is None:
            orden = forms.ModelChoiceField(
                queryset=ordenes.OrdenDeTrabajo.objects.sin_ingresar(),
                required=True,
                widget=forms.Select(),
                label="Orden de trabajo"  # TODO: verificar que el layout muestre un label
            )

        class Meta:
            model = ordenes.OrdenDeTrabajo
            fields = "__all__"
            exclude = ["egreso", "estado", "turno", "materiales", "repuestos"]

            widgets = {
                # "ingreso": forms.DateTimeInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local', 'min': datetime.strftime(datetime.now(),'%Y-%m-%dT%H:%M'), 'value': datetime.strftime(datetime.now(),'%Y-%m-%dT%H:%M')})
                "ingreso": forms.DateTimeInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local'})
            }

        def save(self, commit=True):
            registrarIngresoVehiculo = super().save(commit=bool(model))
            if model:
                registrarIngresoVehiculo.orden = model
                registrarIngresoVehiculo.save()
            return registrarIngresoVehiculo

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.fields['ingreso'].widget.attrs['min'] = datetime.now().strftime('%Y-%m-%dT%H:%M')
            self.fields['ingreso'].widget.attrs['value'] = datetime.now().strftime('%Y-%m-%dT%H:%M')
            self.helper.layout = Layout(
                Fieldset(
                    "",
                    None if model else "orden",
                    "ingreso",
                ),
                Div(Submit('submit', 'Guardar'), css_class='filter-btn-container')
            )

    return RegistrarIngresoVehiculoForm


# Registrar egreso de Vehículo

def RegistrarEgresoVehiculoForm(model=None):
    class RegistrarEgresoVehiculoForm(forms.ModelForm):

        if model is None:
            orden = forms.ModelChoiceField(
                queryset=ordenes.OrdenDeTrabajo.objects.all(),
                required=True,
                widget=forms.Select(),
                label="Orden de trabajo"
            )

        class Meta:
            model = ordenes.OrdenDeTrabajo
            fields = "__all__"
            exclude = ["ingreso", "estado", "turno", "materiales", "repuestos"]

            widgets = {
                "egreso": forms.DateTimeInput(format=('%d/%m/%Y %H:%M'), attrs={'type': 'datetime-local'})
            }
        def save(self, commit=True):
            registrarEgresoVehiculo = super().save(commit=bool(model))
            if model:
                registrarEgresoVehiculo.orden = model
                registrarEgresoVehiculo.save()
            return registrarEgresoVehiculo

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.fields['egreso'].widget.attrs['min'] = datetime.now().strftime('%Y-%m-%dT%H:%M')
            self.fields['egreso'].widget.attrs['value'] = datetime.now().strftime('%Y-%m-%dT%H:%M')
            self.helper.layout = Layout(
                Fieldset(
                    "",
                    "orden",
                    "egreso"
                ),
                Div(Submit('submit', 'Guardar'), css_class='filter-btn-container')
            )

    return RegistrarEgresoVehiculoForm

# Listar Turno

class TurnosFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("turno", "Turno"),
        ("cliente", "Cliente"),
        ("vehiculo", "Vehiculo"),
    ]

    ATTR_CHOICES = [
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
        label='Observaciones:', 
        required=False)
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

    def save(self, nombre_color, detalle_planilla, detalle_orden=None, update=False, planilla_pintura=None):

        if update:
            planilla_pintura.vaciar()
            planilla = planilla_pintura
        else:
            planilla = super().save(commit=False)
            planilla.orden = detalle_orden
        
        planilla.nombre_de_color = nombre_color
        planilla.save()

        for detalle in detalle_planilla:
            if detalle == {}:
                continue
            cantidadDetalle = detalle["cantidad"]
            formulaDetalle = detalle["formula"]
            planilla.agregar(formulaDetalle, cantidadDetalle)
        return planilla

    def __init__(self, *args, **kwargs):
        if "detalle" in kwargs:
            detalle = kwargs.pop('detalle')
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
