from django.urls import path

from .views import (
    ClienteCreateView,
    EmpleadoListView,
    MarcaListView,
    MaterialListView,
    ModeloCreateView, 
    ModeloListView,
    MarcaCreateView,
    ClienteListView,
    RepuestoCreateView,
    RepuestoListView,
    VehiculoListView,
    EmpleadoCreateView,
    EmpleadoUpdateView,
    EmpleadoDeleteView,
    EmpleadoListView,
    TareaCreateView,
    TipoTareaCreateView,
    RepuestoListView,
    TareaListView,
    MarcaUpdateView, 
    MarcaDeleteView
)


urlpatterns = [
    # ----------------- MARCAS -----------------
    path('marcas/crear', MarcaCreateView.as_view(), name="crearMarca"),
    path('marcas/listar', MarcaListView.as_view(), name="listarMarcas"), 
    path('marca/modificar/<int:pk>', MarcaUpdateView.as_view(), name="modificarMarca"),
    path('marca/eliminar/<int:pk>', MarcaDeleteView.as_view(), name="eliminarMarca"),
    # ----------------- TAREAS -----------------
    path('tarea/crear', TareaCreateView.as_view(), name="crearTarea"),
    path('tareas/listar', TareaListView.as_view(), name="listarTareas"),
    # ----------------- TIPOS TAREA -----------------
    path('tipo-tarea/crear', TipoTareaCreateView.as_view(), name="crearTipoTarea"),
    # ----------------- REPUESTOS -----------------
    path('repuesto/crear', RepuestoCreateView.as_view(), name="crearRepuesto"),
    path('repuestos/listar', RepuestoListView.as_view(), name="listarRepuestos"),
     # ----------------- MODELO -----------------
    path('modelo/crear', ModeloCreateView.as_view(), name="crearModelo"),
    path('modelos/listar', ModeloListView.as_view(), name="listarModelos"),
    # ----------------- MATERIALES -----------------
    path('materiales/listar', MaterialListView.as_view(), name="listarMateriales"),
    # ----------------- CLIENTES -----------------
    path('clientes/listar', ClienteListView.as_view(), name='listarClientes'),
    path('clientes/crear', ClienteCreateView.as_view(), name='crearCliente'),
    # ----------------- VEHICULOS -----------------
    path('vehiculos/listar', VehiculoListView.as_view(), name="listarVehiculos"),
    # ----------------- EMPLEADOS -----------------    
    path ('empleado/crear', EmpleadoCreateView.as_view(), name="crearEmpleado"),
    path('empleado/modificar/<int:pk>', EmpleadoUpdateView.as_view(), name="modificarEmpleado"),
    path('empleado/eliminar/<int:pk>', EmpleadoDeleteView.as_view(), name="eliminarEmpleado"),
    path ('empleados/listar', EmpleadoListView.as_view(), name="listarEmpleados"),
]
