if (document.getElementById("switchGMMView"))
{
    document.getElementById("switchGMMView").addEventListener("click", function() {
        var table = document.getElementById("GMMTable");
        var grid = document.getElementById("GMMGrid");

        if (table.style.display == "none") {
            table.style.display = "table";
            grid.style.display = "none";
        } else {
            table.style.display = "none";
            grid.style.display = "flex";
        }
    });
}

window.addEventListener('load', (event) => {
    if (document.getElementById("id_date")) {
        flatpickr("#id_date", { enableTime: false, dateFormat: "Y-m-d", time_24hr: true, });
    }
    if (document.getElementById("id_publish_date")) {
        flatpickr("#id_publish_date", { enableTime: false, dateFormat: "Y-m-d", time_24hr: true, });
    }
    if (document.querySelector("#add-form")) {
        let fileForm = document.querySelectorAll(".file-form");
        let container = document.querySelector("#form-container");
        let addButton = document.querySelector("#add-form");
        let totalForms = document.querySelector("#id_has_files-TOTAL_FORMS");

        let formNum = fileForm.length - 1;

        addButton.addEventListener("click", addForm);

        function addForm(e) {
            e.preventDefault();

            fileForm = document.querySelectorAll(".file-form");
            let newForm = fileForm[formNum].cloneNode(true);
            let formRegex = RegExp(`has_files-(\\d){1}-`, `g`);

            formNum++;
            newForm.innerHTML = newForm.innerHTML.replace(formRegex, `has_files-${formNum}-`);
            container.insertBefore(newForm, addButton);

            totalForms.setAttribute("value", `${formNum+1}`);
        }
    }
});