from django.urls import path
from .views import *
from .views import (
    ClienteCreateView,
    EmpleadoListView,
    MarcaListView,
    MaterialListView,
    MaterialCreateView,
    MaterialUpdateView,
    MaterialDeleteView,
    ModeloCreateView, 
    ModeloListView,
    MarcaCreateView,
    ClienteListView,
    RepuestoCreateView,
    RepuestoListView,
    RepuestoUpdateView,
    RepuestoDeleteView,
    VehiculoListView,
    EmpleadoCreateView,
    EmpleadoUpdateView,
    EmpleadoDeleteView,
    EmpleadoListView,
    TareaCreateView,
    MarcaUpdateView,
    MarcaDeleteView,
    ModeloUpdateView,
    ModeloDeleteView,
    TipoTareaCreateView,
    TipoTareaUpdateView,
    TipoTareaDeleteView,
    TipoTareaListView,
    TareaListView,
    TareaUpdateView,
    TareaDeleteView,
    TareaListView,
    MarcaUpdateView, 
    MarcaDeleteView,
    TipoMaterialCreateView
)


urlpatterns = [
    # ----------------- MARCAS -----------------

    path('marcas/crear', MarcaCreateView.as_view(), name="crearMarca"),
    path('marcas/listar', MarcaListView.as_view(), name="listarMarcas"),
    path('marca/modificar/<int:pk>',
         MarcaUpdateView.as_view(), name="modificarMarca"),
    path('marca/eliminar/<int:pk>',
         MarcaDeleteView.as_view(), name="eliminarMarca"),
         
    # ----------------- TAREAS -----------------

    path('tarea/crear', TareaCreateView.as_view(), name="crearTarea"),
    path('modelo/modificar/<int:pk>',
         TareaUpdateView.as_view(), name="modificarTarea"),
    path('modelo/eliminar/<int:pk>',
         TareaDeleteView.as_view(), name="eliminarTarea"),
    path('tareas/listar', TareaListView.as_view(), name="listarTareas"),

    # ----------------- TIPOS TAREA -----------------

    path('tipo-tarea/crear', TipoTareaCreateView.as_view(), name="crearTipoTarea"),
    path('tipo-tarea/modificar/<int:pk>',
         TipoTareaUpdateView.as_view(), name="modificarTipoTarea"),
    path('tipo-tarea/eliminar/<int:pk>',
         TipoTareaDeleteView.as_view(), name="eliminarTipoTarea"),
    path('tipo-tarea/listar', TipoTareaListView.as_view(), name="listarTipoTarea"),

    # ----------------- REPUESTOS -----------------

    path('repuesto/crear', RepuestoCreateView.as_view(), name="crearRepuesto"),
    path('repuestos/listar', RepuestoListView.as_view(), name="listarRepuestos"),
    path('repuesto/modificar/<int:pk>',
         RepuestoUpdateView.as_view(), name="modificarRepuesto"),
    path('repuesto/eliminar/<int:pk>',
         RepuestoDeleteView.as_view(), name="eliminarRepuesto"),

    # ----------------- MODELO -----------------

    path('modelo/crear', ModeloCreateView.as_view(), name="crearModelo"),
    path('modelos/listar', ModeloListView.as_view(), name="listarModelos"),
    path('modelo/modificar/<int:pk>',
         ModeloUpdateView.as_view(), name="modificarModelo"),
    path('modelo/eliminar/<int:pk>',
         ModeloDeleteView.as_view(), name="eliminarModelo"),

    # ----------------- MATERIALES -----------------

    path('materiales/listar', MaterialListView.as_view(), name="listarMateriales"),
    path('materiales/crear', MaterialCreateView.as_view(), name="crearMaterial"),
    path('materiales/eliminar/<int:pk>',
         MaterialDeleteView.as_view(), name="eliminarMaterial"),
    path('materiales/modificar/<int:pk>',
         MaterialUpdateView.as_view(), name="modificarMaterial"),

    # ----------------- TIPOS MTERIALES -----------------
    
    path('tipos-materiales/crear', TipoMaterialCreateView.as_view(), name="crearTipoMaterial"),
    path('tipos-materiales/listar', TipoMaterialListView.as_view(), name="listarTipoMateriales"),
    path('tipos-materiales/modificar/<int:pk>',
        TipoMaterialUpdateView .as_view(), name="modificarTipoMaterial"),
    path('tipos-materiales/eliminar/<int:pk>',
         TipoMaterialDeleteView.as_view(), name="eliminarTipoMaterial"),
    
    # ----------------- CLIENTES -----------------

    path('clientes/listar', ClienteListView.as_view(), name='listarClientes'),
    path('clientes/crear', ClienteCreateView.as_view(), name='crearCliente'),
        path('clientes/modificar/<int:pk>',
        ClienteUpdateView .as_view(), name="modificarCliente"),
    path('clientes/eliminar/<int:pk>',
         ClienteDeleteView.as_view(), name="eliminarCliente"),

    # ----------------- VEHICULOS -----------------

    path('vehiculos/listar', VehiculoListView.as_view(), name="listarVehiculos"),
    path('vehiculos/crear', VehiculoCreateView.as_view(), name="crearVehiculo"),
    path('vehiculos/modificar/<int:pk>',
         VehiculoUpdateView.as_view(), name="modificarVehiculo"),
    path('vehiculos/eliminar/<int:pk>',
         VehiculoDeleteView.as_view(), name="eliminarVehiculo"),

    # ----------------- EMPLEADOS -----------------

    path('empleado/crear', EmpleadoCreateView.as_view(), name="crearEmpleado"),
    path('empleado/modificar/<int:pk>',
         EmpleadoUpdateView.as_view(), name="modificarEmpleado"),
    path('empleado/eliminar/<int:pk>',
         EmpleadoDeleteView.as_view(), name="eliminarEmpleado"),
    path('empleados/listar', EmpleadoListView.as_view(), name="listarEmpleados"),
]
