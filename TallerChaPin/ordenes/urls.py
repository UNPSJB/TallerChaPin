from django.urls import path
from .views import *


urlpatterns = [
    # ----------------- Presupuesto -----------------
     # path('/',)
    path('presupuesto/crear', PresupuestoCreateView.as_view(), name="crearPresupuesto"),
    path('presupuesto/listar', PresupuestoListView.as_view(), name="listarPresupuestos"),
    path('presupuesto/detalle/<int:pk>',
         PresupuestoDetailView.as_view(), name="detallesPresupuesto"),
    path('presupuesto/modificar/<int:pk>',
         PresupuestoUpdateView.as_view(), name="modificarPresupuesto"),
    path('presupuesto/eliminar/<int:pk>',
         PresupuestoDeleteView.as_view(), name="eliminarPresupuesto"),
     # ------------------ Orden de Trabajo -----------------
    path('orden/crear', OrdenTrabajoCreateView.as_view(), name="crearOrden"), 
    path('orden/listar', OrdenTrabajoListView.as_view(), name="listarOrdenes"),
    path('orden/detalle/<int:pk>',
         OrdenTrabajoDetailView.as_view(), name="detallesOrden"),
    path('orden/modificar/<int:pk>',
         OrdenTrabajoUpdateView.as_view(), name="modificarOrden"),
    path('orden/eliminar/<int:pk>',
         OrdenTrabajoDeleteView.as_view(), name="eliminarOrden"), # No se elimina como tal, se cambia el estado a cancelado

]
