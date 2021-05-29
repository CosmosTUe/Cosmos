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