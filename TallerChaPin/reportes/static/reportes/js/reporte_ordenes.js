window.addEventListener('load', () => {
    chart = new Chart(document.getElementById("ordenes"), {
        type: 'scatter',
        data: {
            labels: [],
              datasets: [{
                type: 'bar',
                label: 'Bar Dataset',
                data: [],
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)'
              }, {
                type: 'line',
                label: 'Line Dataset',
                data: [],
                fill: false,
                borderColor: 'rgb(54, 162, 235)'
              }]
        },
        options: {}
        
    });
});
