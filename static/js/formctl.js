$(document).ready(function() {
    var max_calls = 3;
    $(".add-field").click(function() {
        var current = $(this).parents('.input-group:first'),
            new_field = current.clone();
        new_field.find('.add-field')
            .removeClass('add-field').addClass('remove-field')
            .removeClass('btn-success').addClass('btn-danger')
            .html('<i class="fa fa-times"></i>');
        new_field.find('input').removeAttr('id');
        $(new_field).appendTo(current.parents('.form-group'));

        $(".remove-field").click(function() {
            console.log($(this));
            console.log($(this).parents(".input-group"));
            $(this).parents(".input-group").remove();
        });
    });
});
