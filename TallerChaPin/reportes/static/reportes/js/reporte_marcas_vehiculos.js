form = document.getElementById('form_vehiculos')
input_desde = document.getElementById('fecha_desde')
input_hasta = document.getElementById('fecha_hasta')
submit_button = document.getElementById('submit_filtro')
mensaje_error = document.getElementById('error-grafico-vehiculos')

deshabilitar_submit = (e) => {
  const desde = new Date(input_desde.value)
  const hasta = new Date(input_hasta.value)

  if (desde == 'Invalid Date' || hasta == 'Invalid Date') {
    submit_button.setAttribute('disabled', true)
    return
  }

  if (desde > hasta) {
    submit_button.setAttribute('disabled', true)
    return
  }

  submit_button.removeAttribute('disabled')
}
input_desde.addEventListener('change', deshabilitar_submit)
input_hasta.addEventListener('change', deshabilitar_submit)

actualizarDatos = (desde, hasta) => {
  fetch(`get_marcas_vehiculos/${desde},${hasta}`)
    .then(r => r.json())
    .then(r => {
      if(JSON.stringify(r.vehiculos) === '{}') {
        mensaje_error.innerText = `No se encontraron vehículos entre ${input_desde.value} y ${input_hasta.value}.`
        mensaje_error.style.display = 'inline'
      } else {
        mensaje_error.style.display = 'none'
        window.myCharts.data.datasets[0].data = Object.values(r.vehiculos)
        window.myCharts.data.labels = Object.keys(r.vehiculos)
      }
      window.myCharts.update()
    })
}

form.addEventListener('submit', (e) => {
  e.preventDefault()
  actualizarDatos(input_desde.value, input_hasta.value)
})

date_hoy = new Date()
string_hoy = new Date().toISOString().slice(0, 10)
date_30_dias = new Date().setDate(date_hoy.getDate() - 30)
string_30_dias = new Date(date_30_dias).toISOString().slice(0, 10)

window.addEventListener('load', () => {

  const config_torta = {
    type: 'pie',
    data: {
      labels: [],
      datasets: [{
        label: 'Grafico',
        data: [],
        backgroundColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(255, 159, 64, 1)',
          'rgba(255, 205, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(201, 203, 207, 1)',
        ]
      }]
    },
  };

  if (window.myCharts != undefined) {
    window.myCharts.destroy()
  }

  window.myCharts = new Chart(
    document.getElementById('torta-vehiculos'),
    config_torta
  );

  actualizarDatos(string_30_dias, string_hoy)

  input_desde.value = string_30_dias
  input_hasta.value = string_hoy
})
