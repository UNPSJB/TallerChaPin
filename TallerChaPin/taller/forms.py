from django import forms
from .models import Marca
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class MarcaForm(forms.ModelForm):

    class Meta:
        model = Marca
        # opcionalmente '__all__' en lugar de la lista.
        fields = ['nombre', 'descripcion']
        exclude = []  # añadir campos a excluir

        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'cols': 30, 'rows': 3})
        }

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
        #self.helper.form_id = 'id-exampleForm'
        #self.helper.form_class = 'blueForms'
        #self.helper.form_method = 'post'
        #self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Guardar'))

    # TODO: implementar clean() para sanitización de datos y verificacion de errores.
