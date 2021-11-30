from django import forms
from django.forms import widgets
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Cliente, Empleado, Marca, Modelo, Repuesto, Tarea, TipoTarea, Vehiculo
from .models import Empleado, Marca, Material, Modelo, TipoMaterial
from django.db.models.query import QuerySet
from django.db.models import Q, Model
from .models import Marca
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div, HTML
from decimal import Decimal

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

# Marca Forms


class MarcaForm(forms.ModelForm):

    class Meta:
        model = Marca
        # opcionalmente '__all__' en lugar de la lista.
        fields = ['nombre', 'descripcion']
        exclude = []  # añadir campos a excluir

        # labels = {
        #     'nombre': 'Nombre',
        #     'descripcion': 'Descripción',
        # }

        # widgets = {
        #     'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        #     'descripcion': forms.Textarea(attrs={'class': 'form-control', 'cols': 30, 'rows': 3})
        # }

        # similar a labels y widgets, se pueden definir los diccionarios 'help_texts' y
        # 'error_messages' para mostrar en cada campo que queramos.

    def save(self, commit=True):
        marca = super().save()
        # cambiar a .save(commit=False) si queremos hacer procesamiento extra antes de guardar,
        # por ej. en el caso de Cliente para asociarle un Vehículo antes de guardarlo en la db.
        return marca

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Guardar'))

    # TODO: implementar clean() para sanitización de datos y verificacion de errores.


class MarcaFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("descripcion", "Descripcion")
    ]
    
    nombre = forms.CharField(required=False, label='Nombre', max_length=100)
    descripcion = forms.CharField(required=False)
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
                "nombre",
                "descripcion"
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Modelo Forms

class ModeloForm(forms.ModelForm):
    class Meta:
        model = Modelo
        fields = "__all__"

        labels = {
            'anio': 'Año'
        }

    def save(self, commit=True):
        modelo = super().save()
        return modelo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Guardar'))


class ModeloFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("descripcion", "Descripcion"),
        ("marca", "Marca"),
        ("anio", "Año")
    ]

    nombre = forms.CharField(required=False, label='Nombre', max_length=100)
    descripcion = forms.CharField(required=False)
    marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(), required=False)

    anio__gte = forms.IntegerField(label="Mayor o igual que", required=False)
    anio__lte = forms.IntegerField(label="Menor o igual que", required=False)

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
                "nombre",
                "descripcion",
                "marca",
                HTML("<label>Año </label>"),
                "anio__gte",
                "anio__lte"
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Repuesto Forms


class RepuestoForm(forms.ModelForm):

    class Meta:
        model = Repuesto
        fields = "__all__"

    def save(self, commit=True):
        repuesto = super().save()
        return repuesto

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Guardar'))


class RepuestoFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("modelo", "Modelo"),
        ("tipo", "Tipo"),
        ("cantidad", "Cantidad"),
        ("precio", "Precio"),
    ]
    nombre = forms.CharField(required=False, label='Nombre', max_length=50)
    modelo = forms.ModelChoiceField(
        queryset=Modelo.objects.all(), required=False, label='Modelo')
    
    tipo = forms.ChoiceField(choices=Repuesto.TIPOS, required=False, label='Tipo')
    # TODO: deberían ser campos numéricos
       
    precio__gte = forms.DecimalField(label="Mayor o igual que", required=False)
    precio__lte = forms.DecimalField(label="Menor o igual que", required=False)

    cantidad__gte = forms.IntegerField(label="Mayor o igual que", required=False)
    cantidad__lte = forms.IntegerField(label="Menor o igual que", required=False)

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
                "nombre",
                "modelo",
                "tipo",
                HTML("<label>Precio</label>"),
                "precio__gte",
                "precio__lte",
                HTML("<label>Cantidad</label>"),
                "cantidad__gte",
                "cantidad__lte"
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Material Forms


class MaterialForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = '__all__'

    def save(self, commit=True):
        material = super().save()
        return material

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Guardar'))




class MaterialFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("tipo", "Tipo"),
        ("cantidad", "Cantidad"),
        ("precio", "Precio"),
    ]

    nombre = forms.CharField(required=False, label='Nombre', max_length=100)
    descripcion = forms.CharField(required=False)
    cantidad = forms.DecimalField(required=False)
    precio = forms.DecimalField(required=False)
    #tipo = forms.CharField(required=False)
    
    material__tipo = forms.ModelChoiceField(
        queryset=TipoMaterial.objects.all(), required=False, label='Tipo Material')
    
    orden = forms.CharField(
        required=False
    )

    precio__gte = forms.DecimalField(label="Mayor o igual que", required=False)
    precio__lte = forms.DecimalField(label="Menor o igual que", required=False)

    cantidad__gte = forms.IntegerField(label="Mayor o igual que", required=False)
    cantidad__lte = forms.IntegerField(label="Menor o igual que", required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'

        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<div class="custom-filter"><i class="fas fa-filter"></i> Filtrar</div>'),
                "nombre",
                "material__tipo",
                HTML("<label> Cantidad </label>"),
                "cantidad__gte",
                "cantidad__lte",
                HTML("<label> Precio </label>"),
                "precio__gte",
                "precio__lte",
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

class ModificarCantidadForm(forms.Form):       # TODO VER
    cantidad = forms.IntegerField(min_value=0, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'modificarCantidadForm'
        self.helper.form_action = 'modificarCantidad'
        self.helper.layout = Layout(
            Fieldset(
                "",
                "cantidad"
            )
        )
    
    # def asignar_cantidad(self):
    #     cantidad = self.cleaned_data.get('cantidad')
    #     material_pk = self.cleaned_data.get('material')

# Tipo de Material Forms
class TipoMaterialForm(forms.ModelForm):

        class Meta:
            model = TipoMaterial
            fields = '__all__'
        
        def save(self, commit=True):
            TipoMaterial = super().save()
            return TipoMaterial

        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.helper = FormHelper()
                
                self.helper.add_input(Submit('submit', 'Guardar'))


class TipoMaterialFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("unidad_medida", "Unidad de medida")
    ]

    nombre = forms.CharField(required=False, label='Nombre', max_length=50)
    unidades_medida = forms.ChoiceField(
        choices=TipoMaterial.UNIDADES_BASICAS,
        required=False,
        label="Unidad de medida"
    )

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
                "nombre",
                "unidades_medida",
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )


# Tipo de tarea Forms


class TipoTareaForm(forms.ModelForm):

    class Meta:
        model = TipoTarea
        fields = "__all__"

        labels = {
            'materiales': 'Requiere materiales',
            'repuestos': 'Requiere repuestos',
            'planilla': 'Requiere planilla de pintura'
        }

    def save(self, commit=True):
        tipoTarea = super().save()
        return tipoTarea

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Guardar'))


class TipoTareaFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("descripcion", "Descripción"),
        ("materiales", "Materiales?"),
        ("repuestos", "Repuestos?"),
        ("planilla", "Planilla?"),
    ]

    nombre = forms.CharField(required=False, label='Nombre', max_length=100)

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
                "nombre"
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Tarea Forms


class TareaForm(forms.ModelForm):

    class Meta:
        model = Tarea
        fields = "__all__"

    def save(self, commit=True):
        tarea = super().save()
        return tarea

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Guardar'))

class TareaFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("descripcion", "Descripcion"),
        ("tipo", "Tipo"),
        ("precio", "Precio")
    ]

    nombre = forms.CharField(required=False, label='Nombre', max_length=100)
    descripcion = forms.CharField(required=False)
    tipo = forms.ModelChoiceField(
        queryset=TipoTarea.objects.all(), required=False)
       
    precio__gte = forms.DecimalField(label="Mayor o igual que", required=False)
    precio__lte = forms.DecimalField(label="Menor o igual que", required=False)

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
                "nombre",
                "descripcion",
                "tipo",
                HTML("<label> Precio </label>"),
                "precio__gte",
                "precio__lte"
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )


# Empleado Forms
class EmpleadoForm(forms.ModelForm):

    class Meta:
        model = Empleado
        # opcionalmente '__all__' en lugar de la lista.
        fields = ['nombre', 'apellido', 'cuil', 'legajo']
        exclude = ['usuario']  # añadir campos a excluir

    def save(self, commit=True):
        empleado = super().save()
        # cambiar a .save(commit=False) si queremos hacer procesamiento extra antes de guardar,
        # por ej. en el caso de Cliente para asociarle un Vehículo antes de guardarlo en la db.
        return empleado

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Guardar'))

    # TODO: implementar clean() para sanitización de datos y verificacion de errores.


class EmpleadoFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("apellido", "Apellido"),
        ("legajo", "Legajo"),
        ("cuil", "CUIL"),

    ]
    nombre = forms.CharField(required=False, label='Nombre', max_length=100)
    apellido = forms.CharField(
        required=False, label='Apellido', max_length=100)
    legajo = forms.IntegerField(required=False)
    
    cuil__gte = forms.IntegerField(label="Mayor o igual que", required=False)
    cuil__lte = forms.IntegerField(label="Menor o igual que", required=False)

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
                "nombre",
                "apellido",
                "legajo",
                "cuil__gte",
                "cuil__lte"
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Cliente forms
class ClienteForm(forms.ModelForm):

    # patente = forms.CharField(required=True, label='Patente', max_length=7)
    # modelo = forms.ModelChoiceField(
    # queryset=Modelo.objects.all(), required=True)
    # chasis = forms.CharField(required=True)
    # anio = forms.IntegerField(required=True)

    class Meta:
        model = Cliente
        fields = "__all__"

    def save(self, commit=True):
        cliente = super().save()
        return cliente

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<hr/>'),
                "dni",
                "nombre",
                "apellido",
                "direccion",
                "telefono",
                HTML(
                    '<div> <label class="form-label">Datos del vehículo:</label> <div/> <hr/>' ),
                "patente",
                "modelo",
                "chasis",
                "anio"
            ),
            Div(Submit('submit', 'Guardar'), css_class='submit-btn-container')
        )


class ClienteFiltrosForm(FiltrosForm):  # Revisar
    ORDEN_CHOICES = [
        ("dni", "DNI"),
        ("nombre", "Nombre"),
        ("apellido", "Apellido"),
        ("direccion", "Dirección"),
        ("telefono", "Teléfono"),
        ("vehiculo", "Vehículo"),
    ]
    
    dni = forms.IntegerField(required=False)
    nombre = forms.CharField(required=False, label='Nombre', max_length=100)
    apellido = forms.CharField(
        required=False, label='Apellido', max_length=100)
    direccion = forms.CharField(max_length=100)
    
    vehiculos__modelo = forms.ModelChoiceField(
        queryset=Modelo.objects.all(), required=False, label='Modelo vehículo')
    # vehiculo = forms.ModelChoiceField(
    #     queryset=Vehiculo.objects.all(), required=False)
    telefono = forms.IntegerField(required=False)
    
    dni__gte = forms.IntegerField(label="Mayor o igual que", required=False)
    dni__lte = forms.IntegerField(label="Menor o igual que", required=False)

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
                "dni",
                "nombre",
                "apellido",
                "vehiculos__modelo",
                "dni__gte",
                "dni__lte"
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Vehiculo Forms
class ClienteVehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        fields = "__all__"
        exclude = ["cliente"]

ClienteForm.base_fields.update(ClienteVehiculoForm.base_fields)

class VehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        fields = "__all__"

    def save(self, commit=True):
        vehiculo = super().save()
        return vehiculo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Guardar'))


class VehiculoFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("patente", "Patente"),
        ("modelo", "Modelo"),
        ("anio", "Año"),
        ("cliente", "Cliente"),
        ("chasis", "Chasis"),
    ]

    patente = forms.CharField(required=False, label='Patente', max_length=100)
    modelo = forms.ModelChoiceField(
        queryset=Modelo.objects.all(), required=False)
    chasis = forms.CharField(required=False)

    anio__gte = forms.IntegerField(label="Mayor o igual que", required=False)
    anio__lte = forms.IntegerField(label="Menor o igual que", required=False)

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
                "patente",
                "modelo",
                "chasis",
                "anio__gte",
                "anio__lte"
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )
