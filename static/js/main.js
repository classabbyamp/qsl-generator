$(document).ready(function() {
    var delay = 400;
    var maxes = {
        "callsign": 2,
        "cq": 3,
        "itu": 3,
        "county": 3,
        "qth": 3
    };

    // fade in on load
    $("body").css("opacity", "0").animate({ opacity: 1 }, delay);

    // Handle addition/removal of extra fields
    $(".add-field").click(function() {
        var current = $(this).parents('.copy:first');
        var curr_count = $(current).parents('.copy-parent').children('.copy').length;
        var curr_id = $(current).children('input:first').attr("id");
        console.log(curr_count);
        console.log(curr_id);

        var new_field = current.clone();
        new_field.find('.add-field')
            .removeClass('add-field').addClass('remove-field')
            .removeClass('btn-success').addClass('btn-danger')
            .html('<i class="fa fa-times"></i>');
        new_field.find('input').removeAttr('id').val('');

        $(new_field).css("opacity", "0").animate({ opacity: 1 }, delay).appendTo(current.parents('.copy-parent:first'));

        if (curr_count + 1 >= maxes[curr_id]) {
            $(current).children('div:first').children('button:first').prop("disabled", true);
        }

        $(".remove-field").click(function() {
            $(this).parents(".copy:first").animate({ opacity: 0 }, delay, function() { $(this).remove() });
            $(this).parents(".copy-parent:first").children(".copy:first")
                .children("div:first").children("button:first").prop("disabled", false);
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

    // generate the QSL card with AJAX
    $('form').on('submit', function() {
        // form validation
        // form submission
        $.ajax({
            url: '/generate',
            data: $('form').serialize(),
            type: 'POST',
            beforeSend: function() {
                $("button#generate").prop("disabled", true).html(
                    `<span class="spinner-border" role="status" aria-hidden="true"></span>`
                );
                $("div#gen-error").animate({ opacity: 0 }, delay, function() { $(this).remove() });
                $("button#pdf-btn").animate({ opacity: 0 }, delay);
                $("button#tex-btn").animate({ opacity: 0 }, delay);
                $("div#qsl-img").animate({ opacity: 0 }, delay);
            },
            success: function(data) {
                if (data.success) {
                    $('a#pdf-link').attr("href", "/file/pdf/" + data.file);
                    $('button#pdf-btn').prop("disabled", false)
                        .css("opacity", "0")
                        .prop("hidden", false)
                        .animate({ opacity: 1 }, delay);
                    $('a#tex-link').attr("href", "/file/tex/" + data.file);
                    $('button#tex-btn').prop("disabled", false)
                        .css("opacity", "0")
                        .prop("hidden", false)
                        .animate({ opacity: 1 }, delay);
                    $('img#qsl-preview').attr("src", "/file/png/" + data.file);
                    $('div#qsl-img').css("opacity", "0")
                        .prop("hidden", false)
                        .animate({ opacity: 1 }, delay);
                } else {
                    $('div#generated').prepend(
                        `<div class="alert alert-danger mt-2" id="gen-error" role="alert" hidden>Error generating QSL card: <code>` + data.error + `</code></div>`
                    );
                    $('div#gen-error').css("opacity", "0")
                        .prop("hidden", false)
                        .animate({ opacity: 1 }, delay);
                }
            },
            error: function(err, textStatus, errorThrown) {
                $('div#generated').prepend(
                    `<div class="alert alert-danger mt-2" id="gen-error" role="alert" hidden>Error generating QSL card: <code>` + errorThrown + `</code></div>`
                );
                $('div#gen-error').css("opacity", "0")
                    .prop("hidden", false)
                    .animate({ opacity: 1 }, delay);
            },
            complete: function() {
                $("button#generate").prop("disabled", false).html(`Generate`);
            }
        });
    });
});
