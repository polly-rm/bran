function initAutocomplete() {
    const fromInput = document.getElementById('id_postcode_from');
    const toInput = document.getElementById('id_postcode_to');

    if (fromInput) new google.maps.places.Autocomplete(fromInput, {types: ['geocode']});
    if (toInput) new google.maps.places.Autocomplete(toInput, {types: ['geocode']});
}

// Only load Google Maps if inputs exist or map container exists
document.addEventListener('DOMContentLoaded', () => {
    const hasInputs = document.getElementById('id_postcode_from') || document.getElementById('id_postcode_to');
    const mapContainer = document.getElementById('map-container');

    if (hasInputs) {
        // Load Google Maps immediately for autocomplete
        loadGoogleMaps(initAutocomplete);
    } else if (mapContainer) {
        // Lazy load map when it comes into view
        const observer = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting) {
                loadGoogleMaps(); // will still call initAutocomplete, harmless
                observer.disconnect();
            }
        }, {rootMargin: '200px'});

        observer.observe(mapContainer);
    }
});
