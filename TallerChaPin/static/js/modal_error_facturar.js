// Intento de modal para mostrar advertencias

const mostrarModalWarning = () => {
    /* 
      Configura un modal de advertencia o error con un mensaje en el cuerpo del mismo
      y una URL de navegación para el botón de confirmación.
    */
    const modal_tag = document.getElementById('customModal')
  
    // ocultamos el modal para poder configurarlo
    const modal_instance = bootstrap.Modal.getInstance(modal_tag)
    modal_instance.hide()
  
    // configuramos el contenido del modal
    modal_tag.addEventListener('show.bs.modal', (e) => {
      const btn = e.explicitOriginalTarget
      const mensaje = btn.dataset.bsMensaje
      const msj = mensaje
  
      // modificamos comportamiento del modal (contenido y acción de confirmación)
      const ok_button = document.getElementById('ok-button')
      ok_button.href = url
      document.getElementById('modal-msj').innerHTML = msj
    })
  
    // mostrarmos el modal
    modal_instance.show()
  }
  
  const conectarBotonesAModal = (css_selector) => {
    document.addEventListener('DOMContentLoaded', () => {
      document.querySelectorAll(css_selector).forEach(btn => {
        btn.addEventListener('click',mostrarModalWarning)
      })
    })
  }