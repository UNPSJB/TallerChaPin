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

const linea_media = (media, cantidad) =>
{
  const lista = []
  for (let i = 0; i<cantidad; i++){
    lista.push(media)
  } 
  return lista
}



const actualizarDatos = (desde, hasta) => {
  fetch(`get_ordenes/${desde},${hasta}`)
  .then(r => r.json())
  .then(r => {
    chart.data.datasets[0].data = r.duracion_orden
    chart.data.datasets[1].data = linea_media(r.media, r.label.length)
    chart.data.labels = r.labels
    chart.update()
  })
}
 
form.addEventListener('submit', (e) => {
  e.preventDefault()
  actualizarDatos(input_desde.value, input_hasta.value)
})
 
window.addEventListener('load', () => {
  Chart.defaults.font.size = 12;
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
                borderColor: 'rgb(54, 162, 235)',
                pointHitRadius: 0
              }]
        },
        options: {}
       
    });

    const date_hoy = new Date()
    const string_hoy = date_hoy.toISOString().slice(0, 10)
  
    const date_30_dias = new Date().setDate(date_hoy.getDate() - 30)
    const string_30_dias = new Date(date_30_dias).toISOString().slice(0, 10)
  
    // Se carga con la vista diaria de los últimos 30 días (por defecto)
    actualizarDatos(string_30_dias, string_hoy)
    input_desde.value = string_30_dias
    input_hasta.value = string_hoy
});
 
