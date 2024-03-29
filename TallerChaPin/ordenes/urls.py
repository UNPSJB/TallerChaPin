from django.urls import path
from .views import *
from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [
     path('presupuesto/tareas/requerimientos', requerimientos_tareas, name='requerimientos_tareas'),
     path('presupuesto/ampliar/tareas/requerimientos', requerimientos_tareas, name='requerimientos_tareas'),
     path('presupuesto/modificar/tareas/requerimientos', requerimientos_tareas, name='requerimientos_tareas'),
     # ----------------- Presupuesto -----------------
     path('presupuesto/crear', PresupuestoCreateView.as_view(),
          name="crearPresupuesto"),
     path('presupuesto/listar', PresupuestoListView.as_view(),
          name="listarPresupuestos"),
     path('presupuesto/detalle/<int:pk>',
          PresupuestoDetailView.as_view(), name="detallesPresupuesto"),
     path('presupuesto/modificar/<int:pk>',
          PresupuestoUpdateView.as_view(), name="modificarPresupuesto"),
     path('presupuesto/eliminar/<int:pk>',
          PresupuestoDeleteView.as_view(), name="eliminarPresupuesto"),
     path('presupuesto/ampliar/<int:pk>',
          PresupuestoCreateView.as_view(), name="ampliarPresupuesto"),
     path('presupuesto/confirmarAmpliacion/<int:pk>', confirmar_ampliacion, name="confirmarAmpliacion"),
     path('presupuesto/tareasFinalizadas/<int:pk>', tareasFinalizadas, name="tareasFinalizadas"),
     path('presupuestos/exportar',
          exportar_listado_presupuestos, name='exportarPresupuestos'),
     path('presupuestos/getRepuestos/<int:pk_vehiculo>', get_repuestos_modelo),
      path('presupuestos/getRepuestosAmpliacion/<int:pk_presupuesto>', get_repuestos_modelo_ampliacion),
     
     # ------------------ Orden de Trabajo -----------------
     path('orden/crear/<int:pk>', OrdenTrabajoCreateView.as_view(), name="crearOrden"),
     path('orden/listar', OrdenTrabajoListView.as_view(), name="listarOrdenes"),
     path('orden/detalle/<int:pk>',
          OrdenTrabajoDetailView.as_view(), name="detallesOrden"),
     path('orden/modificar/<int:pk>',
          OrdenTrabajoUpdateView.as_view(), name="modificarOrden"),
     path('orden/cancelar/<int:pk>',
          cancelar_orden, name="cancelarOrden"), 
     path('orden/pausar/<int:pk>', pausar_orden, name='pausarOrden'), 
     path('orden/reanudar/<int:pk>', reanudar_orden, name='reanudarOrden'),
     path('ordenes/exportar',
          exportar_listado_ordenes, name='exportarOrdenes'),
     # ------------------ Detalle de Orden de Trabajo -----------------
     path('detalles-orden/listar', DetalleOrdenDeTrabajoListView.as_view(),
          name="listarDetallesOrden"),
     path('detalles-orden/iniciar/<int:pk>',
          iniciar_tarea, name="iniciarTarea"),
     path('detalles-orden/cantidad',
         asignar_cantidad, name="asignarCantidad"),
     path('detalles-orden/asignar_empleado',
         asignar_empleado, name="asignarEmpleado"),
     path('detalles-orden/finalizar',
          finalizar_tarea, name="finalizarTarea"),
     path('detalles-orden/resumen/<int:pk>',
         resumen_orden, name="resumenOrden"),
     # ------------------ Planilla de pintura ----------------- 
     path('detalles-orden/<int:detalle>/planilla/crear',
          PlanillaCreateView.as_view(), name="cargarPlanillaParaTarea"),
     path('planilla/modificar/<int:pk>',
          PlanillaUpdateView.as_view(), name="modificarPlanilla"),
     path('planilla/eliminar/<int:pk>',
          PlanillaDeleteView, name="eliminarPlanilla"),
     # ----------------- Ingreso y Entrega de vehiculo -----------------
     path('ordenesTurnos/registrarIngresoVehiculo',
          RegistrarIngresoVehiculoCreateView.as_view(), name="registrarIngresoVehiculo"),
     path('ordenesTurnos/registrarIngresoVehiculo/<int:pk>',
          RegistrarIngresoVehiculoCreateView.as_view(), name="registrarIngresoVehiculo"),
     path('ordenesTurnos/registrarEgresoVehiculo',
          RegistrarEgresoVehiculoCreateView.as_view(), name="registrarEgresoVehiculo"),
     path('ordenesTurnos/registrarEgresoVehiculo/<int:pk>',
          RegistrarEgresoVehiculoCreateView.as_view(), name="registrarEgresoVehiculo"),
     # ----------------- Turnos -------------------
     path('ordenesTurnos/listarTurnos',
          ListarTurnosListView.as_view(), name="calendarioTurnos"),
     path('ordenesTurnos/listarTurnos/detalleTurno/<int:pk>',datoPlantilla, name="datoPlantilla"),
     # ----------------PDF-------------------------
     path('presupuesto/pdf/<int:pk>', imprimirPresupuesto.as_view(),
          name='imprimirPresupuesto'),
     path('orden/pdf/<int:pk>', imprimirOrdenDeTrabajo.as_view(),
          name='imprimirOrden')
]
