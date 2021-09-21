from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import *
from .forms import MarcaForm, EmpleadoForm

# Create your views here.



class MarcaCreateView(CreateView):
    model = Marca
    form_class = MarcaForm # configuración de los campos del form + estilos.
    template_name = 'taller/marca_form.html' # template del form
    success_url = reverse_lazy('crearMarca') # a donde vamos luego de guardar exitosamente?

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
        context['titulo'] = "Listado de Modelos"
        return context

class EmpleadoCreateView(CreateView):

    model = Empleado
    form_class = EmpleadoForm # configuración de los campos del form + estilos.
    template_name = 'taller/empleado_form.html' # template del form
    success_url = reverse_lazy('crearEmpleado') 

class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = "taller/empleado_update_form.html"
    success_url = reverse_lazy("listarEmpleado")

class EmpleadoDeleteView(DeleteView):
    model = Empleado
    form_class= EmpleadoForm
    teamplate_name = "taller/empleado_delete_form.html"
    success_url = reverse_lazy("listarEmpleado")

class EmpleadoListView(ListView):

    model = Empleado
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Empleados"
        return context


