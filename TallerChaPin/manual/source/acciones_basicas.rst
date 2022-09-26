Acciones básicas sobre las entidades de la aplicación
=====================================================

Para el control de los datos de la aplicación, se requiere la creación de distintas entidades, las cuales son:

- Clientes.
- Vehículos.
- Empleados.
- Marcas.
- Modelos.
- Materiales.
- Tipos de materiales.
- Repuestos.
- Tareas.
- Tipos de tarea.
- Presupuestos.
- Ordenes de trabajo.
- Detalles de órdenes de trabajo.
- Facturas.
- Pagos.

Todas ellas poseen distintas acciones básicas, como lo son la **creación**, **modificación** y **eliminación**. 
A continuación se detallará la forma de realizar cada una de estas operaciones en forma general.

********
Creación
********

+-----------------------------+-------------------------------------------------------+
| Entidad                     | Forma de creación                                     |
+=============================+=======================================================+
| Cliente                     | Taller > Registrar cliente                            |
+-----------------------------+-------------------------------------------------------+
| Vehículo                    | Taller > Registrar vehículo                           |
+-----------------------------+-------------------------------------------------------+
| Empleado                    | Taller > Registrar empleado                           |
+-----------------------------+-------------------------------------------------------+
| Marca                       | Taller > Marcas > Registrar una marca                 |
+-----------------------------+-------------------------------------------------------+
| Modelo                      | Taller > Modelos > Registrar un modelo                |
+-----------------------------+-------------------------------------------------------+
| Material                    | Taller > Registrar material                           |
+-----------------------------+-------------------------------------------------------+
| Tipo de material            | Taller > Materiales > Registrar un tipo de material   |
+-----------------------------+-------------------------------------------------------+
| Repuesto                    | Taller > Registrar repuesto                           |
+-----------------------------+-------------------------------------------------------+
| Tarea                       | Taller > Crear tarea                                  |
+-----------------------------+-------------------------------------------------------+
| Tipo de tarea               | Taller > Tareas > Registrar un tipo de tarea          |
+-----------------------------+-------------------------------------------------------+
| Presupuesto                 | Presupuestos > Crear presupuesto                      |
+-----------------------------+-------------------------------------------------------+
| Orden de trabajo            | Se crea automáticamente al confirmar un presupuesto.  |
+-----------------------------+-------------------------------------------------------+
| Detalle de orden de trabajo | Se crea junto con la orden de trabajo.                |
+-----------------------------+-------------------------------------------------------+
| Factura                     | Se crea al facturar una orden.                        |
+-----------------------------+-------------------------------------------------------+
| Pago                        | Se crea al pagar una factura.                         |
+-----------------------------+-------------------------------------------------------+

************
Modificación
************

+-----------------------------+---------------------------------------------------------+
| Entidad                     | Forma de modificación                                   |
+=============================+=========================================================+
| Cliente                     | Listados > ver clientes > *sìmbolo de editar*           |
+-----------------------------+---------------------------------------------------------+
| Vehículo                    | Listados > ver vehículos > *sìmbolo de editar*          |
+-----------------------------+---------------------------------------------------------+
| Empleado                    | Listados > ver empleados > *sìmbolo de editar*          |
+-----------------------------+---------------------------------------------------------+
| Marca                       | Listados > ver marcas > *sìmbolo de editar*             |
+-----------------------------+---------------------------------------------------------+
| Modelo                      | Listados > ver modelos > *sìmbolo de editar*            |
+-----------------------------+---------------------------------------------------------+
| Material                    | Listados > ver materiales > *sìmbolo de editar*         |
+-----------------------------+---------------------------------------------------------+
| Tipo de material            | Listados > ver tipos de material > *sìmbolo de editar*  |
+-----------------------------+---------------------------------------------------------+
| Repuesto                    | Listados > ver repuestos > *sìmbolo de editar*          |
+-----------------------------+---------------------------------------------------------+
| Tarea                       | Listados > ver tareas > *sìmbolo de editar*             |
+-----------------------------+---------------------------------------------------------+
| Tipo de tarea               | Listados > ver tipos de tarea > *sìmbolo de editar*     |
+-----------------------------+---------------------------------------------------------+
| Presupuesto                 | Ver :ref:`modificar-presupuesto`.                       |
+-----------------------------+---------------------------------------------------------+
| Orden de trabajo            | Ver :ref:`ampliar-presupuesto`.                         |
+-----------------------------+---------------------------------------------------------+
| Detalle de orden de trabajo | *Acción no disponible*                                  |
+-----------------------------+---------------------------------------------------------+
| Factura                     | *Acción no disponible*                                  |
+-----------------------------+---------------------------------------------------------+
| Pago                        | *Acción no disponible*                                  |
+-----------------------------+---------------------------------------------------------+

************
Eliminación
************

+-----------------------------+-----------------------------------------------------------+
| Entidad                     | Forma de eliminación                                      |
+=============================+===========================================================+
| Cliente                     | Listados > ver clientes > *sìmbolo de eliminar*           |
+-----------------------------+-----------------------------------------------------------+
| Vehículo                    | Listados > ver vehículos > *sìmbolo de eliminar*          |
+-----------------------------+-----------------------------------------------------------+
| Empleado                    | Listados > ver empleados > *sìmbolo de eliminar*          |
+-----------------------------+-----------------------------------------------------------+
| Marca                       | Listados > ver marcas > *sìmbolo de eliminar*             |
+-----------------------------+-----------------------------------------------------------+
| Modelo                      | Listados > ver modelos > *sìmbolo de eliminar*            |
+-----------------------------+-----------------------------------------------------------+
| Material                    | Listados > ver materiales > *sìmbolo de eliminar*         |
+-----------------------------+-----------------------------------------------------------+
| Tipo de material            | Listados > ver tipos de material > *sìmbolo de eliminar*  |
+-----------------------------+-----------------------------------------------------------+
| Repuesto                    | Listados > ver repuestos > *sìmbolo de eliminar*          |
+-----------------------------+-----------------------------------------------------------+
| Tarea                       | Listados > ver tareas > *sìmbolo de eliminar*             |
+-----------------------------+-----------------------------------------------------------+
| Tipo de tarea               | Listados > ver tipos de tarea > *sìmbolo de eliminar*     |
+-----------------------------+-----------------------------------------------------------+
| Presupuesto                 | Ver :ref:`cancelar-presupuesto`.                          |
+-----------------------------+-----------------------------------------------------------+
| Orden de trabajo            | Ver **cancelar orden**                                    |
+-----------------------------+-----------------------------------------------------------+
| Detalle de orden de trabajo | *Acción no disponible*                                    |
+-----------------------------+-----------------------------------------------------------+
| Factura                     | Listados > ver facturas > *sìmbolo de eliminar*           |
+-----------------------------+-----------------------------------------------------------+
| Pago                        | Listados > ver pagos > *sìmbolo de eliminar*              |
+-----------------------------+-----------------------------------------------------------+