from django import forms
from .models import Cliente, Empleado, Marca, Modelo, Repuesto, Tarea, TipoTarea, Vehiculo
from .models import Empleado, Marca, Material, Modelo, TipoMaterial
from .models import Marca
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML
from TallerChaPin.utils import FiltrosForm


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

        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML(
                    '<hr/>'),
                "nombre",
                "descripcion",

            ),
            Div(HTML(
                '<input href="{% url "crearVehiculo" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar registrando"/>')),
            Div(HTML(
                '<input href="{% url "listarVehiculos" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )

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
                '<input href="{% url "crearVehiculo" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar registrando"/>')),
            Div(HTML(
                '<input href="{% url "listarVehiculos" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )


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
                '<input href="{% url "crearVehiculo" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar registrando"/>')),
            Div(HTML(
                '<input href="{% url "listarVehiculos" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )


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

    tipo = forms.ChoiceField(choices=Repuesto.TIPOS,
                             required=False, label='Tipo')

    precio__gte = forms.DecimalField(label="Mayor o igual que", required=False)
    precio__lte = forms.DecimalField(label="Menor o igual que", required=False)

    cantidad__gte = forms.IntegerField(
        label="Mayor o igual que", required=False)
    cantidad__lte = forms.IntegerField(
        label="Menor o igual que", required=False)

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
                '<input href="{% url "crearVehiculo" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar registrando"/>')),
            Div(HTML(
                '<input href="{% url "listarVehiculos" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )

# Tipo de Material - Filtro


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
                '<input href="{% url "crearVehiculo" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar registrando"/>')),
            Div(HTML(
                '<input href="{% url "listarVehiculos" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )


# Material - Filtro

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

    material__tipo = forms.ModelChoiceField(
        queryset=TipoMaterial.objects.all(), required=False, label='Tipo Material')

    orden = forms.CharField(
        required=False
    )

    precio__gte = forms.DecimalField(
        label="Mayor o igual que:", required=False)
    precio__lte = forms.DecimalField(
        label="Menor o igual que:", required=False)

    cantidad__gte = forms.IntegerField(
        label="Mayor o igual que:", required=False)
    cantidad__lte = forms.IntegerField(
        label="Menor o igual que:", required=False)

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

# Modificar - Cantidad


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
                '<input href="{% url "crearVehiculo" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar registrando"/>')),
            Div(HTML(
                '<input href="{% url "listarVehiculos" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
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
                '<input href="{% url "crearVehiculo" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar registrando"/>')),
            Div(HTML(
                '<input href="{% url "listarVehiculos" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )

# Tarea - Filtro


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


# Empleado

class EmpleadoForm(forms.ModelForm):

    class Meta:
        model = Empleado
        # opcionalmente '__all__' en lugar de la lista.
        fields = ['nombre', 'apellido', 'cuil', 'legajo']
        exclude = ['usuario']  # añadir campos a excluir

        widgets = {
            "cuil": forms.TextInput(attrs={'pattern': '(\d{2}-\d{8}-\d{1})', 'placeholder': '##-########-#'})
        }

    def save(self, commit=True):
        empleado = super().save()
        # cambiar a .save(commit=False) si queremos hacer procesamiento extra antes de guardar,
        # por ej. en el caso de Cliente para asociarle un Vehículo antes de guardarlo en la db.
        return empleado

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
            ),
            Div(HTML(
                '<input href="{% url "crearVehiculo" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar registrando"/>')),
            Div(HTML(
                '<input href="{% url "listarVehiculos" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
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
    nombre = forms.CharField(required=False, label='Nombre', max_length=100)
    apellido = forms.CharField(
        required=False, label='Apellido', max_length=100)
    legajo = forms.IntegerField(required=False)

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
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )

# Cliente


class ClienteForm(forms.ModelForm):

    # patente = forms.CharField(required=True, label='Patente', max_length=7)
    # modelo = forms.ModelChoiceField(
    # queryset=Modelo.objects.all(), required=True)
    # chasis = forms.CharField(required=True)
    # anio = forms.IntegerField(required=True)

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
                    '<div> <label class="form-label">Datos del vehículo:</label> <div/> <hr/>'),
                "patente",
                "modelo",
                "chasis",
                "anio"
            ),
            Div(HTML(
                '<input href="{% url "crearCliente" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar registrando"/>')),
            Div(HTML(
                '<input href="{% url "listarClientes" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )

# Cliente - Filtro


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
                HTML("<label> DNI </label>"),
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

        widgets = {
            "patente": forms.TextInput(attrs={'pattern': '([A-Z]{2}\d{3}[A-Z]{2}|[A-Z]{3}\d{3})', 'placeholder': 'AA###AA o AAA###'})
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
                '<input href="{% url "crearVehiculo" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y continuar registrando"/>')),
            Div(HTML(
                '<input href="{% url "listarVehiculos" %}" type="submit" class="btn btn-primary mt-3" value="Guardar y salir"/>'))
        )


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
                HTML("<label> Año </label>"),
                "anio__gte",
                "anio__lte"
            ),
            Div(Submit('submit', 'Filtrar'), css_class='filter-btn-container')
        )
