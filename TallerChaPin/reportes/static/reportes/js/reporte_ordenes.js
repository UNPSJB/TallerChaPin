let chart
 
const form = document.getElementById('form_filtros')
const input_desde = document.getElementById('fecha_desde')
const input_hasta = document.getElementById('fecha_hasta')
const submit_button = document.getElementById('submit_filtro')
 
const deshabilitar_submit = (e) => {
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
 
const actualizarDatos = (desde, hasta) => {
  fetch(`get_ordenes/${desde},${hasta}`)
  .then(r => r.json())
  .then(r => {
    chart.data.datasets[0].data = r.dias_orden
    chart.data.datasets[1].data = r.media
    chart.data.labels = r.labels
    chart.update()
  })
}
 
form.addEventListener('submit', (e) => {
  e.preventDefault()
  actualizarDatos(input_desde.value, input_hasta.value)
})
 
window.addEventListener('load', () => {
  Chart.defaults.font.size = 16;
    chart = new Chart(document.getElementById("ordenes"), {
        type: 'scatter',
        data: {
            labels: [],
              datasets: [{
                type: 'bar',
                label: 'Ordenes',
                data: [],
                borderColor: 'rgb(151, 91, 235)',
                backgroundColor: 'rgba(151, 91, 235, 0.2)'
              }, {
                type: 'line',
                label: 'Media de tiempo',
                data: [],
                fill: false,
                borderColor: 'rgb(54, 162, 235)'
              }]
        },
        options: {}
       
    });
});
 
