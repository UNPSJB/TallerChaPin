from django.urls import path
from .views import *
from django.conf.urls.defaults import url, patterns
from wkhtmltopdf.views import PDFTemplateView

urlpatterns = patterns('',

)

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

     # ----------------PDF-------------------------
     #     url(r'^pdf/$', PDFTemplateView.as_view(template_name='my_template.html',
     #                                       filename='my_pdf.pdf'), name='pdf'),
]
