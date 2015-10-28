$(document).ready(function() {
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
    var request2 = $.ajax({
        'url': '/get_tables'
    });
    request2.done(function(response) {
        var double_list = response.site_url;
        var double_list2 = response.icon_url;
        var siteUrls = [];
        var imgUrls = [];
        var tableString = "";
        for (i = 0; i < double_list2.length; i++) {
            siteUrls.push(double_list[i][0]);
            imgUrls.push(double_list2[i][0]);
            console.log(typeof(siteUrls[i]))
            console.log(typeof(imgUrls[i]))
            tableString +=
                "<tr><td align=\"center\" width=\"64\">" +
                "<img src=" + imgUrls[i] +
                "></td><td style=\"color: #FFFFFF\">" +
                siteUrls[i] + "</td><td>" +
                "Last checked 2 seconds ago" + "</td><td id=" +
                i.toString() +
                " style=\"font-size:200%\"></td><td>" +
                "Weekly Stats" + "</td></tr>";
            console.log(tableString)
        }
        document.getElementById("popular_sites").innerHTML =
            tableString;
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
        console.log(response.res.length)
        for (i = 0; i < response.res.length; i++) {
            $('#' + i).text(response.res[i]);
        }
    });
    request.fail(function(jqXHR, textStatus) {
        alert('Request failed: ' + textStatus);
    });
})