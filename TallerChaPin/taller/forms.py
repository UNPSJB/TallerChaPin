from django import forms
from .models import Empleado, Marca, Modelo, Repuesto, Tarea, TipoTarea
from django.db.models.query import QuerySet
from .models import Marca
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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

class ModeloForm(forms.ModelForm):
    class Meta:
        model = Modelo
        fields = "__all__"

    def save(self, commit=True):
        modelo = super().save()
        return modelo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        
        self.helper.add_input(Submit('submit', 'Guardar'))

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

class EmpleadoForm(forms.ModelForm):
    
    class Meta:
        model = Empleado
        # opcionalmente '__all__' en lugar de la lista.
        fields = ['nombre', 'apellido','cuil','legajo']
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

class ModeloFiltrosForm(forms.Form):
    nombre = forms.CharField(required=False, label='Nombre', max_length=100)
    descripcion = forms.CharField(required=False)
    marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'

        self.helper.add_input(Submit('submit', 'Filtrar'))