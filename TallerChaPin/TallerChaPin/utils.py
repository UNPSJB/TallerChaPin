from xmlrpc.client import Boolean
from django import forms
from django.db.models import Q, Model, fields
from django.http import HttpResponse
from decimal import Decimal
from datetime import date
from django.views.generic.list import ListView
# from django_pandas.io import read_frame
import csv


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
        # elif isinstance(value, Model) or isinstance(value, int) or isinstance(value, Decimal):
        elif isinstance(value, (Model, int, Decimal, date)):
            filtro &= Q(**{attr: value})
    return filtro

# Filtros - Form

class FiltrosForm(forms.Form):
    ORDEN_CHOICES = []
    orden = forms.CharField(required=False)

    def filter(self, qs, filters):
        return qs.filter(dict_to_query(filters))  # aplicamos filtros

    def sort(self, qs, ordering):
        for o in ordering.split(','):
            if o != '':
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

# Lista Filtros - ListView

class ListFilterView(ListView):
    filtros = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.filtros:
            context['filtros'] = self.filtros(self.request.GET)
            context['query'] = self.get_queryset()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if self.filtros:
            filtros = self.filtros(self.request.GET)
            return filtros.apply(qs)
        return qs

def export_list(request, Modelo, Filtros):

    qs = Modelo.objects.all()
    filtros = Filtros(request.GET)
    if filtros.is_valid():
        qs = filtros.apply(qs)
    
        encabezados = filtros.sortables()
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename=filename.csv'
        
        writer = csv.writer(response, delimiter=";")

        fields_nombre = [v for k,v in encabezados]
        fields_clave = [k for k,v in encabezados]
        writer.writerow(fields_nombre)

        for fila in qs:
            valores = []
            for f in fields_clave:
                print(f)
                valor = getattr(fila, f)
                if callable(valor):
                    
                    try:
                        valor = valor()
                        if bool(valor):
                            valor = 'Si'
                        else:
                            valor = 'No'

                    except:
                        valor =  ''.join([str(v)+'\n' for v in valor.all()])

                if valor is None:
                    valor = 'n/a'
                

                valores.append(valor)
                print(valores)
            writer.writerow(valores)

    return response