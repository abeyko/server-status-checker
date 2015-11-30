function scriptReload(id) {
        var $el = $('#' + id);
        console.log('this is el');
        //console.log(el);
        $('#' + id).replaceWith('<script id="' + id + '" src="' + $el.prop(
            'src') + '"><\/script>');
        console.log('after el');
    }
// -------POPULAR SITES-----------
// gets 2 responses (return values) from 'get_table' function in CherryPy
// and puts them in their own list
// one list for site_urls and one list for icon_urls
// then generates the html with a for loop and displays it via innerHTML 
var getPopSites = $.ajax({
    'url': '/get_table'
});
getPopSites.done(function(response) {
    var double_list = response.site_url;
    var double_list2 = response.icon_url;
    var siteUrls = [];
    var imgUrls = [];
    var tableString = "";
    for (i = 0; i < double_list2.length; i++) {
        siteUrls.push(double_list[i][0]);
        imgUrls.push(double_list2[i][0]);
        tableString += "<tr><td align=\"center\" width=\"64\">" +
            "<img src=" + imgUrls[i] +
            "></td><td style=\"color: #FFFFFF\">" + siteUrls[i] +
            "</td><td>" + "Last checked 2 seconds ago" + "</td><td id=" +
            i.toString() + " style=\"font-size:200%\"></td><td>" +
            "Weekly Stats" + "</td></tr>";
        console.log(tableString)
    }
    document.getElementById("popular_sites").innerHTML = tableString;
});
// -------DELETE BUTTON FUNCTION DEFINED-----------
// when the delete_the_string function is called, posts the functions 
// argument to the CherryPy function 'delete_site'
// under the key of 'the_url'
function delete_the_string(e) {
        console.log("deleting string")
        $.post("/delete_site", {
            "the_url": e
        }).done(function delete_the_string() {
            //$('.selected').remove();
            // need to add something to reload the my_sites table upon 
            // clicking the delete button
        });
    }
    // -------SET BUTTON FUNCTION DEFINED-----------
    // when the 'Set' button is clicked, the information or input inside 
    // the text box is posted to the CherryPy function 'append_my_sites', 
    // which then adds the new site to the database
$("#pingThisToo").click(function(e) {
    $.post("/append_my_sites", {
        "newSite": $("input[name='field']").val()
    }).done(function() {
        console.log("this happened");
        //getMySites();
        //getMySites.done(response);
        $("input[name='field']").val('');
        scriptReload('my_sites');
        console.log("afer this");
        //$('<li>').text('New item').appendTo('.items');
        // add something to clear text box after user input and then 
        // reload the table part of page upon clicking the Set button
    });
    e.preventDefault();
});
// -------MY SITES-----------
// gets 1 response (return value) from 'get_other_table' function 
// in CherryPy and puts it in a list for the site_urls, then generates
// the html with a for loop and displays it via innerHTML. This table
// has a delete buton associated with each Url via the 
// delete_the_string function in JS
var getMySites = $.ajax({
    'url': '/get_other_table'
});
getMySites.done(function(response) {
    var url_list = response.site_url;
    var siteUrl = [];
    var j = 0;
    var nTableString = "";
    for (i = 0; i < url_list.length; i++) {
        siteUrl.push(url_list[i][0]);
        j = i + 8;
        console.log(typeof(siteUrl[i]))
        console.log("site url is " + siteUrl[i]) //
        nTableString +=
            "<tr><td align=\"center\" width=\"64\" style=\"color: #FFFFFF\">" +
            siteUrl[i] + "</td><td>" + "Last checked 2 seconds ago" +
            "</td><td id=" + j.toString() +
            " style=\"font-size:200%\"></td><td>" + "Weekly Stats" +
            "</td><td>" +
            "<button type=\"button\" onclick=\"delete_the_string(&#34;" +
            siteUrl[i] + "&#34;)\">Delete</button>" + "</td></tr>";
        console.log(nTableString)
    }
    document.getElementById("my_sites").innerHTML = nTableString;
});
// -------PING / HTTP THE SITES-----------
// runs the CherryPy funtion 'get_data' and adds an id to each 
// index for the response list
var pingEverything = $.ajax({
    'url': '/get_data'
});
pingEverything.done(function(response) {
    console.log(response.res.length)
    for (i = 0; i < response.res.length; i++) {
        $('#' + i).text(response.res[i]);
    }
});
pingEverything.fail(function(jqXHR, textStatus) {
    alert('Request failed: ' + textStatus);
});