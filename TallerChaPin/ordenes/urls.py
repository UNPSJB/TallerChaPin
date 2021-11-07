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
     # ----------------- Presupuesto -----------------
    path('orden/crear', PresupuestoCreateView.as_view(), name="crearPresupuesto"), #No se si haga falta esta vista, supongo que del lado del sistema se genera sola la orden de trabajo
    path('orden/listar', PresupuestoListView.as_view(), name="listarPresupuestos"),
    path('orden/detalle/<int:pk>',
         PresupuestoDetailView.as_view(), name="detallesOrden"),
    path('orden/modificar/<int:pk>',
         PresupuestoUpdateView.as_view(), name="modificarOrden"),
    path('orden/eliminar/<int:pk>',
         PresupuestoDeleteView.as_view(), name="eliminarOrden"), # No se elimina como tal, se cambia el estado a cancelado

]
