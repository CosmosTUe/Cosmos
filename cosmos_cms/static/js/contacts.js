"use strict";
$(function () {

    $('.contacts-plugin input[type=submit]').on('click', function (evt) {
        let $form = $(this).parents('form').eq(0);

        let data = $form.serializeArray().reduce((formData, nameValue) => {
            formData.append(nameValue.name, nameValue.value);
            return formData;
        }, new FormData());

        function handleResponse(data) {
            if (data.msg) { // Success!
                $form.siblings('.success').html(data.success).show(100);

                //
                // NOTE: We hide the form if there was ANY success to prevent
                // duplicate submissions. There can be no success if there are
                // form-validation errors, in which case, the form remains
                // visible so the visitor can correct their mistakes.  In the
                // event that there are no validation errors and yet, nothing is
                // successful, the form remains visible so the user can try again.
                //
                $form.add('.legend').hide(100);
            } else { // Validation Issues...
                //
                // data will a dictionary like so:
                // { 'field_name': ['error1', 'error2'], ... }
                //
                $form.find('.error').empty();
                let output = ''
                $.each(data.responseJSON, (field, error) => {
                    output = output + `${field}: ${error}<br>`;
                })
                $form.siblings('.errors').find('.form-errors').html(output)
                $form.siblings('.errors').show(100);
            }
        }

        evt.preventDefault();
        $form.siblings('.errors, .success').hide(100);

        $.ajax({ type: "POST", url: $form.attr('action'), data: data, processData: false, contentType: false }).always(handleResponse);
    });

});