from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import *
from .forms import *

# Create your views here.

# Marca Views


class MarcaCreateView(CreateView):
    model = Marca
    form_class = MarcaForm  # configuración de los campos del form + estilos.
    # a donde vamos luego de guardar exitosamente?
    success_url = reverse_lazy('crearMarca')


class MarcaUpdateView(UpdateView):
    model = Marca
    form_class = MarcaForm
    success_url = reverse_lazy("listarMarcas")


class MarcaDeleteView(DeleteView):
    model = Marca
    success_url = reverse_lazy("listarMarcas")
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class MarcaListView(ListView):
    model = Marca
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtros'] = MarcaFiltrosForm(self.request.GET)
        context['titulo'] = "Listado de Marcas"
        return context

# ---------------------------------------------------------------- #

# Modelo View


class ModeloCreateView(CreateView):
    model = Modelo
    form_class = ModeloForm
    success_url = reverse_lazy('crearModelo')


class ModeloUpdateView(UpdateView):
    model = Modelo
    form_class = ModeloForm
    success_url = reverse_lazy("listarModelos")


class ModeloDeleteView(DeleteView):
    model = Modelo
    success_url = reverse_lazy("listarModelos")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


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
        #return qs
        return qs.filter(
            nombre=self.request.GET.get('nombre'),
            descripcion=self.request.GET.get('descripcion'),
            marca=self.request.GET.get('marca')
        )

# ---------------------------------------------------------------- #

# Repuesto Views


class RepuestoCreateView(CreateView):
    model = Repuesto
    form_class = RepuestoForm
    success_url = reverse_lazy('crearRepuesto')


class RepuestoUpdateView(UpdateView):
    model = Repuesto
    form_class = RepuestoForm
    success_url = reverse_lazy("listarRepuestos")


class RepuestoDeleteView(DeleteView):
    model = Repuesto
    success_url = reverse_lazy("listarRepuestos")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class RepuestoListView(ListView):

    model = Repuesto
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtros'] = RepuestoFiltrosForm(self.request.GET)
        context['titulo'] = "Listado de Repuestos"
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs
       
# ---------------------------------------------------------------- #

# Tipo de tareas View

class TipoTareaCreateView(CreateView):
    model = TipoTarea
    form_class = TipoTareaForm
    template_name = 'taller/tipotarea_form.html'
    success_url = reverse_lazy('crearTipoTarea')


class TipoTareaUpdateView(UpdateView):
    model = TipoTarea
    form_class = TipoTareaForm
    template_name = 'taller/tipotarea_update_form.html'
    success_url = reverse_lazy("listarTipoTarea")


class TipoTareaDeleteView(DeleteView):
    model = TipoTarea
    success_url = reverse_lazy("listarTipoTarea")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class TipoTareaListView(ListView):

    model = TipoTarea
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtros'] = TipoTareaFiltrosForm(self.request.GET)
        context['titulo'] = "Listado de Tipos de Tarea"
        return context

# ---------------------------------------------------------------- #

# Tareas View


class TareaCreateView(CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'taller/tarea_form.html'
    success_url = reverse_lazy('crearTarea')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Tarea"
        return context

class TareaUpdateView(UpdateView):
    model = Tarea
    form_class = TareaForm
    success_url = reverse_lazy("listarTareas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Tarea"
        return context


class TareaDeleteView(DeleteView):
    model = TipoTarea
    success_url = reverse_lazy("listarTareas")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

class TareaListView(ListView):
    model = Tarea
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Tareas"
        return context

# ---------------------------------------------------------------- #


# Material View

class MaterialListView(ListView):
    model = Material

    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtros'] = MaterialFiltrosForm(self.request.GET)
        context['titulo'] = "Listado de Materiales"
        return context

class MaterialCreateView(CreateView):
    model = Material
    form_class = MaterialForm
    success_url = reverse_lazy('crearMaterial')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar material"
        return context

class MaterialUpdateView(UpdateView):
    model = Material
    form_class = MaterialForm
    success_url = reverse_lazy("listarMateriales")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Material"
        return context

class MaterialDeleteView(DeleteView):
    model = Material
    success_url = reverse_lazy("listarMateriales")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
# ---------------------------------------------------------------- #

# Repuesto View


class RepuestoListView(ListView):
    model = Repuesto
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Repuestos"
        return context

# ---------------------------------------------------------------- #

# Cliente View


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    # template_name = 'taller/cliente_form.html' # template del form
    success_url = reverse_lazy('crearCliente')

class ClienteUpdateView(UpdateView):

    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy("listarClientes")

class ClienteDeleteView(DeleteView):

    model = Cliente
    success_url = reverse_lazy("listarClientes")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class ClienteListView(ListView):

    model = Cliente
    success_url = reverse_lazy('listarClientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Listado de Clientes"
        return context
# ---------------------------------------------------------------- #

# Vehiculo View


class VehiculoCreateView(CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    success_url = reverse_lazy('crearVehiculo')

class VehiculoUpdateView(UpdateView):

    model = Vehiculo
    form_class = VehiculoForm
    success_url = reverse_lazy("listarVehiculos")

class VehiculoDeleteView(DeleteView):

    model = Vehiculo
    success_url = reverse_lazy("listarVehiculos")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

class VehiculoListView(ListView):
    model = Vehiculo
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtros'] = VehiculoFiltrosForm(self.request.GET)
        context['titulo'] = "Listado de Vehiculos"
        return context
# ---------------------------------------------------------------- #

# Empleado View


class EmpleadoCreateView(CreateView):

    model = Empleado
    # configuración de los campos del form + estilos.
    form_class = EmpleadoForm
    # template_name = 'taller/empleado_form.html' # template del form
    success_url = reverse_lazy('crearEmpleado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar empleado"
        return context

class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    success_url = reverse_lazy("listarEmpleados")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar empleado"
        return context


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
        context['filtros'] = EmpleadoFiltrosForm(self.request.GET)
        context['titulo'] = "Listado de Empleados"
        return context

# ---------------------------------------------------------------- #
