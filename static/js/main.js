$(document).ready(function() {
    var max = 2;
    $(".add-field").click(function() {
        var current = $(this).parents('.copy:first'),
            new_field = current.clone();
        new_field.find('.add-field')
            .removeClass('add-field').addClass('remove-field')
            .removeClass('btn-success').addClass('btn-danger')
            .html('<i class="fa fa-times"></i>');
        new_field.find('input').removeAttr('id').val('');
        $(new_field).appendTo(current.parents('.copy-parent:first'));

        $(".remove-field").click(function() {
            $(this).parents(".copy:first").remove();
        });
    });

    $('textarea[data-limit-rows=true]')
        .on('keypress', function (event) {
            var textarea = $(this),
                text = textarea.val(),
                numberOfLines = (text.match(/\n/g) || []).length + 1,
                maxRows = parseInt(textarea.attr('rows'));

            if (event.which === 13 && numberOfLines === maxRows ) {
                return false;
        }
    });
});
