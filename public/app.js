$(document).ready(function() {
    // just for the demos, avoids form submit
    jQuery.validator.setDefaults({
        debug: true,
        success: "valid"
    });
    $("#testform").validate({
        rules: {
            field: {
                required: true,
                url: true
            }
        }
    });
    $(function() {
        // When the testform is submitted…
        $("#testform").submit(function() {
            // post the form values via AJAX…
            var postdata = {
                name: $("#field").val()
            };
            $.post('/submit', postdata, function(data) {
                // and set the title with the result
                $("#title").html(data['title']);
            });
            return false;
        });
    });
    var request = $.ajax({
        'url': '/get_data'
    });
    request.done(function(response) {
        for (i = 0; i < 8; i++) {
            $('#' + i).text(response.res[i]);
        }
    });
    request.fail(function(jqXHR, textStatus) {
        alert('Request failed: ' + textStatus);
    });
})