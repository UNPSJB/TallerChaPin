document.addEventListener('DOMContentLoaded', (event) => {
  const url = new URL(window.location.href);
  // Obtengo "orden" de la url y prepara el array de campos que aplican el ordenamiento
  const urlOrden = url.searchParams.get("orden") || "";
  let orden = urlOrden.trim() !== "" ? urlOrden.split(",") : [];
  const ths = document.querySelectorAll('table.sortable th.sortable');

  // Iteramos sobre los th y ponemos el click
  ths.forEach(th => {
    const field = th.dataset.sField;
    const nombre = th.textContent;
    const i = orden.indexOf(field) + 1;
    const j = orden.indexOf(`-${field}`) + 1;
    if (orden.includes(field)) {
      th.innerHTML = `${nombre}&nbsp;<small>${i}</small>&nbsp;<i class="fas fa-sort-up"></i>`;
    } else if (orden.includes(`-${field}`)) {
      th.innerHTML = `${nombre}&nbsp;<small>${j}</small>&nbsp;<i class="fas fa-sort-down"></i>`;
    }

    th.addEventListener("click", (event) => {
      const field = event.target.dataset.sField;
      if (orden.includes(field) || orden.includes("-" + field)) {
        if (orden.includes(field)) {
          orden = orden.filter(o => o !== field);
          orden.push(`-${field}`);
        } else if (orden.includes(`-${field}`)) {
          orden = orden.filter(o => o !== `-${field}`);
        }
      } else {
        orden.push(field);
      }
      console.log(orden);
      url.searchParams.set('orden', orden.join(","));
      window.location.href = decodeURIComponent(url.href);
    });
  });

});