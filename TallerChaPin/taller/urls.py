from django.urls import path

from .views import (
    EmpleadoListView,
    # index, 
    # listado_marcas, 
    # modelos_x_marcas, 
    # registrar_cliente, 
    MarcaListView, 
    ModeloListView,
    MarcaCreateView,
    ClienteListView,
    registrar_empleado,
    VehiculoListView,
    registrar_modelo,
    registrar_tipo_tarea,
    EmpleadoCreateView,
    EmpleadoUpdateView,
    EmpleadoDeleteView,
    EmpleadoListView
)


urlpatterns = [
    # path('', index),
    # path('marcas/', listado_marcas),
    #path('marcas/<slug:marca>/modelos', modelos_x_marcas, name="modelosXmarcas"),
    #path('cliente/registrar', registrar_cliente, name="registrarCliente"),
    path('marcas/crear', MarcaCreateView.as_view(), name="crearMarca"),
    path('marcas/listar', MarcaListView.as_view(), name="listarMarcas"),  
    path('modelos/listar', ModeloListView.as_view(), name="listarModelos"),
    path('clientes/listar', ClienteListView.as_view(), name='listarClientes'),
    path('empleado/registrar', registrar_empleado, name="registrarEmpleado"),
    path('vehiculos/listar', VehiculoListView.as_view(), name="listarVehiculos"),
    path('modelo/registrar', registrar_modelo, name="registrarModelo"),
    path('tipo-tarea/registrar', registrar_tipo_tarea, name="registrarTipoTarea"),
    path ('empleado/crear', EmpleadoCreateView.as_view(), name="crearEmpleado"),
    path('empleado/modificar/<int:pk>', EmpleadoUpdateView.as_view(), name="modificarEmpleado"),
    path('empleado/eliminar/<int:pk>', EmpleadoDeleteView.as_view(), name="eliminarEmpleado"),
    path ('empleados/listar', EmpleadoListView.as_view(), name="listarEmpleados")

]
