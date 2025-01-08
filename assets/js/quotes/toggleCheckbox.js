$('#toggleCheckbox').on('change', function () {
    if ($(this).is(':checked')) {
        $('#id_additional_info').show();
    } else {
        $('#id_additional_info').hide();
    }
});