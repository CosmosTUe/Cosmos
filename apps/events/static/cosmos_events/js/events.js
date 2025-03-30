if (document.readyState == "complete") {
    if (document.getElementById("id_start_date_time")) {
        flatpickr("#id_start_date_time", { enableTime: true, dateFormat: "Y-m-d H:i", time_24hr: true, });
    }
    if (document.getElementById("id_end_date_time")) {
        flatpickr("#id_end_date_time", { enableTime: true, dateFormat: "Y-m-d H:i", time_24hr: true, });
    }
} else{
    window.addEventListener('load', (event) => {
        console.log("event-outside-log")
        if (document.getElementById("id_start_date_time")) {
            flatpickr("#id_start_date_time", { enableTime: true, dateFormat: "Y-m-d H:i", time_24hr: true, });
        }
        if (document.getElementById("id_end_date_time")) {
            flatpickr("#id_end_date_time", { enableTime: true, dateFormat: "Y-m-d H:i", time_24hr: true, });
        }
    });
}