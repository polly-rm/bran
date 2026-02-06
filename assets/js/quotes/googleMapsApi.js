window.initAutocomplete = function () {
    const from = document.getElementById('id_postcode_from');
    const to = document.getElementById('id_postcode_to');

    if (from && !from.dataset.autocomplete) {
        new google.maps.places.Autocomplete(from, {
            types: ['geocode'],
            componentRestrictions: {country: 'uk'}
        });
        from.dataset.autocomplete = "true";
    }

    if (to && !to.dataset.autocomplete) {
        new google.maps.places.Autocomplete(to, {
            types: ['geocode'],
            componentRestrictions: {country: 'uk'}
        });
        to.dataset.autocomplete = "true";
    }
};