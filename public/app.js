/** Gets site_url and icon_url return values from popular_sites_data Python function. */
var get_popular_sites = $.ajax({
    'url': '/read_table'
});
get_popular_sites.done(function(sites) {
    var urls = sites.url_list;
    console.log("urls is ");
    console.log(urls);
    var icons = sites.icon_list;
    console.log("icons is ");
    console.log(icons);
    var site_urls = [];
    var img_urls = [];
    var table_string = "";
    for (i = 0; i < urls.length; i++) {
        site_urls.push(urls[i]);
        img_urls.push(icons[i]);
        console.log("SITE URLS ARE");
        console.log("IMG URLS ARE");
        console.log(site_urls);
        console.log(img_urls);
        table_string += "<tr><td align=\"center\" width=\"64\">" +
            "<img src=" + img_urls[i] +
            "></td><td style=\"color: #FFFFFF\">" + site_urls[i] +
            "</td><td>" + "Last checked 2 seconds ago" + "</td><td id=" +
            i.toString() + " style=\"font-size:200%\"></td><td>" +
            "Ping Status: " + "</td><td>" +
            "Ping Latency: " + "</td><td>" +
            "HTTP Status: " + "</td><td>" +
            "Weekly Stats" + "</td><td>" +
            "<button type=\"button\" onclick=\"delete_the_site(&#34;" +
            site_urls[i] + "&#34;, &#34;" + site_urls[i] +
            "&#34;)\">Delete</button>" + "</td><td>" +
            "Ping Now" + "</td></tr>";
        console.log("IMG URLS [I] ARE");
        console.log(img_urls[i]);
    }
    document.getElementById("sites").innerHTML = table_string;
});
/** Posts site to delete in delete_site Python function. */
function delete_the_site(site, site_url) {
    console.log("deleting string");
    $.post("/delete_site", {
        "url": site
    }).done(function delete_the_site() {
        $("tr").remove(":contains(\'" + site_url + "\')");
        console.log("." + site_url);
    });
}

/** Posts site to add in add_site Python function. */
$("#add_site_button").click(function(add_site_button_clicked) {
    $.post("/add_site", {
        "url": $("input[name='field']").val()
    }).done(function() {
        console.log("new site was added");
        $("input[name='field']").val('');
        //$('<li>').text('New item').appendTo('.items');
    });
    add_site_button_clicked.preventDefault();
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


/**HTTP/1.1 500 Internal Server Error 
function read_database(tables, table_columns) {
    tables = ["popular_sites", "my_sites"];
    table_columns = ["site_url", "icon_url"];
    console.log("reading database");
    console.log("tables are");
    console.log(tables);
    console.log("table_columns are: ");
    console.log(table_columns);
    $.post("/read_table", {
        "tables": tables,
        "table_columns": table_columns
    });
}*/
    //table_type = "popular_sites"; // code test
    //read_database(table_type); // code test
    //var popular_sites_site_url_list = popular_sites.site_url;
    //var popular_sites_icon_url_list = popular_sites.icon_url;
/** Gets site_url return values from my_sites_data Python function. 
var get_my_sites = $.ajax({
    'url': '/my_sites_data'
});
get_my_sites.done(function(response) {
    //table_type = "my_sites"; // code test
    //read_database(table_type); // code test
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
});*/

