
window["addCalendar"] = function(type, id_date_time, id_calendar_button ) {
    if (document.getElementById(id_date_time)) {
        var dialog = new mdDateTimePicker.default({
            type: type,
            // future: moment().add(3, 'months'),
            trigger: document.getElementById(id_date_time)
        });
        console.log(type)
        console.log(id_date_time)
        console.log(id_calendar_button)

        document.getElementById(id_calendar_button).addEventListener('click', function() {
            dialog.toggle();
        });

        document.getElementById(id_date_time).addEventListener('onOk', function() {
            this.value = dialog.time._d.toISOString().split('T')[0];
        });
    }
}