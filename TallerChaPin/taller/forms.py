from audioop import reverse
from urllib.parse import urlencode
from django import forms
from django.contrib.auth.models import Group
from .models import Cliente, Empleado, Marca, Modelo, Repuesto, Tarea, TipoTarea, Vehiculo
from .models import Empleado, Marca, Material, Modelo, TipoMaterial
from .models import Marca
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from TallerChaPin.utils import FiltrosForm


# Marca Forms
def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    '''Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    '''
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url

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

        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<hr/>'),
                "nombre",
                "descripcion",

            ),
            Div(HTML(
                '<input name="continuar" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar"/>'),
            HTML(
                '<input name="guardar" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )

    # TODO: implementar clean() para sanitización de datos y verificacion de errores.


class MarcaFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("descripcion", "Descripcion"),
    ]
    ATTR_CHOICES = [
        ("nombre", "Nombre"),
        ("descripcion", "Descripcion"),
    ]

    nombre = forms.CharField(required=False, label='Nombre', max_length=100)
    descripcion = forms.CharField(required=False)

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
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<hr/>'),
                "nombre",
                "descripcion",
                "marca",
                "anio",

            ),
            Div(HTML(
                '<input name="continuar" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar"/>'),
            HTML(
                '<input name="guardar" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )


class ModeloFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("descripcion", "Descripcion"),
        ("marca", "Marca"),
        ("anio", "Año")
    ]
    ATTR_CHOICES = [
        ("nombre", "Nombre"),
        ("descripcion", "Descripcion"),
        ("marca", "Marca"),
        ("anio", "Año"),
    ]

    nombre = forms.CharField(required=False, label='Nombre', max_length=100)
    marca = forms.ModelChoiceField(
        queryset=Marca.objects.all().order_by('nombre'), required=False)
    
    anio__gte = forms.IntegerField(
        label="Mayor o igual que", required=False)
    anio__lte = forms.IntegerField(
        label="Menor o igual que", required=False)

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
                "marca",
                HTML("<label><b>Año:</b></label>"),
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
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<hr/>'),
                "nombre",
                "modelo",
                "tipo",
                "cantidad",
                "precio",
            ),
            Div(HTML(
                '<input name="continuar" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar"/>'),
            HTML(
                '<input name="guardar" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))

        )


class RepuestoFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("modelo", "Modelo"),
        ("tipo", "Tipo"),
        ("cantidad", "Cantidad"),
        ("precio", "Precio"),
    ]
    ATTR_CHOICES = [
        ("nombre", "Nombre"),
        ("modelo", "Modelo"),
        ("get_tipo", "Tipo"),
        ("cantidad", "Cantidad"),
        ("precio", "Precio"),
    ]


    nombre = forms.CharField(required=False, label='Nombre', max_length=50)
    modelo = forms.ModelChoiceField(
        queryset=Modelo.objects.all(), required=False, label='Modelo')


    tipo_choices = [('','-'*9)] + list(Repuesto.TIPOS)

    tipo = forms.ChoiceField(choices=tipo_choices,
                             required=False, 
                             label='Tipo')
   

    precio__gte = forms.DecimalField(label="Mayor o igual que", required=False)
    precio__lte = forms.DecimalField(label="Menor o igual que", required=False)

    cantidad__gte = forms.IntegerField(
        label="Mayor o igual que", required=False)
    cantidad__lte = forms.IntegerField(
        label="Menor o igual que", required=False)

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
                HTML("<label><b>Precio:</b></label>"),
                "precio__gte",
                "precio__lte",
                HTML("<label><b>Cantidad</b></label>"),
                "cantidad__gte",
                "cantidad__lte"
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Tipo de Material

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
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<hr/>'),
                "nombre",
                "unidad_medida",

            ),
            Div(HTML(
                '<input name="continuar" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar"/>'),
            HTML(
                '<input name="guardar" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )

# Tipo de Material - Filtro

class TipoMaterialFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("unidad_medida", "Unidad de medida")
    ]

    ATTR_CHOICES = [
        ("nombre", "Nombre"),
        ("get_unidad_medida", "Unidad de medida")
    ]

    nombre = forms.CharField(required=False, label='Nombre', max_length=50)

    tipo_choices = [('','-'*9)] + list(TipoMaterial.UNIDADES_BASICAS)
    unidad_medida = forms.ChoiceField(
        choices=tipo_choices,
        required=False,
        label="Unidades de medida"
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
                "unidad_medida",
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Material

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
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<hr/>'),
                "nombre",
                "tipo",
                "cantidad",
                "precio",

            ),
            Div(HTML(
                '<input name="continuar" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar"/>'),
            HTML(
                '<input name="guardar" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))

        )


# Material - Filtro

class MaterialFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("tipo", "Tipo"),
        ("cantidad", "Cantidad"),
        ("precio", "Precio"),
    ]
    ATTR_CHOICES = [
        ("nombre", "Nombre"),
        ("tipo", "Tipo"),
        ("cantidad", "Cantidad"),
        ("precio", "Precio"),
    ]

    nombre = forms.CharField(required=False, label='Nombre', max_length=100)
    descripcion = forms.CharField(required=False)
    cantidad = forms.DecimalField(required=False)

    tipo = forms.ModelChoiceField(
        queryset=TipoMaterial.objects.all().order_by('nombre'), required=False)

    precio__gte = forms.DecimalField(label="Mayor o igual que", required=False)
    precio__lte = forms.DecimalField(label="Menor o igual que", required=False)


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
                "tipo",
                "descripcion",
                HTML('<label><b>Precio:</b></label>'),
                "precio__gte",
                "precio__lte"

            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Modificar - Cantidad

class ModificarCantidadForm(forms.Form):      
    cantidad = forms.IntegerField(min_value=0, max_value=10000, required=True)

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

    def save(self, pk):
        material = Material.objects.get(pk=pk)
        cantidad = self.cleaned_data.get('cantidad')
        material.cantidad = cantidad
        material.save()

    

    # def asignar_cantidad(self):
    #     cantidad = self.cleaned_data.get('cantidad')
    #     material_pk = self.cleaned_data.get('material')


# Tipo de Tarea


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
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<hr/>'),
                "nombre",
                "descripcion",
                "materiales",
                "repuestos",
                "planilla",
            ),
            Div(HTML(
                '<input type="submit" class="btn btn-primary mt-3" name= "accion" value="Guardar y continuar registrando"/>')),
            Div(HTML(
                '<input type="submit" class="btn btn-primary mt-3" name= "accion" value="Guardar y salir"/>'))
        )


# Tipo de Tarea - Filtro

class TipoTareaFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("descripcion", "Descripción"),
        ("materiales", "Materiales?"),
        ("repuestos", "Repuestos?"),
        ("planilla", "Planilla?"),
    ]

    ATTR_CHOICES = [
        ("nombre", "Nombre"),
        ("descripcion", "Descripción"),
        ("get_req_materiales", "Materiales"),
        ("get_req_repuestos", "Repuestos"),
        ("get_req_planilla", "Planilla"),
    ]

    nombre = forms.CharField(required=False, label='Nombre', max_length=100)
    materiales = forms.BooleanField(required=False)
    repuestos = forms.BooleanField(required=False)
    planilla = forms.BooleanField(required=False)


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
                "materiales",
                "repuestos",
                "planilla",
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Tarea


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

        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<hr/>'),
                "nombre",
                "descripcion",
                "tipo",
                "precio",
            ),
            Div(HTML(
                '<input name="continuar" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar"/>'),
            HTML(
                '<input name="guardar" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))

        )

# Tarea - Filtro


class TareaFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("descripcion", "Descripcion"),
        ("tipo", "Tipo"),
        ("precio", "Precio")
    ]
    
    ATTR_CHOICES = [
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
                HTML(
                    '<label> <b>Precio:</b> </label>'
                    ),
                "precio__gte",
                "precio__lte"
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )


# Empleado

class EmpleadoForm(forms.ModelForm):

    class Meta:
        model = Empleado
        # opcionalmente '__all__' en lugar de la lista.
        fields = '__all__'
        exclude = ["usuario", "tareas"]
        

        widgets = {
            "cuil": forms.TextInput(attrs={'pattern': '(\d{2}-\d{8}-\d{1})', 'placeholder': '##-########-#'})
        }

    def save(self, is_new_instance=False, commit=True):
        empleado = super().save(commit=False)
        if is_new_instance:
            empleado.crear_usuario()
            empleado.añadir_grupos(grupos=self.cleaned_data['grupos'])
        else:
            empleado.usuario.groups.clear() #Ver por que entra aca
            empleado.usuario.groups.add(*self.cleaned_data['grupos'])
        if commit:
            empleado.save()
            empleado.usuario.save()
        return empleado


    grupos = forms.ModelMultipleChoiceField(
                         queryset= Group.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<hr/>'),
                "nombre",
                "apellido",
                "cuil",
                "legajo",
                "grupos",
            ),
            Div(HTML(
                '<input name="continuar" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar"/>'),
            HTML(
                '<input name="guardar" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )
    # TODO: implementar clean() para sanitización de datos y verificacion de errores.


# Empleado - Filtro

class EmpleadoFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("nombre", "Nombre"),
        ("apellido", "Apellido"),
        ("legajo", "Legajo"),
        ("cuil", "CUIL"),
    ]

    ATTR_CHOICES = [
        ("nombre", "Nombre"),
        ("apellido", "Apellido"),
        ("legajo", "Legajo"),
        ("cuil", "CUIL"),
        ("usuario","Usuario"),
        ("get_grupos","Grupos"),
        ("get_tareas","Tareas que realiza")
    ]
    nombre = forms.CharField(required=False, label='Nombre', max_length=100)
    apellido = forms.CharField(
        required=False, label='Apellido', max_length=100)
    legajo = forms.IntegerField(required=False)
    cuil = forms.IntegerField(required=False)

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
                "cuil",
            ),
            
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

class TareaEmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado

        fields = ['tareas']
        labels = {
           'tareas': 'Tipos de tareas'
        }
        widgets = {
            "tareas": forms.CheckboxSelectMultiple(attrs={'class': 'checks_tareas'}),
        }

# Cliente


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = "__all__"

        widgets = {
            "dni": forms.TextInput(attrs={'pattern': '(\d{7}|\d{8})', 'placeholder': '########'}),
        }

    def save(self, commit=True):
        cliente = super().save()
        return cliente

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_tag = False
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
                    '<hr/> <h3> Datos del vehículo: </h3>'),
                "patente",
                "modelo",
                "chasis",
                "anio"
            ),
            Div(HTML(
                '<input name="continuar" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar registrando"/>'),
            HTML(
                '<input name="guardar" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )
class ClienteUpdateForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = "__all__"

        widgets = {
            "dni": forms.TextInput(attrs={'pattern': '(\d{7}|\d{8})', 'placeholder': 'Sin puntos'})
        }

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
            ),
            Div(HTML(
                '<input href="{% url "modificarCliente" object.pk %}" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar registrando"/>')),
            Div(HTML(
                '<input href="{% url "listarClientes" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )

# Cliente - Filtro

class ClienteFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("dni", "DNI"),
        ("nombre", "Nombre"),
        ("apellido", "Apellido"),
        ("direccion", "Dirección"),
        ("telefono", "Teléfono"),
        ("vehiculos", "Vehículo"),
    ]

    ATTR_CHOICES = [
        ("dni", "DNI"),
        ("nombre", "Nombre"),
        ("apellido", "Apellido"),
        ("direccion", "Dirección"),
        ("telefono", "Teléfono"),
        ("vehiculos", "Vehículo"),
        ("vip","Es Vip"),
    ]

    dni = forms.CharField (required=False, max_length=8)
    nombre = forms.CharField(required=False, label='Nombre', max_length=100)
    apellido = forms.CharField(
        required=False, label='Apellido', max_length=100)
    direccion = forms.CharField(required=False, max_length=100)
    vehiculos__modelo = forms.ModelChoiceField(
        queryset=Modelo.objects.all(), required=False, label='Modelo vehículo')
    telefono = forms.CharField(required=False)

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
                Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
            ),

        )

# Vehiculo Forms


class ClienteVehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        fields = "__all__"
        exclude = ["cliente"]

        widgets = {
            "patente": forms.TextInput(attrs={'pattern': '([A-Z]{2}\d{3}[A-Z]{2}|[A-Z]{3}\d{3})', 'placeholder': 'AA###AA o AAA###'})
        }

        labels = {
            "anio": 'Año'
        }


ClienteForm.base_fields.update(ClienteVehiculoForm.base_fields)


class VehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        fields = "__all__"

        widgets = {
            "patente": forms.TextInput(attrs={'pattern': '([A-Z]{2}\d{3}[A-Z]{2}|[A-Z]{3}\d{3})', 'placeholder': 'AA###AA o AAA###'})
        }
        labels = {
            "anio": 'Año'
        }

    def save(self, commit=True):
        vehiculo = super().save()
        return vehiculo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<hr/>'),
                "cliente",
                "patente",
                "modelo",
                "chasis",
                "anio"
            ),
            Div(HTML(
                '<input name="continuar" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar registrando"/>'),
            HTML(
                '<input name="guardar" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )


class VehiculoFiltrosForm(FiltrosForm):
    ORDEN_CHOICES = [
        ("patente", "Patente"),
        ("modelo", "Modelo"),
        ("anio", "Año"),
        ("cliente", "Cliente"),
        ("chasis", "Chasis"),
    ]

    ATTR_CHOICES = [
        ("patente", "Patente"),
        ("modelo", "Modelo"),
        ("anio", "Año"),
        ("cliente", "Cliente"),
        ("chasis", "Chasis"),
    ]


    patente = forms.CharField(required=False, label='Patente', max_length=100)
    modelo = forms.ModelChoiceField(
        queryset=Modelo.objects.all().order_by('nombre'), required=False)
    chasis = forms.CharField(required=False)

    anio__gte = forms.IntegerField(label="Mayor o igual que", required=False)
    anio__lte = forms.IntegerField(label="Menor o igual que", required=False)

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
                HTML(
                    '<label> <b>Año:</b> </label>'
                ),
                "anio__gte",
                "anio__lte",
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )
