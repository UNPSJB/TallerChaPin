from django import forms
from .models import Marca

class MarcaForm(forms.ModelForm):

    class Meta:
        model = Marca
        fields = ['nombre', 'descripcion'] # opcionalmente '__all__' en lugar de la lista.
        exclude = [] # añadir campos a excluir

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

    # TODO: implementar __init__()
    # TODO: implementar clean() para sanitización de datos y verificacion de errores.
