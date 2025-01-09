document.getElementById("submit-btn").addEventListener("click", function (event) {
    // Get all forms in the formset
    const formsetForms = document.querySelectorAll(".cargo-form");

    // Check if there is only one form in the formset
    if (formsetForms.length === 1) {
        console.log('1 forma')
        const fields = formsetForms[0].querySelectorAll("input");

        // Check if all fields are empty
        const allEmpty = Array.from(fields).every(field => field.value.trim() === "");
        const errorMessage = document.getElementById("error-message");

        if (allEmpty) {
            event.preventDefault(); // Prevent form submission
            errorMessage.style.display = "block"; // Show the error message
        } else {
            errorMessage.style.display = "none"; // Show the error message
        }
    }
});