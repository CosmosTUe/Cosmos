function switchGMMView()
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
    if (document.getElementById("id_date") != null) {
        var dialog = new mdDateTimePicker.default({
            type: "date",
            trigger: document.getElementById("id_date")
        });

        document.getElementById("id_date").addEventListener('click', function() {
            dialog.toggle();
        });

        document.getElementById("id_date").addEventListener('onOk', function() {
            this.value = dialog.time._d.toISOString().split('T')[0];
        });
    }
};