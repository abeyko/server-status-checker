/*  Need to fix logic / methods and learn how to integrate with cherrypy */

$(document).ready(function() {
      $('input').change(function() {
    var $input = $(this),
      $flag = $input.next();


    if (!$input.val()) { 
      $flag.remove();
    }

    if ($flag.length == 0 || !$flag.is('.valid')) {
      $input.after('<div class="valid"></div>');
    }

    if ($flag.length == 0 || !$flag.is('.invalid')) {
      $input.after('<div class="invalid"></div>');
    }

    })
});