let chart
window.addEventListener('load', () => {
  // Se crea el gráfico pero sin datos cargados, solo para dejarlo configurado
  chart = new Chart(document.getElementById("chart-clientes"), {
    type: 'scatter',
    data: {
      datasets: [{
        labels: [],
        data: [],
        label: "Clientes comunes",
        borderColor: "rgba(245, 39, 50, 0.8)",
        backgroundColor: "rgba(245, 39, 50, 0.8)",
      }, {
          labels: [],
          data: [],
          label: "Clientes VIP",
          borderColor: "rgba(32, 8, 210, 0.8)",
          backgroundColor: "rgba(32, 8, 210, 0.8)",
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        tooltip: {
          callbacks: {
            label: function (ctx) {
              let label = ctx.dataset.labels[ctx.dataIndex];
              label += " (" + ctx.parsed.x + " órdenes, $" + ctx.parsed.y + ")";
              return label;
            }
          }
        }
      },
      scales: {
        y: {
            beginAtZero: true,
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
          beginAtZero: true,
          ticks: {
            stepSize: 1
          },
          title: {
            text: 'Cantidad de órdenes registradas',
            display: true,
          },
        }
      }
    }
  });

  fetch(`get_clientes`)
    .then(r => r.json())
    .then(r => {
      const data = {'clientes': [], 'clientes_vip': []}
      const labels = { 'clientes': [], 'clientes_vip': [] }
      for (let c in r.d_clientes) {
        if (r.d_clientes[c].vip) {
          labels.clientes_vip.push(r.d_clientes[c].nombre)
          data.clientes_vip.push([r.d_clientes[c].cantidad, r.d_clientes[c].facturado])
        } else {
          labels.clientes.push(r.d_clientes[c].nombre)
          data.clientes.push([r.d_clientes[c].cantidad, r.d_clientes[c].facturado])
        }
      }

      chart.data.datasets[0].data = data.clientes
      chart.data.datasets[0].labels = labels.clientes
      chart.data.datasets[1].data = data.clientes_vip
      chart.data.datasets[1].labels = labels.clientes_vip
      chart.update()      
    })
})