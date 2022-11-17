
// Marco el radio button 'tareas taller' como predeterminado
const radio_buttons = document.querySelectorAll('.radio_tipo_tarea')
radio_buttons[0].checked = true

// Si rubro = 'taller' carga datos del taller, lo mismo con 'pintura'
const cargarDatos = (rubro) => {
  chart.data.datasets[0].data = data[rubro].data
  chart.data.datasets[1].data = data[rubro].cantidad
  chart.data.labels = data[rubro].labels
  chart.update()
}

// Cada vez que se clickea un radio button, cambio los datos del gráfico
for (let radio of radio_buttons) {
  radio.addEventListener('click', (e) => {
    
    const seleccionado = e.target.value
    seleccionado == 1 ? cargarDatos('taller') : cargarDatos('pintura')
  })
}

// Defino estructura del objeto con los datos
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

let chart
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

      // Cargo todos los datos necesarios en el objeto 'data'
      for (let d in r.data_taller) {
        data.taller.data.push(r.data_taller[d].promedio)
        data.taller.cantidad.push(r.data_taller[d].cantidad)
        data.taller.labels.push(r.data_taller[d].nombre)
      }

      for (let d in r.data_pintura) {
        data.pintura.data.push(r.data_pintura[d].promedio)
        data.pintura.cantidad.push(r.data_pintura[d].cantidad)
        data.pintura.labels.push(r.data_pintura[d].nombre)
      }
      
      cargarDatos('taller')
    })
})