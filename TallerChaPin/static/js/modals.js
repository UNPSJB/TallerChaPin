
const getMensaje = (target, nombre) => {
  switch (target) {
    case "#modalEliminarOrden":
      return `¿Estás seguro/a de querer <strong>Cancelar</strong> la orden de trabajo del cliente "${nombre}"?`
    case "#modalEliminarPresupuesto":
      return `¿Estás seguro/a de querer <strong>Cancelar</strong> el presupuesto del cliente "${nombre}"?`
    case "#modalEliminarPago":
      return `¿Estás seguro/a de querer <strong>eliminar</strong> el pago del cliente "${nombre}"?`
    default:
      return `¿Estás seguro/a de querer <strong>eliminar</strong> "${nombre}" ?`
  }
}

const mostrarModalEliminacion = (e, modal_id) => {
  /* 
    Configura un modal de eliminación con un mensaje en el cuerpo del mismo
    y una URL de navegación para el botón de confirmación.
  */
  const modal_tag = document.getElementById(modal_id);
  // ocultamos el modal para poder configurarlo
  const modal_instance = bootstrap.Modal.getInstance(modal_tag);
  modal_instance.hide();

  // configuramos el contenido del modal
  modal_tag.addEventListener('show.bs.modal', () => {
    const btn = e.currentTarget; // e.currentTarget es el boton al que se le hizo click.
    const url = btn?.dataset.bsUrl;
    const nombre = btn?.dataset.bsNombre;
    const msj = getMensaje(btn?.dataset.bsTarget, nombre)

    // modificamos comportamiento del modal (contenido y acción de confirmación)
    const ok_button = document.getElementById('ok-button');
    ok_button.href = url;
    document.getElementById('modal-msj').innerHTML = msj;
  })

  // mostrarmos el modal
  modal_instance.show()
}

const conectarBotonesAModal = (btn_selector, modal_id) => {
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll(btn_selector).forEach(btn => {
      btn.addEventListener('click', (e) => mostrarModalEliminacion(e, modal_id));
    })
  })
}
