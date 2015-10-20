
// just for the demos, avoids form submit
jQuery.validator.setDefaults({
	debug: true,
	success: "valid"
});
$( "#myform" ).validate({
	rules: {
		field: {
			required: true,
			url: true
		}
	}
});

$(document).ready(function()
  {
    var request = $.ajax({'url': '/get_data'});
    request.done(function(response) 
    { for(i=0; i < 8; i++){
      $('#' + i).text(response.res[i]);
    }
    });
    request.fail(function(jqXHR, textStatus) 
    {
      alert('Request failed: ' + textStatus);
    });
  })