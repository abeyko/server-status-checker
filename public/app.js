/** Gets site_url and icon_url return values from popular_sites_data Python function. */
var get_sites = $.ajax({
    'url': 'Site/Database/read_the_table'
});
get_sites.done(function(sites) {
    var icon_urls = sites.icon_list;
    var display_site_urls = sites.display_url_list;
    var original_site_urls = sites.original_url_list;
    var last_checked = sites.last_checked_list;
    var status_icon = sites.status_icon_list;
    var ping_status = sites.ping_status_list;
    var ping_latency = sites.ping_latency_list;
    var http_status = sites.http_status_list;
    var source = "";
    var table_string = "";
    var strings = ["Icon", "Site", "Last Checked", "Status Icon",
        "Packets Received", "Ping Latency", "HTTP Status",
        "Delete Site", "Update Stats"
    ];
    for (i = 0; i < strings.length; i++) {
        table_string += "<th style=\"color: #FFFFFF\"><i>" + strings[i] +
            "</i></th>";
    }
    new_table_string = "<tr>" + table_string + "</tr>";
    for (i = 0; i < display_site_urls.length; i++) {
        if (icon_urls[i] == null) {
            source =
                "<form action=\"Site/Database/upload\" method=\"post\" target=None enctype=\"multipart/form-data\">" +
                "<input type=\"text\" name=\"url\" id=\"uploader" + i +
                "\" value=\"" + original_site_urls[i] +
                "\" style = display:none;/> " +
                "<input type=\"file\" name=\"myFile\" id=\"fileupload" +
                i +
                "\" style=\"display: none;\" onchange=\"javascript:this.form.submit();\" onsubmit=\"return false\" />" +
                "<button type=\"button\" name=\"Upload Image\" onclick=\"javascript:document.getElementById('fileupload" +
                i + "').click();\">Upload Image</button></form>";
        } else {
            source = "<img src=" + icon_urls[i] + ">";
        }
        table_string += "<tr><td align=\"center\" width=\"64\">" +
            source + "</td><td style=\"color: #FFFFFF\">" +
            display_site_urls[i] + "</td><td style=\"color: #FFFFFF\">" +
            last_checked[i] + "</td><td style=\"font-size:200%\">" +
            status_icon[i] + "</td><td style=\"color: #FFFFFF\">" +
            ping_status[i] + "</td><td style=\"color: #FFFFFF\">" +
            ping_latency[i] + "</td><td style=\"color: #FFFFFF\">" +
            http_status[i] + "</td><td>" +
            "<button type=\"button\" onclick=\"delete_the_site(&#34;" +
            original_site_urls[i] + "&#34;, &#34;" + display_site_urls[
                i] + "&#34;)\">Delete</button>" + "</td><td>" +
            "<button type=\"button\" onclick=\"ping_the_site(&#34;" +
            original_site_urls[i] + "&#34;)\">Update</button>" +
            "</td></tr>";
    }
    document.getElementById("sites").innerHTML = table_string;
    // every 5 min do a location.reload()
});
/** Posts site to delete in delete_site Python function. */
function delete_the_site(site, site_url) {
        console.log("deleting string");
        $.post("Site/Database/delete_a_site", {
            "url": site
        }).done(function delete_the_site() {
            $("tr").remove(":contains(\'" + site_url + "\')");
            console.log("." + site);
        });
    }
    /** Posts site to add in add_site Python function. */
$("#add_site_button").click(function(add_site_button_clicked) {
    $.post("Site/Database/add_a_site", {
        "url": $("input[name='field']").val()
    }).done(function() {
        console.log("new site was added");
        $("input[name='field']").val('');
    });
    add_site_button_clicked.preventDefault();
});
/** Posts site to update stats on in check_single Python function. */
function ping_the_site(site) {
    console.log("pinging site");
    console.log(site);
    $.post("Site/check_single", {
        "url": site
    });
}