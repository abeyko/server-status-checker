/** Gets site_url and icon_url return values from popular_sites_data Python function. */
var get_sites = $.ajax({
    'url': 'Site/Database/read_the_table'
});
get_sites.done(function(sites) {
    var icon_urls = sites.icon_list;
    var site_urls = sites.url_list;
    var last_checked = sites.last_checked_list;
    var status_icon = sites.status_icon_list;
    var ping_status = sites.ping_status_list;
    var ping_latency = sites.ping_latency_list;
    var http_status = sites.http_status_list;

    var table_string = "";
    var strings = ["Icon", "Site", "Last Checked", "Status Icon", "Packets Received", "Ping Latency", "HTTP Status", "Delete Site", "Ping Site"];
    for (i = 0; i < strings.length; i++) {
        table_string += "<th style=\"color: #FFFFFF\">" + strings[i] + "</th>";

    }
    new_table_string = "<tr>" + table_string + "</tr>";

    for (i = 0; i <site_urls.length; i++) {
        table_string += "<tr><td align=\"center\" width=\"64\">" +
            "<img src=" + icon_urls[i] +
            "></td><td style=\"color: #FFFFFF\">" + site_urls[i] +
            "</td><td style=\"color: #FFFFFF\">" + last_checked[i] +
            "</td><td style=\"font-size:200%\">" + status_icon[i] +
            "</td><td style=\"color: #FFFFFF\">" + ping_status[i] +
            "</td><td style=\"color: #FFFFFF\">" + ping_latency[i] +
            "</td><td style=\"color: #FFFFFF\">" + http_status[i] +
            "</td><td>" +
            "<button type=\"button\" onclick=\"delete_the_site(&#34;" +
            site_urls[i] + "&#34;, &#34;" + site_urls[i] +
            "&#34;)\">Delete</button>" + "</td><td>" +
            "<button type=\"button\" onclick=\"ping_the_site(&#34;" +
            site_urls[i] + "&#34;, &#34;" + site_urls[i] +
            "&#34;)\">Ping Now</button>" + "</td></tr>";
    }
    document.getElementById("sites").innerHTML = table_string;
    // ever 5 min do a location.reload()
});
/** Posts site to delete in delete_site Python function. */
function delete_the_site(site, site_url) {
    console.log("deleting string");
    $.post("Site/Database/delete_a_site", {
        "url": site
    }).done(function delete_the_site() {
        $("tr").remove(":contains(\'" + site_url + "\')");
        console.log("." + site_url);
    });
}

/** Posts site to add in add_site Python function. */
$("#add_site_button").click(function(add_site_button_clicked) {
    $.post("Site/Database/add_a_site", {
        "url": $("input[name='field']").val()
    }).done(function() {
        console.log("new site was added");
        $("input[name='field']").val('');
        //$('#sites tr:last').after(table_row);

    });
    add_site_button_clicked.preventDefault();
});

/** Posts site to delete in delete_site Python function. */
function ping_the_site(site, site_url) {
    console.log("pinging site");
    $.post("Site/Database/single_status_check", {
        "url": site
    });
}
