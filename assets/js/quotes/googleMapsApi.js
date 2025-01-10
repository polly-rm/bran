$(document).ready(function () {
    $('#id_postcode_from').on('input', function () {
        const query = $(this).val();
        fetch(`/api/autocomplete/?input=${query}`)
            .then(response => response.json())
            .then(data => {
                const autocompleteAddressFrom = new google.maps.places.Autocomplete(document.getElementById('id_postcode_from'));
            });
    });
    $('#id_postcode_to').on('input', function () {
        const query = $(this).val();
        fetch(`/api/autocomplete/?input=${query}`)
            .then(response => response.json())
            .then(data => {
                const autocompleteAddressFrom = new google.maps.places.Autocomplete(document.getElementById('id_postcode_to'));
            });
    });
});