
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
    $('button').on('click', function()
    {
      var request = $.ajax({'url': '/getData'});
      request.done(function(response) 
      {
        $('#res').text(response.res);
      });
      request.fail(function(jqXHR, textStatus) 
      {
        alert('Request failed: ' + textStatus);
      });
    })
  });