from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from .models import *
from .forms import *
from datetime import date
from django.contrib import messages
from TallerChaPin.utils import ListFilterView, export_list
import json



# class ReportePrueba(TemplateView):
#     template_name = 'reporte_prueba.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

def ReportePrueba(request):
    context={}
    context['titulo'] = "Reporte 1"
    return render (request, 'reportes/reporte_prueba.html',context)


def traerJson(request):

    marcas = list(Marca.objects.all().values('pk','nombre'))
    reponse = []
    for marca in marcas:
        cantidad = Vehiculo.objects.filter(modelo__marca = marca['pk']).count()
        reponse.append({'cantidad': cantidad , 'nombre':marca['nombre']})
    reponse.sort(key=lambda c : c['cantidad'], reverse=True)
    return JsonResponse({'vehiculos' : reponse })