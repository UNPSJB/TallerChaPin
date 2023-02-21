from django.urls import path
from .views import *


urlpatterns = [

     path('materiales/unidades_de_medida/<int:pk>', UnidadesDeMedida),
     path('cliente/vehiculos/<int:pk>', vehiculosDelCliente),
     # ----------------- MARCAS -----------------

     path('marcas/crear', MarcaCreateView.as_view(), name="crearMarca"),
     path('marcas/listar', MarcaListView.as_view(), name="listarMarcas"),
     path('marca/modificar/<int:pk>',
          MarcaUpdateView.as_view(), name="modificarMarca"),
     path('marca/eliminar/<int:pk>',
          MarcaDeleteView.as_view(), name="eliminarMarca"),
     path('marcas/exportar',
          exportar_listado_marcas, name='exportarMarcas'),
     # ----------------- TAREAS -----------------

     path('tarea/crear', TareaCreateView.as_view(), name="crearTarea"),
     path('tarea/modificar/<int:pk>',
          TareaUpdateView.as_view(), name="modificarTarea"),
     path('tarea/eliminar/<int:pk>',
          TareaDeleteView.as_view(), name="eliminarTarea"),
     path('tareas/listar', TareaListView.as_view(), name="listarTareas"),
     path('tareas/exportar',
          exportar_listado_tareas, name='exportarTareas'),

     # ----------------- TIPOS TAREA -----------------

     path('tipo-tarea/crear', TipoTareaCreateView.as_view(), name="crearTipoTarea"),
     path('tipo-tarea/modificar/<int:pk>',
          TipoTareaUpdateView.as_view(), name="modificarTipoTarea"),
     path('tipo-tarea/eliminar/<int:pk>',
          TipoTareaDeleteView.as_view(), name="eliminarTipoTarea"),
     path('tipo-tarea/listar', TipoTareaListView.as_view(), name="listarTipoTarea"),
     path('tipo-tarea/exportar',
          exportar_listado_tipotareas, name='exportarTipoTareas'),
     # ----------------- REPUESTOS -----------------

     path('repuesto/crear', RepuestoCreateView.as_view(), name="crearRepuesto"),
     path('repuestos/listar', RepuestoListView.as_view(), name="listarRepuestos"),
     path('repuesto/modificar/<int:pk>',
          RepuestoUpdateView.as_view(), name="modificarRepuesto"),
     path('repuesto/eliminar/<int:pk>',
          RepuestoDeleteView.as_view(), name="eliminarRepuesto"),
     path('repuestos/exportar',
          exportar_listado_repuestos, name='exportarRepuestos'),
     # ----------------- MODELO -----------------

     path('modelo/crear', ModeloCreateView.as_view(), name="crearModelo"),
     path('modelos/listar', ModeloListView.as_view(), name="listarModelos"),
     path('modelo/modificar/<int:pk>',
          ModeloUpdateView.as_view(), name="modificarModelo"),
     path('modelo/eliminar/<int:pk>',
          ModeloDeleteView.as_view(), name="eliminarModelo"),
     path('modelos/exportar',
          exportar_listado_modelos, name='exportarModelos'),
     # ----------------- MATERIALES -----------------

     path('materiales/listar', MaterialListView.as_view(), name="listarMateriales"),
     path('materiales/crear', MaterialCreateView.as_view(), name="crearMaterial"),
     path('materiales/eliminar/<int:pk>',
          MaterialDeleteView.as_view(), name="eliminarMaterial"),
     path('materiales/modificar/<int:pk>',
          MaterialUpdateView.as_view(), name="modificarMaterial"),
     path('materiales/modificarCantidad',
          MaterialCantidad, name="modificarCantidad"),
     path('materiales/exportar',
          exportar_listado_materiales, name='exportarMateriales'),
     # ----------------- TIPOS MATERIALES -----------------

     path('tipos-materiales/crear', 
          TipoMaterialCreateView.as_view(), name="crearTipoMaterial"),
     path('tipos-materiales/listar', 
          TipoMaterialListView.as_view(), name="listarTipoMateriales"),
     path('tipos-materiales/modificar/<int:pk>',
          TipoMaterialUpdateView .as_view(), name="modificarTipoMaterial"),
     path('tipos-materiales/eliminar/<int:pk>',
          TipoMaterialDeleteView.as_view(), name="eliminarTipoMaterial"),
     path('tipo-materiales/exportar',
          exportar_listado_tipomateriales, name='exportarTipoMateriales'),
     # ----------------- CLIENTES -----------------

     path('clientes/listar', 
          ClienteListView.as_view(), name='listarClientes'),
     path('clientes/crear', 
          ClienteCreateView.as_view(), name='crearCliente'),
     path('clientes/modificar/<int:pk>',
          ClienteUpdateView .as_view(), name="modificarCliente"),
     path('clientes/eliminar/<int:pk>',
          ClienteDeleteView.as_view(), name="eliminarCliente"),
     path('clientes/exportar',
          exportar_listado_clientes, name='exportarClientes'),
     # ----------------- VEHÍCULOS -----------------

     path('vehiculos/listar', 
          VehiculoListView.as_view(), name="listarVehiculos"),
     path('vehiculos/crear', 
          VehiculoCreateView.as_view(), name="crearVehiculo"),
     path('vehiculos/modificar/<int:pk>',
          VehiculoUpdateView.as_view(), name="modificarVehiculo"),
     path('vehiculos/eliminar/<int:pk>',
          VehiculoDeleteView.as_view(), name="eliminarVehiculo"),
     path('vehiculos/exportar',
          exportar_listado_vehiculos, name='exportarVehiculos'),
     # ----------------- EMPLEADOS -----------------

     # path('empleado/registro_usuario/<int:pk>',
     #      RegistrarUsuarioCreateView.as_view(), name="registroEmpleado"),
     path('empleado/imprimir_pdf/<int:pk>',
          imprimirUsuarioEmpleado.as_view(), name="usuarioPDF"),
     path('empleado/registrar',
          EmpleadoCreateView.as_view(), name="crearEmpleado"),
     path('empleado/modificar/<int:pk>',
          EmpleadoUpdateView.as_view(), name="modificarEmpleado"),
     path('empleado/eliminar/<int:pk>',
          EmpleadoDeleteView.as_view(), name="eliminarEmpleado"),
     path('empleados/listar', 
          EmpleadoListView.as_view(), name="listarEmpleados"),
     path('empleados/exportar',
          exportar_listado_empleados, name='exportarEmpleados'),
     path('empleado/asociar_tarea/<int:pk>',
          asociar_tarea_empleado, name='asociarTarea'),
]
