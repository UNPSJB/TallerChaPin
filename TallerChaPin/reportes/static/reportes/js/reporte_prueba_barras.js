data = [
    {
      nombre: 'Ford',
      cantidad: 10, 
      color: '#010957'
    }, {
      nombre: 'Chevrolet',
      cantidad: 8,
      color: '#C89E4B'
    }, {
      nombre: 'Fiat',
      cantidad: 8,
      color: '#9F022E'
    }, {
      nombre: 'Toyota',
      cantidad: 9,
      color: '#717374'
    }, {
      nombre: 'Nissan',
      cantidad: 2,
      color: '#717374'
    }, {
      nombre: 'Jeep',
      cantidad: 1,
      color: '#211C1E'
    }, {
      nombre: 'Peugeot',
      cantidad: 7,
      color: '#A1A1A1'
    }
]

  
  fetch('reporte_json').then(r=>r.json()).then(r=> {

    const config_barras = {
        type: 'bar',
        data: {
          datasets: [{
            data: r.vehiculos,
            backgroundColor: ["#F00","#00F"]
          }]
        },
        options: {
          parsing: {
            xAxisKey: 'nombre',
            yAxisKey: 'cantidad',
          }
        }
      }
      const barras = new Chart(
        document.getElementById('barras'),
        config_barras
      );
    console.log(r)
  })
