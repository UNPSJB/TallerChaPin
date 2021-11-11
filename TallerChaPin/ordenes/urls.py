from django.urls import path
from .views import *
<<<<<<< Updated upstream
from wkhtmltopdf.views import PDFTemplateView

=======
#from wkhtmltopdf.views import PDFTemplateView




>>>>>>> Stashed changes
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
    path('orden/crear/<int:pk>', OrdenTrabajoCreateView.as_view(), name="crearOrden"), 
    path('orden/listar', OrdenTrabajoListView.as_view(), name="listarOrdenes"),
    path('orden/detalle/<int:pk>',
         OrdenTrabajoDetailView.as_view(), name="detallesOrden"),
    path('orden/modificar/<int:pk>',
         OrdenTrabajoUpdateView.as_view(), name="modificarOrden"),
    path('orden/eliminar/<int:pk>',
         OrdenTrabajoDeleteView.as_view(), name="eliminarOrden"), # No se elimina como tal, se cambia el estado a cancelado
<<<<<<< Updated upstream
     # ------------------ Detalle de Orden de Trabajo -----------------
    path('detalles-orden/listar', DetalleOrdenDeTrabajoListView.as_view(), name="listarDetallesOrden"),
=======

<<<<<<< Updated upstream
>>>>>>> Stashed changes
     # ----------------PDF-------------------------
    path('presupuesto/pdf/<int:pk>', imprimirPresupuesto.as_view(), name='imprimirPresupuesto'),
=======
      #----------------PDF-------------------------
       #   url(r'^pdf/$', PDFTemplateView.as_view(template_name='my_template.html',
        #                                    filename='my_pdf.pdf'), name='pdf'),

     # ----------------- Ordenes y Turnos -----------------
     path ('ordenesTurnos/RegistrarIngresoVehiculo', RegistrarIngresoVehiculoCreateView.as_view(), name="RegistrarIngresoVehiculo")
>>>>>>> Stashed changes
]
