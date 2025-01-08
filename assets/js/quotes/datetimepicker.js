$(function () {
    $('#datetimepicker1').datetimepicker({
        format: 'DD/MM/YYYY HH:mm',
    });
    $('#datetimepicker2').datetimepicker({
        useCurrent: false,
        format: 'DD/MM/YYYY HH:mm',
    });
    $("#datetimepicker1").on("change.datetimepicker", function (e) {
        $('#datetimepicker2').datetimepicker('minDate', e.date);
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
        $('#datetimepicker4').datetimepicker('minDate', e.date);
    });
    $("#datetimepicker4").on("change.datetimepicker", function (e) {
        $('#datetimepicker3').datetimepicker('maxDate', e.date);
    });
});