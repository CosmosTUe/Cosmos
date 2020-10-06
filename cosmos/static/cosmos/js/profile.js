window.addEventListener("load", function () {
    $(function () {
        var hash = window.location.hash;
        if (hash) {
            $('.nav-pills a[href="' + hash + '"]').tab('show');
        }
    });

    $('.nav-pills a').on('shown.bs.tab', function (e) {
        history.pushState(null, null, e.target.hash);
    });
});