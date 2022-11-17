
// Marco el radio button 'tareas taller' como predeterminado
const radio_buttons = document.querySelectorAll('.radio_tipo_tarea')
let selected_radio = 1
radio_buttons[0].checked = true

// Cada vez que se clickea un radio button, 'selected_radio' se modifica
for (let radio of radio_buttons) {
  radio.addEventListener('click', (e) => {
    selected_radio = e.target.value
  })
}

let chart
const data = 
{ 
  taller: { 
    data: [], 
    labels: [], 
    cantidad: [] 
  }, pintura: { 
    data: [], 
    labels: [], 
    cantidad: [] 
  }
}

window.addEventListener('load', () => {
  // Se crea el gráfico pero sin datos cargados, solo para dejarlo configurado
  chart = new Chart(document.getElementById("horas-trabajo"), {
    type: 'bar',
    data: {
      labels: [],
      datasets: [{
        data: [],
        label: "Horas de trabajo promedio",
        borderColor: "rgba(245, 39, 50, 0.8)",
        backgroundColor: "rgba(245, 39, 50, 0.8)",
        yAxisID: 'y',
      }, {
          data: [],
          label: "Tareas completadas",
          borderColor: "rgba(71, 245, 39, 0.8)",
          backgroundColor: "rgba(71, 245, 39, 0.8)",
          yAxisID: 'y1',
        }]
    },
    options: {
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
        }
    }
  }});

  fetch(`get_horas_trabajo`)
    .then(r => r.json())
    .then(r => {
      console.log(r)

      for (let d in r.data_taller) {
        data.taller.data.push(r.data_taller[d].promedio)
        data.taller.cantidad.push(r.data_taller[d].cantidad)
        data.taller.labels.push(r.data_taller[d].nombre)
      }

      chart.data.datasets[0].data = data.taller.data
      chart.data.datasets[1].data = data.taller.cantidad
      chart.data.labels = data.taller.labels
      chart.update()
    })
})