from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import *
from .forms import *
from django.contrib import messages
from TallerChaPin.utils import ListFilterView
# Create your views here.


def UnidadesDeMedida(request, pk):
    material = get_object_or_404(Material, pk=pk)
    return JsonResponse({'material': material.tipo.get_unidad_medida_display()})

def vehiculosDelCliente(request, pk):
    vehiculos = list(Vehiculo.objects.filter(cliente=pk).values('id', 'patente', 'modelo__nombre'))
    return JsonResponse({'pk_cliente': pk, 'vehiculos': vehiculos})

def MaterialCantidad(request):
    if request.method == "POST":
        form = ModificarCantidadForm(request.POST)
        pk = request.POST["pk"]
        if form.is_valid():
            form.save(pk)
        else:
            messages.add_message(request, messages.WARNING,'Cantidad no válida')
    return redirect('listarMateriales')

# ----------------------------- Marca View ----------------------------------- #


class MarcaCreateView(CreateView):
    model = Marca
    form_class = MarcaForm  # configuración de los campos del form + estilos.
    # a donde vamos luego de guardar exitosamente?
    success_url = reverse_lazy('crearMarca')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Marca"
        return context


    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Marca registrada con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)


class MarcaUpdateView(UpdateView):
    model = Marca
    form_class = MarcaForm
    success_url = reverse_lazy("listarMarcas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Marca"
        return context
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Marca modificada con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

class MarcaDeleteView(DeleteView):
    model = Marca
    success_url = reverse_lazy("listarMarcas")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class MarcaListView(ListFilterView):
    filtros = MarcaFiltrosForm
    model = Marca
    paginate_by = 100  # if pagination is desired
    ordering = ['nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Marcas"
        return context

# ----------------------------- Modelo View ----------------------------------- #

class ModeloCreateView(CreateView):
    model = Modelo
    form_class = ModeloForm
    success_url = reverse_lazy('crearModelo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Modelo"
        return context
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Modelo registrado con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)



class ModeloUpdateView(UpdateView):
    model = Modelo
    form_class = ModeloForm
    success_url = reverse_lazy("listarModelos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Modelo"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Modelo modificado con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

class ModeloDeleteView(DeleteView):
    model = Modelo
    success_url = reverse_lazy("listarModelos")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class ModeloListView(ListFilterView):
    filtros = ModeloFiltrosForm
    model = Modelo
    paginate_by = 100  # if pagination is desired
    ordering = ['nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Modelos"
        return context

# ----------------------------- Repuesto View ----------------------------------- #


class RepuestoCreateView(CreateView):
    model = Repuesto
    form_class = RepuestoForm
    success_url = reverse_lazy('crearRepuesto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Repuesto"
        return context
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Repuesto registrado con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)


class RepuestoUpdateView(UpdateView):
    model = Repuesto
    form_class = RepuestoForm
    success_url = reverse_lazy("listarRepuestos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Repuesto"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Repuesto modificado con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

class RepuestoDeleteView(DeleteView):
    model = Repuesto
    success_url = reverse_lazy("listarRepuestos")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class RepuestoListView(ListFilterView):
    filtros = RepuestoFiltrosForm
    model = Repuesto
    paginate_by = 100
    ordering = ['nombre']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Repuestos"
        return context

# ----------------------------- Tipo Tareas View ----------------------------------- #


class TipoTareaCreateView(CreateView):
    model = TipoTarea
    form_class = TipoTareaForm
    # success_url = reverse_lazy('crearTipoTarea')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Tipo de Tarea"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Tipo de tarea registrada con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)    

    def get_success_url(self):
        accion = self.request.POST['accion']
        return reverse_lazy('crearTipoTarea') if str(accion) != "Guardar y salir" else reverse_lazy('listarTipoTarea')


class TipoTareaUpdateView(UpdateView):
    model = TipoTarea
    form_class = TipoTareaForm
    success_url = reverse_lazy("listarTipoTarea")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Tipo de Tarea"
        return context
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Tipo de tarea modificada con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)    


class TipoTareaDeleteView(DeleteView):
    model = TipoTarea
    success_url = reverse_lazy("listarTipoTarea")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class TipoTareaListView(ListFilterView):
    filtros = TipoTareaFiltrosForm
    model = TipoTarea
    paginate_by = 100
    ordering = ['nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Tipos de Tarea"
        return context

# ----------------------------- Tareas View ----------------------------------- #

class TareaCreateView(CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'taller/tarea_form.html'
    success_url = reverse_lazy('crearTarea')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Tarea"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Tarea registrada con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)    


class TareaUpdateView(UpdateView):
    model = Tarea
    form_class = TareaForm
    success_url = reverse_lazy("listarTareas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Tarea"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Tarea modificada con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)    


class TareaDeleteView(DeleteView):
    model = Tarea
    success_url = reverse_lazy("listarTareas")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class TareaListView(ListFilterView):
    filtros = TareaFiltrosForm
    model = Tarea
    paginate_by = 100
    ordering = ['nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Tareas"
        return context

# ---------------------------- Tipo Material View ------------------------------------ #

class TipoMaterialCreateView(CreateView):
    model = TipoMaterial
    form_class = TipoMaterialForm
    success_url = reverse_lazy('crearTipoMaterial')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar tipo material"
        return context
    

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Tipo material registrado con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)    



class TipoMaterialListView(ListView):
    model = TipoMaterial
    paginate_by = 100
    ordering = ['nombre']

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
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Tipo material modificado con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)   

class TipoMaterialDeleteView(DeleteView):
    model = TipoMaterial
    success_url = reverse_lazy("listarTipoMateriales")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

# ---------------------------- Material View ------------------------------------ #

class MaterialListView(ListFilterView):
    filtros = MaterialFiltrosForm
    model = Material
    ordering = ['nombre']

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

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Material registrado con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)   


class MaterialUpdateView(UpdateView):
    model = Material
    form_class = MaterialForm
    success_url = reverse_lazy("listarMateriales")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Material"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Material modificado con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)  

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

# ---------------------------- Cliente View ------------------------------------ #

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
            messages.add_message(self.request, messages.INFO, 'Cliente y Vehiculos registrado con exito')
            return redirect('crearCliente')
        messages.add_message(self.request, messages.ERROR, cliente_form.errors)
        messages.add_message(self.request, messages.ERROR, vehiculo_form.errors)
        return self.form_invalid(form=cliente_form)

class ClienteUpdateView(UpdateView):

    model = Cliente
    form_class = ClienteUpdateForm
    success_url = reverse_lazy("listarClientes")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = "Modificar cliente"
        return context
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Cliente modificado con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form) 

class ClienteDeleteView(DeleteView):

    model = Cliente
    success_url = reverse_lazy("listarClientes")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class ClienteListView(ListFilterView):
    filtros = ClienteFiltrosForm
    model = Cliente
    success_url = reverse_lazy('listarClientes')
    ordering = ['dni']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Clientes"
        return context

# ---------------------------- Vehiculo View ------------------------------------ #

class VehiculoCreateView(CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    success_url = reverse_lazy('crearVehiculo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Vehículo"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Vehiculo registrado con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)  

class VehiculoUpdateView(UpdateView):

    model = Vehiculo
    form_class = VehiculoForm
    success_url = reverse_lazy("listarVehiculos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Vehículo"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, 'Vehiculo modificado con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)


class VehiculoDeleteView(DeleteView):

    model = Vehiculo
    success_url = reverse_lazy("listarVehiculos")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class VehiculoListView(ListFilterView):
    filtros = VehiculoFiltrosForm
    model = Vehiculo
    paginate_by = 100
    ordering = ['anio']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Vehículos"
        return context

# ---------------------------- Empleado View ------------------------------------ #

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
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Empleado registrado con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)  


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    success_url = reverse_lazy("listarEmpleados")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar empleado"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Empleado modificado con exito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)  

class EmpleadoDeleteView(DeleteView):
    model = Empleado
    success_url = reverse_lazy("listarEmpleados")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class EmpleadoListView(ListFilterView):
    filtros = EmpleadoFiltrosForm
    model = Empleado
    paginate_by = 100
    ordering = ['apellido']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de Empleados"
        return context

# ---------------------------------------------------------------- #
