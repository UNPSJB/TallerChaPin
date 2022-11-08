import { months } from './utils.js'

const labels = months({ count: 12 });

const chart = new Chart(document.getElementById("facturacion"), {
  type: 'line',
  data: {
    labels: labels,
    datasets: [{
      data: [86, 114, 106, 106, 107, 111],
      label: "Facturado",
      borderColor: "#3e95cd",
      fill: true
    }, {
      data: [282, 350, 411, 502, 635, 809],
      label: "Pagado",
      borderColor: "#8e5ea2",
      fill: true
    }]
  },
  options: {}
});

const radio_buttons = document.querySelectorAll('.radio_periodo')
let selected_radio = 3
for (let radio of radio_buttons) {
  radio.addEventListener('click', (e) => {
    selected_radio = e.target.value
    console.log(selected_radio)
  })
}

const form = document.getElementById('form_filtros')
const input_desde = document.getElementById('fecha_desde')
const input_hasta = document.getElementById('fecha_hasta')

form.addEventListener('submit', (e) => {
  e.preventDefault()
  fetch(`get_facturacion/${selected_radio},${input_desde.value},${input_hasta.value}`)
    .then(r => r.json())
    .then(r => {
      console.log(r)

      chart.data.datasets[0].data = r.facturado
      chart.data.datasets[1].data = r.pagado
      chart.data.labels = r.labels
      chart.update()

    })
})