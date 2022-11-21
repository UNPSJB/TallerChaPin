  fetch('get_marcas_vehiculos').then(r=>r.json()).then(r=> {

    const config_torta = {
        type: 'pie',
        data: {
          labels: r.vehiculos.map(m => m.nombre),
          datasets: [{
            label: 'Grafico',
            data: r.vehiculos.map(m => m.cantidad),
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

    const torta = new Chart(
        document.getElementById('torta'),
        config_torta
    );

  })
