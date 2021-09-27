from django.urls import reverse_lazy

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import *
from .forms import MarcaForm, EmpleadoForm
from .forms import MarcaForm, ModeloFiltrosForm

# Create your views here.

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

class ClienteListView(ListView):

    model = Cliente

    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Listado de Clientes"
        return context

class EmpleadoCreateView(CreateView):

    model = Empleado
    form_class = EmpleadoForm # configuración de los campos del form + estilos.
    template_name = 'taller/empleado_form.html' # template del form
    success_url = reverse_lazy('crearEmpleado') 

class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    success_url = reverse_lazy("listarEmpleados")

class EmpleadoDeleteView(DeleteView):
    model = Empleado
    success_url = reverse_lazy("listarEmpleados")
    
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

class EmpleadoListView(ListView):

    model = Empleado
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Empleados"
        return context


