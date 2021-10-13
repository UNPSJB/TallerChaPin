from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import *
from .forms import MarcaForm, ModeloFiltrosForm
# Create your views here.


def index(request):
    return render(request, 'taller/listado_marcas.html')


def listado_marcas(request):
    marca = Marca(1, "ford", " ")
    marca2 = Marca(2, "Fiat", " ")
    marca.save()
    marca2.save()
    lista_marcas = [marca, marca2]

    return render(request, 'taller/listado_marcas.html', context={"titulo": "marcas:", "marcas": lista_marcas})


def modelos_x_marcas(request, marca):
    """
        Obtiene los modelos de una marca
    """
    marca = get_object_or_404(Marca, nombre=marca)
    print(marca.modelos.all())
    lista_modelos = [m for m in marca.modelos.all()]
    return render(request, 'taller/modelos_x_marca.html', context={"titulo": "modelos:", "modelos": lista_modelos})


def registrar_cliente(request):
    return render(request, 'taller/form_registrar_cliente.html', {"titulo": "Registrar Cliente"})

def registrar_empleado(request):
    return render(request, 'taller/form_registrar_empleado.html', {"titulo": "Registrar Empleado"})

def registrar_modelo(request):
    return render(request, 'taller/form_registrar_modelo.html', {"titulo": "Registrar Modelo"})

def registrar_tipo_tarea(request):
    return render(request, 'taller/form_registrar_tipo_tarea.html', {"titulo": "Registrar Tipo de Tarea"})


class MarcaCreateView(CreateView):
    model = Marca
    form_class = MarcaForm  # configuración de los campos del form + estilos.
    template_name = 'taller/marca_form.html'  # template del form
    # a donde vamos luego de guardar exitosamente?
    success_url = reverse_lazy('crearMarca')


class MarcaListView(ListView):
    model = Marca
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Marcas"
        return context


class ModeloListView(ListView):

    model = Modelo
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtros'] = ModeloFiltrosForm(self.request.GET)
        context['titulo'] = "Listado de Modelos"
        return context

    def get_queryset(self):
        # print(self.request.GET)
        #{'nombre': ['Gol'], 'descripcion': [''], 'marca': [''], 'submit': ['Filtrar']}
        #{'nombre': ['Punto'], 'descripcion': [''], 'marca': ['3'], 'submit': ['Filtrar']}
        qs = super().get_queryset()
        return qs
        # return qs.filter(algo(self.request.GET))

class VehiculoListView(ListView):
    model = Vehiculo
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Vehiculos"
        return context

class ClienteListView(ListView):

    model = Cliente
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Clientes"
        return context
