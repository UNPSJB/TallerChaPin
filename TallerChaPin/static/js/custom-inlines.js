$(document).ready(() => {
    const prefix = 'presupuesto_materiales';
    const totalForms = $("#id_" + prefix + "-TOTAL_FORMS").prop("autocomplete", "off");
    let nextIndex = parseInt(totalForms.val(), 10);
    const maxForms = $("#id_" + prefix + "-MAX_NUM_FORMS").prop("autocomplete", "off");
    const minForms = $("#id_" + prefix + "-MIN_NUM_FORMS").prop("autocomplete", "off");

    const updateElementIndex = function(el, prefix, ndx) {
        const id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
        const replacement = prefix + "-" + ndx;
        if ($(el).prop("for")) {
            $(el).prop("for", $(el).prop("for").replace(id_regex, replacement));
        }
        if (el.id) {
            el.id = el.id.replace(id_regex, replacement);
        }
        if (el.name) {
            el.name = el.name.replace(id_regex, replacement);
        }
        return el
    };
    console.log(minForms, maxForms, nextIndex, totalForms)

    console.log(updateElementIndex($('.d-none.empty-form'), prefix, 0).html())

})