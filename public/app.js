/** Gets site_url and icon_url return values from popular_sites_data Python function. */
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
        //console.log(table_string)
    }
    document.getElementById("popular_sites").innerHTML = table_string;
});
/** Posts site to delete in delete_site Python function. */
function delete_the_site(site, site_url) {
        console.log("deleting string")
        $.post("/delete_site", {
            "delete_site": site
        }).done(function delete_the_site() {
            $("tr").remove(":contains(\'" + site_url + "\')");
            console.log("." + site_url);
        });
    }
    /** Posts site to add in add_site Python function. */
$("#add_site_button").click(function(add_site_button_clicked) {
    $.post("/add_site", {
        "add_site": $("input[name='field']").val()
    }).done(function() {
        console.log("new site was added");
        $("input[name='field']").val('');
        //$('<li>').text('New item').appendTo('.items');
    });
    add_site_button_clicked.preventDefault();
});
/** Gets site_url return values from my_sites_data Python function. */
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
        table_string += "<tr class=\"" + j.toString() +
            "\"><td align=\"center\" width=\"64\" style=\"color: #FFFFFF\">" +
            site_urls[i] + "</td><td>" + "Last checked 2 seconds ago" +
            "</td><td id=" + j.toString() +
            " style=\"font-size:200%\"></td><td>" + "Weekly Stats" +
            "</td><td>" +
            "<button type=\"button\" onclick=\"delete_the_site(&#34;" +
            site_urls[i] + "&#34;, &#34;" + site_urls[i] +
            "&#34;)\">Delete</button>" + "</td></tr>";
        console.log(table_string)
    }
    document.getElementById("my_sites").innerHTML = table_string;
});
/** Gets result return values from site_status Python function. */
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