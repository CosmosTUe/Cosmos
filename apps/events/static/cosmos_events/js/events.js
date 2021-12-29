window.addEventListener('load', (event) => {
    console.log("event-outside-log")
    if (document.getElementById("id_start_date_time")) {
        flatpickr("#id_start_date_time", {enableTime: true, dateFormat: "Y-m-d H:i", time_24hr: true,});
    }
    if (document.getElementById("id_end_date_time")) {
        flatpickr("#id_end_date_time", {enableTime: true, dateFormat: "Y-m-d H:i", time_24hr: true,});
    }
});

// https://getbootstrap.com/docs/5.0/forms/validation/#custom-styles
// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation');

    // Loop over them and prevent submission
    forms.forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
})()