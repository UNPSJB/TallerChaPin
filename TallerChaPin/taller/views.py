from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import *
from .forms import *
from django.contrib import messages
from TallerChaPin.utils import ListFilterView, export_list


import pandas as pd
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
        messages.add_message(self.request, messages.SUCCESS, 'Marca registrada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

    def post(self, *args, **kwargs):
        self.object = None
        form = MarcaForm(self.request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Marca registrada con éxito')
            if 'guardar' in self.request.POST:
                return redirect('listarMarcas')
            return redirect('crearMarca')
        return self.form_invalid(form=form)

class MarcaUpdateView(UpdateView):
    model = Marca
    form_class = MarcaForm
    success_url = reverse_lazy("listarMarcas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Marca"
        return context
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Marca modificada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

class MarcaDeleteView(DeleteView):
    model = Marca
    success_url = reverse_lazy("listarMarcas")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.add_message(self.request, messages.SUCCESS, f'Marca eliminada con éxito..')
        except models.RestrictedError:
            messages.add_message(self.request, messages.WARNING, f'La marca "{self.object.nombre}" no se puede eliminar porque posee modelos registrados.')
        finally:
            return redirect(success_url)


class MarcaListView(ListFilterView):
    filtros = MarcaFiltrosForm
    model = Marca
    paginate_by = 100  # if pagination is desired
    ordering = ['nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de marcas"
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
        messages.add_message(self.request, messages.SUCCESS, 'Modelo registrado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

    def post(self, *args, **kwargs):
        self.object = None
        form = ModeloForm(self.request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Modelo registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('listarModelos')
            return redirect('crearModelo')
        return self.form_invalid(form=form)


class ModeloUpdateView(UpdateView):
    model = Modelo
    form_class = ModeloForm
    success_url = reverse_lazy("listarModelos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Modelo"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Modelo modificado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

class ModeloDeleteView(DeleteView):
    model = Modelo
    success_url = reverse_lazy("listarModelos")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.add_message(self.request, messages.SUCCESS, f'Modelo eliminado con éxito.')
        except models.RestrictedError:
            messages.add_message(self.request, messages.WARNING, f'El modelo "{self.object.nombre}" no se puede eliminar porque está en uso.')
        finally:
            return redirect(success_url)


class ModeloListView(ListFilterView):
    filtros = ModeloFiltrosForm
    model = Modelo
    paginate_by = 100  # if pagination is desired
    ordering = ['nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de modelos"
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
        messages.add_message(self.request, messages.SUCCESS, 'Repuesto registrado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

    def post(self, *args, **kwargs):
        self.object = None
        form = RepuestoForm(self.request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Repuesto registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('listarRepuestos')
            return redirect('crearRepuesto')
        return self.form_invalid(form=form)

class RepuestoUpdateView(UpdateView):
    model = Repuesto
    form_class = RepuestoForm
    success_url = reverse_lazy("listarRepuestos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Repuesto"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Repuesto modificado con éxito')
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
        context['titulo'] = "Listado de repuestos"
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
        messages.add_message(self.request, messages.SUCCESS, 'Tipo de tarea registrada con éxito')
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
        messages.add_message(self.request, messages.SUCCESS, 'Tipo de tarea modificada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)    


class TipoTareaDeleteView(DeleteView):
    model = TipoTarea
    success_url = reverse_lazy("listarTipoTarea")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
        
    def post(self, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.add_message(self.request, messages.SUCCESS, 'Tipo de tarea eliminada con éxito.')
        except models.RestrictedError:
            messages.add_message(self.request, messages.WARNING, f'El tipo de tarea "{self.object.nombre}" no se puede eliminar porque posee tareas registradas.')
        finally:
            return redirect(success_url)


class TipoTareaListView(ListFilterView):
    filtros = TipoTareaFiltrosForm
    model = TipoTarea
    paginate_by = 100
    ordering = ['nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de tipos de tarea"
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
        messages.add_message(self.request, messages.SUCCESS, 'Tarea registrada con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)    

    def post(self, *args, **kwargs):
        self.object = None
        form = TareaForm(self.request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Tarea registrada con éxito')
            if 'guardar' in self.request.POST:
                return redirect('listarTareas')
            return redirect('crearTarea')
        return self.form_invalid(form=form)

class TareaUpdateView(UpdateView):
    model = Tarea
    form_class = TareaForm
    success_url = reverse_lazy("listarTareas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Tarea"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Tarea modificada con éxito')
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
        context['titulo'] = "Listado de tareas"
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
        messages.add_message(self.request, messages.SUCCESS, 'Tipo material registrado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)    

    def post(self, *args, **kwargs):
        self.object = None
        form = TipoMaterialForm(self.request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Tipo Material registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('listarTipoMateriales')
            return redirect('crearTipoMaterial')
        return self.form_invalid(form=form)


class TipoMaterialListView(ListFilterView):
    filtros = TipoMaterialFiltrosForm
    model = TipoMaterial
    paginate_by = 100
    ordering = ['nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de tipos de materiales"
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
        messages.add_message(self.request, messages.SUCCESS, 'Tipo material modificado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)   

class TipoMaterialDeleteView(DeleteView):
    model = TipoMaterial
    success_url = reverse_lazy("listarTipoMateriales")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.add_message(self.request, messages.SUCCESS, f'Tipo de material eliminado con éxito.')
        except models.RestrictedError:
            messages.add_message(self.request, messages.WARNING, f'El tipo de material "{self.object.nombre}" no se puede eliminar porque está en uso.')
        finally:
            return redirect(success_url)

# ---------------------------- Material View ------------------------------------ #

class MaterialListView(ListFilterView):
    filtros = MaterialFiltrosForm
    model = Material
    ordering = ['nombre']

    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de materiales"
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
        messages.add_message(self.request, messages.SUCCESS, 'Material registrado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)   

    def post(self, *args, **kwargs):
        self.object = None
        form = MaterialForm(self.request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Material registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('listarMateriales')
            return redirect('crearMaterial')
        return self.form_invalid(form=form)

class MaterialUpdateView(UpdateView):
    model = Material
    form_class = MaterialForm
    success_url = reverse_lazy("listarMateriales")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Material"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Material modificado con éxito')
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
        context['ayuda'] = 'crear_cliente.html'
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
            messages.add_message(self.request, messages.SUCCESS, 'Cliente y Vehiculos registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('listarClientes')
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
        messages.add_message(self.request, messages.SUCCESS, 'Cliente modificado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form) 

class ClienteDeleteView(DeleteView):

    model = Cliente
    success_url = reverse_lazy("listarClientes")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.add_message(self.request, messages.SUCCESS, f'Cliente eliminado con éxito.')
        except models.RestrictedError:
            messages.add_message(self.request, messages.WARNING, f'El cliente {self.object} no se puede eliminar porque está en uso.')
        finally:
            return redirect(success_url)


class ClienteListView(ListFilterView):
    filtros = ClienteFiltrosForm
    model = Cliente
    success_url = reverse_lazy('listarClientes')
    ordering = ['dni']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de clientes"
        return context

# def exportar_listado(request,):
#     qs = Modelo.objects.all()
#     print(request.GET)
#     filtros = Filtros(request.GET)
#     if filtros.is_valid():
#         qs = filtros.apply(qs)
#     print("hola",filtros)
#     return export_list(qs)

# exportar_listado_clientes = lambda r: export_list(r, Cliente, ClienteFiltrosForm, ["nombre", "apellido", "vip"])
exportar_listado_clientes = lambda r: export_list(r, Cliente, ClienteFiltrosForm)    

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
        messages.add_message(self.request, messages.SUCCESS, 'Vehiculo registrado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)  

    def post(self, *args, **kwargs):
        self.object = None
        form = VehiculoForm(self.request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Vehiculo registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('listarVehiculos')
            return redirect('crearVehiculo')
        return self.form_invalid(form=form)
        

class VehiculoUpdateView(UpdateView):

    model = Vehiculo
    form_class = VehiculoForm
    success_url = reverse_lazy("listarVehiculos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Vehículo"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Vehiculo modificado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)


class VehiculoDeleteView(DeleteView):

    model = Vehiculo
    success_url = reverse_lazy("listarVehiculos")

    def get(self, *args, **kwargs):
        return self.post(self, *args, **kwargs)

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except models.RestrictedError:
            messages.add_message(self.request, messages.WARNING, f'El vehículo {self.object.patente } no se puede eliminar porque está en uso.')
        finally:
            return redirect(success_url)



class VehiculoListView(ListFilterView):
    filtros = VehiculoFiltrosForm
    model = Vehiculo
    paginate_by = 100
    ordering = ['anio']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Listado de vehículos"
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
        messages.add_message(self.request, messages.SUCCESS, 'Empleado registrado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)  

    def post(self, *args, **kwargs):
        self.object = None
        form = EmpleadoForm(self.request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Empleado registrado con éxito')
            if 'guardar' in self.request.POST:
                return redirect('listarEmpleados')
            return redirect('crearEmpleado')
        return self.form_invalid(form=form)


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    success_url = reverse_lazy("listarEmpleados")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar empleado"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Empleado modificado con éxito')
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
        context['titulo'] = "Listado de empleados"
        return context

# ---------------------------------------------------------------- #
