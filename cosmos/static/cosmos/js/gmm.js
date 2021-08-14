window["switchGMMView"] = function()
{
    var table = document.getElementById("GMMTable");
    var grid = document.getElementById("GMMGrid");

    if (table.style.display == "none")
    {
        table.style.display = "table";
        grid.style.display = "none";
    } else
    {
        table.style.display = "none";
        grid.style.display = "flex";
    }
}

window.onload = function() {
    if (document.getElementById("id_date")) {
        var dialog = new mdDateTimePicker.default({
            type: "date",
            future: moment().add(3, 'months'),
            trigger: document.getElementById("id_date")
        });

        document.getElementById("id_calendar_button").addEventListener('click', function() {
            dialog.toggle();
        });

        document.getElementById("id_date").addEventListener('onOk', function() {
            this.value = dialog.time._d.toISOString().split('T')[0];
        });
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
};