
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
window.addEventListener('load', () => {

  // Se crea el gráfico pero sin datos cargados, solo para dejarlo configurado
  chart = new Chart(document.getElementById("horas-trabajo"), {
    type: 'bar',
    data: {
      labels: ['pepe', 'pepito', 'manuel', 'manolito'],
      datasets: [{
        data: [10, 15, 12, 10],
        label: "Horas de trabajo promedio",
        borderColor: "rgba(43, 57, 231, 0.8)",
        backgroundColor: "rgba(43, 57, 231, 0.3)",
      }]
    },
    options: {}
  });
})