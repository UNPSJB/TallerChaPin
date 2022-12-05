import { loadTable } from "./utils.js"
let chart

// Marco el radio button 'Diario' como predeterminado
const radio_buttons = document.querySelectorAll('.radio_periodo')
let selected_radio = 1
radio_buttons[0].checked = true

// Cada vez que se clickea un radio button, 'selected_radio' se modifica
for (let radio of radio_buttons) {
  radio.addEventListener('click', (e) => {
    selected_radio = e.target.value
  })
}

const form = document.getElementById('form_filtros_facturacion')
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


const actualizarTabla = (data) => {

  console.log(data)

  const rows = []
  for (let d in data.labels) {
    rows.push([data.labels[d], `$${data.facturado[d]}`, `$${data.pagado[d]}`])
  }

  console.log(rows)
  loadTable(['Fecha', 'Facturación acumulada', 'Pagos acumulados'], rows)
}

const actualizarDatos = (temporalidad, desde, hasta) => {
  fetch(`get_facturacion/${temporalidad},${desde},${hasta}`)
  .then(r => r.json())
  .then(r => {
    chart.data.datasets[0].data = r.facturado
    chart.data.datasets[1].data = r.pagado
    chart.data.labels = r.labels
    chart.update()
    actualizarTabla(r)
  })
}

form.addEventListener('submit', (e) => {
  e.preventDefault()
  actualizarDatos(selected_radio, input_desde.value, input_hasta.value)
})

window.addEventListener('load', () => {

  // Se crea el gráfico pero sin datos cargados, solo para dejarlo configurado
  chart = new Chart(document.getElementById("facturacion"), {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        data: [],
        label: "Facturado",
        borderColor: "rgba(43, 57, 231, 0.8)",
        backgroundColor: "rgba(43, 57, 231, 0.3)",
        fill: true
      }, {
        data: [],
        label: "Pagado",
        borderColor: "rgba(18, 165, 13, 0.8)",
        backgroundColor: "rgba(18, 165, 13, 0.3)",
        fill: true
      }]
    },
    options: {
      scales: {
        y: {
          title: {
            text: 'Cantidad facturada',
            display: true,
          },
          ticks: {
            callback: function (value, index, ticks) {
              return '$' + value;
            }
          }
        },
      x: {
        title: {
          text: 'Fecha',
          display: true,
        }
      }
      }, 
    }
  });

  
  const date_hoy = new Date()
  const string_hoy = date_hoy.toISOString().slice(0, 10)

  const date_30_dias = new Date().setDate(date_hoy.getDate() - 30)
  const string_30_dias = new Date(date_30_dias).toISOString().slice(0, 10)

  // Se carga con la vista diaria de los últimos 30 días (por defecto)
  actualizarDatos("1", string_30_dias, string_hoy)
  input_desde.value = string_30_dias
  input_hasta.value = string_hoy
})