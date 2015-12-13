//function scriptReload(id) {
//        var $el = $('#' + id);
//        console.log('this is el');
//        console.log($el.prop);
//        //$('#' + id).replaceWith('<script id="' + id + '" src="' + $el.prop(
        //    'src') + '"><\/script>');
//        console.log('after el');
//    }
// -------POPULAR SITES-----------
// gets 2 responses (return values) from 'popular_sites_data' function in CherryPy
// and puts them in their own list
// one list for site_urls and one list for icon_urls
// then generates the html with a for loop and displays it via innerHTML 
var get_popular_sites = $.ajax({
    'url': '/popular_sites_data'
});
get_popular_sites.done(function(popular_sites) {
    var popular_sites_site_url_list = popular_sites.site_url;
    var popular_sites_icon_url_list = popular_sites.icon_url;
    var site_urls = [];
    var img_urls = [];
    var table_string = "";
    for (i = 0; i < popular_sites_icon_url_list.length; i++) {
        site_urls.push(popular_sites_site_url_list[i][0]);
        img_urls.push(popular_sites_icon_url_list[i][0]);
        table_string += "<tr><td align=\"center\" width=\"64\">" +
            "<img src=" + img_urls[i] +
            "></td><td style=\"color: #FFFFFF\">" + site_urls[i] +
            "</td><td>" + "Last checked 2 seconds ago" + "</td><td id=" +
            i.toString() + " style=\"font-size:200%\"></td><td>" +
            "Weekly Stats" + "</td></tr>";
        console.log(table_string)
    }
    document.getElementById("popular_sites").innerHTML = table_string;
});
// -------DELETE BUTTON FUNCTION DEFINED-----------
// when the delete_the_string function is called, posts the functions 
// argument to the CherryPy function 'delete_site'
// under the key of 'the_url'
function delete_the_site(site) {
        console.log("deleting string")
        $.post("/delete_site", {
            "delete_site": site
        }).done(function delete_the_site() {
            //$('.selected').remove();
            // need to add something to reload the my_sites table upon 
            // clicking the delete button
        });
    }
    // -------SET BUTTON FUNCTION DEFINED-----------
    // when the 'Set' button is clicked, the information or input inside 
    // the text box is posted to the CherryPy function 'append_my_sites', 
    // which then adds the new site to the database
$("#add_site_button").click(function(add_site_button_clicked) {
    $.post("/append_to_my_sites", {
        "add_site": $("input[name='field']").val()
    }).done(function() {
        console.log("new site was added");
        //getMySites();
        //getMySites.done(response);
        $("input[name='field']").val('');
        //scriptReload('my_sites');
        //console.log("afer this");
        //$('<li>').text('New item').appendTo('.items');
        // add something to clear text box after user input and then 
        // reload the table part of page upon clicking the Set button
    });
    add_site_button_clicked.preventDefault();
});
// -------MY SITES-----------
// gets 1 response (return value) from 'get_other_table' function 
// in CherryPy and puts it in a list for the site_urls, then generates
// the html with a for loop and displays it via innerHTML. This table
// has a delete buton associated with each Url via the 
// delete_the_string function in JS
var get_my_sites = $.ajax({
    'url': '/my_sites_data'
});
get_my_sites.done(function(response) {
    var url_list = response.site_url;
    var site_urls = [];
    var j = 0;
    var table_string = "";
    for (i = 0; i < url_list.length; i++) {
        site_urls.push(url_list[i][0]);
        j = i + 8;
        console.log(typeof(site_urls[i]))
        console.log("site url is " + site_urls[i]) //
        table_string +=
            "<tr><td align=\"center\" width=\"64\" style=\"color: #FFFFFF\">" +
            site_urls[i] + "</td><td>" + "Last checked 2 seconds ago" +
            "</td><td id=" + j.toString() +
            " style=\"font-size:200%\"></td><td>" + "Weekly Stats" +
            "</td><td>" +
            "<button type=\"button\" onclick=\"delete_the_site(&#34;" +
            site_urls[i] + "&#34;)\">Delete</button>" + "</td></tr>";
        console.log(table_string)
    }
    document.getElementById("my_sites").innerHTML = table_string;
});
// -------PING / HTTP THE SITES-----------
// runs the CherryPy funtion 'get_data' and adds an id to each 
// index for the response list
var get_site_status = $.ajax({
    'url': '/site_status'
});
get_site_status.done(function(ping_list) {
    console.log(ping_list.result.length)
    for (i = 0; i < ping_list.result.length; i++) {
        $('#' + i).text(ping_list.result[i]);
    }
});
get_site_status.fail(function(jqXHR, textStatus) {
    alert('Request failed: ' + textStatus);
});