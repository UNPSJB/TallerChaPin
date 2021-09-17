from django.urls import path

from .views import (
    EmpleadoListView,
    # index, 
    # listado_marcas, 
    # modelos_x_marcas, 
    registrar_cliente, 
    MarcaListView, 
    ModeloListView,
    MarcaCreateView,
    EmpleadoCreateView,
    EmpleadoUpdateView,
    EmpleadoListView
)


urlpatterns = [
    # path('', index),
    # path('marcas/', listado_marcas),
    path('marcas/crear', MarcaCreateView.as_view(), name="crearMarca"),
    path('marcas/listar', MarcaListView.as_view(), name="listarMarcas"),
    #path('marcas/<slug:marca>/modelos', modelos_x_marcas, name="modelosXmarcas"),
    path('cliente/registrar', registrar_cliente, name="registrarCliente"),
    path('modelos/listar', ModeloListView.as_view(), name="listarModelos"),
    path ('empleado/crear', EmpleadoCreateView.as_view(), name="crearEmpleado"),
    path('empleado/modificar/<int:pk>', EmpleadoUpdateView.as_view(), name="modificarEmpleado"),
    path ('empleados/listar', EmpleadoListView.as_view(), name="listarEmpleados")

]
