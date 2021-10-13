from django.urls import path

from .views import (
    EmpleadoListView,
    MarcaListView,
    MaterialListView,
    ModeloCreateView, 
    ModeloListView,
    MarcaCreateView,
    ClienteListView,
    VehiculoListView,
    EmpleadoCreateView,
    EmpleadoUpdateView,
    EmpleadoDeleteView,
    EmpleadoListView
)


urlpatterns = [
    path('marcas/crear', MarcaCreateView.as_view(), name="crearMarca"),
    path('marcas/listar', MarcaListView.as_view(), name="listarMarcas"),  
    path('modelo/crear', ModeloCreateView.as_view(), name="crearModelo"),
    path('modelos/listar', ModeloListView.as_view(), name="listarModelos"),
    path('materiales/listar', MaterialListView.as_view(), name="listarMateriales"),
    path('clientes/listar', ClienteListView.as_view(), name='listarClientes'),
    path('vehiculos/listar', VehiculoListView.as_view(), name="listarVehiculos"),
    path ('empleado/crear', EmpleadoCreateView.as_view(), name="crearEmpleado"),
    path('empleado/modificar/<int:pk>', EmpleadoUpdateView.as_view(), name="modificarEmpleado"),
    path('empleado/eliminar/<int:pk>', EmpleadoDeleteView.as_view(), name="eliminarEmpleado"),
    path ('empleados/listar', EmpleadoListView.as_view(), name="listarEmpleados")

]
