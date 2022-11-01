const updateElementIndex = function (el, prefix, ndx) {
  const id_regex = new RegExp('(' + prefix + '-(\\d+|__prefix__))');
  const replacement = prefix + '-' + ndx;
  if ($(el).prop('for')) {
    $(el).prop('for', $(el).prop('for').replace(id_regex, replacement));
  }
  if (el.id) {
    el.id = el.id.replace(id_regex, replacement);
  }
  if (el.name) {
    el.name = el.name.replace(id_regex, replacement);
  }
};

function getQuitarButton(){
  button = document.createElement('a')
  button.classList.add('quitar')
  button.setAttribute('href', '#')
  button.appendChild(document.createTextNode('Quitar'))
  return button
}

const addInlineDeleteButton = function (row, prefix) {
  fila = row[0]
  hijos = Array.from(fila.childNodes)
  td_quitar = hijos.filter(n => n.id?.includes("DELETE"))[0]
  td_quitar.appendChild(getQuitarButton())

  row.find('a.quitar').on('click', function (event) {
    inlineDeleteHandler(event, prefix);
  });
  
};


const inlineDeleteHandler = function (e1, prefix) {
  e1.preventDefault();
  const deleteButton = $(e1.target);
  const row = deleteButton.closest('tr');
  const tbody = deleteButton.closest('tbody');
  const trs = $('tr', tbody);
  row.remove();
  
  $('#id_' + prefix + '-TOTAL_FORMS').val(trs.length);

  $('tr', tbody).each(function (i, tr) {
    updateElementIndex($(tr), prefix, i - 1);
    $(tr)
      .find('*')
      .each(function (j, e) {
        updateElementIndex(e, prefix, i - 1);
      });
  });
};

const inlineFormset = function ($context) {
  const prefix = $context.data('formset');
  console.log(`El prefix es ${prefix}`)
  const row = $('.d-none.empty-form', $context).clone(true);
  const table = $('.d-none.empty-form', $context).parents('table');
  const tbody = $('tbody', table);
  
  const agregarRenglon = $('<tfoot><tr><td colspan="4"><a class="btn btn-sm btn-outline-primary ">Agregar</a></td></tr></tfoot>');
  
  $('a', agregarRenglon).click(() => {
    const totalForms = $('#id_' + prefix + '-TOTAL_FORMS').prop('autocomplete', 'off');
    console.log('totalForms', totalForms.val());
    let nextIndex = Number(totalForms.val());
    const newRow = row.clone(true);

    addInlineDeleteButton(newRow, prefix);
    newRow.removeClass('d-none empty-form');
    newRow.find('*').each(function (index, el) {
      updateElementIndex(el, prefix, nextIndex);
    });

    $(tbody).append(newRow);
    const trs = $('tr', tbody);

    $('#id_' + prefix + '-TOTAL_FORMS').val(trs.length);
  });
  
  table.append(agregarRenglon);
};

// Go bitch!
$(document).ready(() => {
  $('[data-formset]').each(function (index, el) {
    $('.checkboxinput').remove(); // quita el checkbox 
    
    inlineFormset($(el));
  });
  
});
