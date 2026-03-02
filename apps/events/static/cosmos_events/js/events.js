// TODO: Fix date picker
// if (document.readyState == "complete") {
//     console.log("doc-already-complete")
//     if (document.getElementById("id_start_date_time")) {
//         flatpickr("#id_start_date_time", { enableTime: true, dateFormat: "Y-m-d H:i", time_24hr: true, });
//     }
//     if (document.getElementById("id_end_date_time")) {
//         flatpickr("#id_end_date_time", { enableTime: true, dateFormat: "Y-m-d H:i", time_24hr: true, });
//     }
// } else{
//     window.addEventListener('load', (event) => {
//         console.log("event-outside-log")
//         if (document.getElementById("id_start_date_time")) {
//             flatpickr("#id_start_date_time", { enableTime: true, dateFormat: "Y-m-d H:i", time_24hr: true, });
//         }
//         if (document.getElementById("id_end_date_time")) {
//             flatpickr("#id_end_date_time", { enableTime: true, dateFormat: "Y-m-d H:i", time_24hr: true, });
//         }
//     });
// }

document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("past-events-container");
    const loader = document.getElementById("past-events-loader");

    if (!container) return;

    let page = parseInt(container.dataset.nextPage, 10);
    let hasNext = container.dataset.hasNext === "true";
    let loading = false;
    let failed = false;

    function loadMorePastEvents() {
        if (!hasNext || loading || failed) return;

        loading = true;
        loader.style.display = "block";

        fetch(`/events/past/?page=${page}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Server error");
            }
            return response.json();
        })
        .then(data => {
            container.insertAdjacentHTML("beforeend", data.html);
            hasNext = data.has_next;
            page += 1;
        })
        .catch(err => {
            console.error("Infinite scroll failed:", err);
            failed = true; // 🔒 STOP retry loop
        })
        .finally(() => {
            loading = false;
            loader.style.display = "none";
        });
    }

    window.addEventListener("scroll", () => {
        const nearBottom =
            window.innerHeight + window.scrollY >=
            document.body.offsetHeight - 300;

        if (nearBottom) {
            loadMorePastEvents();
        }
    });
});