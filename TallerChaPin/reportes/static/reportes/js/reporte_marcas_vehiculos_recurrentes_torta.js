  fetch('reporte_marcas_vehiculos').then(r=>r.json()).then(r=> {

    const config_torta = {
        type: 'pie',
        data: {
          labels: r.vehiculos.map(m => m.nombre),
          datasets: [{
            label: 'Grafico',
            data: r.vehiculos.map(m => m.cantidad),
            backgroundColor: ["#F00","#00F"],
          }]
        },
      };

    const torta = new Chart(
        document.getElementById('torta'),
        config_torta
    );
    console.log(r.vehiculos)
  })
