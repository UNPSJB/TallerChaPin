from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from .models import *
from .forms import MarcaForm, EmpleadoForm

# Create your views here.


# def index(request):
#     return render(request, 'taller/listado_marcas.html')

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

# def listado_marcas(request):
#     marca = Marca(1,"ford", " ")
#     marca2 = Marca(2,"Fiat", " ")
#     marca.save()
#     marca2.save()
#     lista_marcas = [marca,marca2]

#     return render(request, 'taller/listado_marcas.html',context={"titulo": "marcas:", "marcas": lista_marcas})

# def modelos_x_marcas(request, marca):
#     marca = get_object_or_404(Marca, nombre=marca)
#     print(marca.modelos.all())
#     lista_modelos = [m for m in marca.modelos.all()]
#     return render(request, 'taller/modelos_x_marca.html', context={"titulo": "modelos:", "modelos": lista_modelos})

def registrar_cliente(request):
    return render(request, 'taller/form_registrar_cliente.html', {"titulo": "Registrar Cliente"})


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
    success_url = reverse_lazy("crearEmpleado")

class EmpleadoListView(ListView):

    model = Empleado
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Empleados"
        return context


