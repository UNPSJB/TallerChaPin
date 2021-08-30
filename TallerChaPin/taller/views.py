from django.shortcuts import get_object_or_404, render
from .models import *
# Create your views here.


def index(request):
    return render(request, 'taller/listado_marcas.html')

def listado_marcas(request):
    marca = Marca(1,"ford", " ")
    marca2 = Marca(2,"Fiat", " ")
    marca.save()
    marca2.save()
    lista_marcas = [marca,marca2]

    return render(request, 'taller/listado_marcas.html',context={"titulo": "marcas:", "marcas": lista_marcas})

def modelos_x_marcas(request, marca):
    marca = get_object_or_404(Marca, nombre=marca)
    print(marca.modelos.all())
    lista_modelos = [m for m in marca.modelos.all()]
    return render(request, 'taller/modelos_x_marca.html', context={"titulo": "modelos:", "modelos": lista_modelos})