$(function () {
    $('#datetimepicker1').datetimepicker({
        format: 'DD/MM/YYYY HH:mm',
    });

    $('#datetimepicker2').datetimepicker({
        useCurrent: false,
        format: 'DD/MM/YYYY HH:mm',
    });

    $("#datetimepicker1").on("change.datetimepicker", function (e) {
        const minDate = e.date;
        $('#datetimepicker2').datetimepicker('minDate', minDate);

        // If date_to is already set and now invalid, clear it
        const dateTo = $('#datetimepicker2').datetimepicker('date');
        if (dateTo && dateTo.isBefore(minDate)) {
            $('#datetimepicker2').datetimepicker('date', null);
        }
    });

    $("#datetimepicker2").on("show.datetimepicker", function () {
        const dateFrom = $('#datetimepicker1').datetimepicker('date');
        const dateTo = $('#datetimepicker2').datetimepicker('date');

        if (dateFrom && (!dateTo || dateTo.isBefore(dateFrom))) {
            // If user opens the picker and the current date_to is not valid, suggest a default
            $('#datetimepicker2').datetimepicker('date', dateFrom.clone().add(1, 'hours'));
        }
    });

    $("#datetimepicker2").on("change.datetimepicker", function (e) {
        $('#datetimepicker1').datetimepicker('maxDate', e.date);
    });
});


$(function () {
    $('#datetimepicker3').datetimepicker({
        format: 'DD/MM/YYYY HH:mm',
    });

    $('#datetimepicker4').datetimepicker({
        useCurrent: false,
        format: 'DD/MM/YYYY HH:mm',
    });

    $("#datetimepicker3").on("change.datetimepicker", function (e) {
        const minDate = e.date;
        $('#datetimepicker4').datetimepicker('minDate', minDate);

        // Clear date_to if it's earlier than date_from
        const dateTo = $('#datetimepicker4').datetimepicker('date');
        if (dateTo && dateTo.isBefore(minDate)) {
            $('#datetimepicker4').datetimepicker('date', null);
        }
    });

    $("#datetimepicker4").on("show.datetimepicker", function () {
        const dateFrom = $('#datetimepicker3').datetimepicker('date');
        const dateTo = $('#datetimepicker4').datetimepicker('date');

        if (dateFrom && (!dateTo || dateTo.isBefore(dateFrom))) {
            $('#datetimepicker4').datetimepicker('date', dateFrom.clone().add(1, 'hours'));
        }
    });

    $("#datetimepicker4").on("change.datetimepicker", function (e) {
        $('#datetimepicker3').datetimepicker('maxDate', e.date);
    });
});
