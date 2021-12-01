from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import *
from .forms import *
from django.contrib import messages
# Create your views here.


def UnidadesDeMedida(request, pk):
    material = get_object_or_404(Material, pk=pk)
    return JsonResponse({'material': material.tipo.get_unidad_medida_display()})


class ListFilterView(ListView):
    filtros = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.filtros:
            context['filtros'] = self.filtros(self.request.GET)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if self.filtros:
            filtros = self.filtros(self.request.GET)
            return filtros.apply(qs)
        return qs

# ---------------------------------------------------------------- #

# Marca Views


class MarcaCreateView(CreateView):
    model = Marca
    form_class = MarcaForm  # configuración de los campos del form + estilos.
    # a donde vamos luego de guardar exitosamente?
    success_url = reverse_lazy('crearMarca')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Marca"
        return context


class MarcaUpdateView(UpdateView):
    model = Marca
    form_class = MarcaForm
    success_url = reverse_lazy("listarMarcas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Marca"
        return context


class MarcaDeleteView(DeleteView):
    model = Marca
    success_url = reverse_lazy("listarMarcas")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class MarcaListView(ListFilterView):
    filtros = MarcaFiltrosForm
    model = Marca
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Marcas"
        return context

# ---------------------------------------------------------------- #

# Modelo View


class ModeloCreateView(CreateView):
    model = Modelo
    form_class = ModeloForm
    success_url = reverse_lazy('crearModelo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Modelo"
        return context


class ModeloUpdateView(UpdateView):
    model = Modelo
    form_class = ModeloForm
    success_url = reverse_lazy("listarModelos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Modelo"
        return context


class ModeloDeleteView(DeleteView):
    model = Modelo
    success_url = reverse_lazy("listarModelos")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class ModeloListView(ListFilterView):
    filtros = ModeloFiltrosForm
    model = Modelo
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Modelos"
        return context

# ---------------------------------------------------------------- #

# Repuesto Views


class RepuestoCreateView(CreateView):
    model = Repuesto
    form_class = RepuestoForm
    success_url = reverse_lazy('crearRepuesto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Repuesto"
        return context


class RepuestoUpdateView(UpdateView):
    model = Repuesto
    form_class = RepuestoForm
    success_url = reverse_lazy("listarRepuestos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Vehiculo"
        return context


class RepuestoDeleteView(DeleteView):
    model = Repuesto
    success_url = reverse_lazy("listarRepuestos")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class RepuestoListView(ListFilterView):
    filtros = RepuestoFiltrosForm
    model = Repuesto
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Repuestos"
        return context

# ---------------------------------------------------------------- #

# Tipo de tareas View


class TipoTareaCreateView(CreateView):
    model = TipoTarea
    form_class = TipoTareaForm
    success_url = reverse_lazy('crearTipoTarea')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Tipo de Tarea"
        return context


class TipoTareaUpdateView(UpdateView):
    model = TipoTarea
    form_class = TipoTareaForm
    success_url = reverse_lazy("listarTipoTarea")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Tipo de Tarea"
        return context


class TipoTareaDeleteView(DeleteView):
    model = TipoTarea
    success_url = reverse_lazy("listarTipoTarea")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class TipoTareaListView(ListFilterView):
    filtros = TipoTareaFiltrosForm
    model = TipoTarea
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class TareaListView(ListFilterView):
    filtros = TareaFiltrosForm
    model = Tarea
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Tareas"
        return context

# ---------------------------------------------------------------- #

# Material View


class MaterialListView(ListFilterView):
    filtros = MaterialFiltrosForm
    model = Material

    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Materiales"
        context['modificarCantidadForm'] = ModificarCantidadForm()
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

def modificar_cantidad(request):
    form = ModificarCantidadForm(request.POST)
    if form.is_valid():
        form.finalizar()
        messages.add_message(request, messages.SUCCESS,
                             'Se ha modificado la cantidad del material.')
    else:
        messages.add_message(request, messages.WARNING,
                             'No se ha podido modificar la cantidad del material.')
    return redirect('listarMateriales')
# ---------------------------------------------------------------- #

# Tipo Material View


class TipoMaterialCreateView(CreateView):
    model = TipoMaterial
    form_class = TipoMaterialForm
    success_url = reverse_lazy('crearTipoMaterial')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar tipo material"
        return context


class TipoMaterialListView(ListView):
    model = TipoMaterial

    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtros'] = TipoMaterialFiltrosForm(self.request.GET)
        context['titulo'] = "Listado de Tipos Materiales"
        return context


class TipoMaterialUpdateView(UpdateView):
    model = TipoMaterial
    form_class = TipoMaterialForm
    success_url = reverse_lazy("listarTipoMateriales")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar tipo Material"
        return context


class TipoMaterialDeleteView(DeleteView):
    model = TipoMaterial
    success_url = reverse_lazy("listarTipoMateriales")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

# ---------------------------------------------------------------- #

# Repuesto View


class RepuestoCreateView(CreateView):
    model = Repuesto
    form_class = RepuestoForm
    success_url = reverse_lazy('crearRepuesto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Repuesto"
        return context


class RepuestoUpdateView(UpdateView):
    model = Repuesto
    form_class = RepuestoForm
    success_url = reverse_lazy("listarRepuestos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Repuesto"
        return context


class RepuestoDeleteView(DeleteView):
    model = Repuesto
    success_url = reverse_lazy("listarRepuestos")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class RepuestoListView(ListFilterView):
    filtros = RepuestoFiltrosForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Registrar cliente"
        return context

    def post(self, *args, **kwargs):
        self.object = None
        cliente_form = self.get_form()
        vehiculo_form = ClienteVehiculoForm(self.request.POST)

        if cliente_form.is_valid() and vehiculo_form.is_valid():
            cliente = cliente_form.save()
            vehiculo = vehiculo_form.save(commit=False)
            vehiculo.cliente = cliente
            vehiculo.save()
            return redirect('home')
        return self.form_invalid(form=cliente_form)


class ClienteUpdateView(UpdateView):

    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy("listarClientes")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Modificar cliente"
        return context


class ClienteDeleteView(DeleteView):

    model = Cliente
    success_url = reverse_lazy("listarClientes")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class ClienteListView(ListFilterView):
    filtros = ClienteFiltrosForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Vehículo"
        return context


class VehiculoUpdateView(UpdateView):

    model = Vehiculo
    form_class = VehiculoForm
    success_url = reverse_lazy("listarVehiculos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Vehículo"
        return context


class VehiculoDeleteView(DeleteView):

    model = Vehiculo
    success_url = reverse_lazy("listarVehiculos")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class VehiculoListView(ListFilterView):
    filtros = VehiculoFiltrosForm
    model = Vehiculo
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Vehículos"
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


class EmpleadoListView(ListFilterView):
    filtros = EmpleadoFiltrosForm
    model = Empleado
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Empleados"
        return context

# ---------------------------------------------------------------- #
