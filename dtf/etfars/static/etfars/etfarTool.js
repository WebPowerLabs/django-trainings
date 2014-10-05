(function () {
function splitScreen() {
  // show right editor, make left editor half width
  $("#right-editor").addClass('col-md-6').removeClass('hidden');
  $("#left-editor").addClass('col-md-6');
}
function singleScreen() {
  // hide right editor, make left editor full width
  $("#right-editor").removeClass('col-md-6').addClass('hidden');
  $("#left-editor").removeClass('col-md-6');
}
function cloneForm() {
  // clone from the hidden form clone
  $('#etfar_tool_clone').clone().appendTo($("#right-editor")).attr('id', 'etfar_tool').removeClass('hidden');
  $('#right-editor #etfar_tool').fadeOut(0, function() {
    $(this).delay(500).fadeIn();
  });
  // populate hidden event input with event title value
  $('#right-editor #id_event').val($('#event-title').text());
}
function saveEvent(eventInput) {
  // hide event field and move to clone.
  eventInput.parents('.form-group').addClass('hidden').appendTo($("#etfar_tool_clone"));
  // move event input to page title
  $('#event-title').removeClass('hidden').text(eventInput.val());
}
function moveRightFormToLeft() {
  $("#right-editor #etfar_tool").fadeOut(500, function() {
    $("#left-editor #etfar_tool").replaceWith($("#right-editor #etfar_tool"));
    $("#left-editor #etfar_tool").fadeIn(500);
    singleScreen();
  });
}
function moveLeftFormToRight() {
  $("#right-editor #etfar_tool").replaceWith($("#left-editor #etfar_tool"));
}
function toggleObj(obj, toggle) {
  // toggle an objects 'hidden' css class
  // optionally pass toggle as 'show' or 'hide' string
  toggle = toggle || false;
  if(toggle) {
    if(toggle=='show'){
      obj.removeClass('hidden');
      obj.fadeOut(0, function() {
        obj.fadeIn(500);
      });
    }
    if(toggle=='hide'){
      obj.fadeOut(500, function() {
        //obj.addClass('hidden');
      });
    }
  } else {
    obj.toggleClass('hidden');
  }
}

function progressCheckNo() {
  // user selects no in progress box
  // this starts a new "tfar"
  $('#progress-check').fadeOut(500, function() {
    $('#replace-old-tfar').fadeOut(0, function() {
      $(this).removeClass('hidden').fadeIn(500);
    });
  });
  splitScreen();
  cloneForm();
}
function progressCheckYes() {
  // user selects yes in progress box
  toggleObj($('#progress-check'), 'hide');
  // save etfar
  $("#left-editor #etfar_tool").submit();
}
function startNewTfar() {
  var $eventInput = $("#left-editor #etfar_tool #id_event");
    $('#start-new-tfar').fadeOut(0);
    $('#replace-old-tfar').removeClass('hidden').fadeIn(0);
    saveEvent($eventInput);
    splitScreen();
    cloneForm();
}
$(document).ready(function(){
  $('#start-new-tfar').on('click', function(e) {
    e.preventDefault();
    startNewTfar(e);
  });
  $('#replace-old-tfar').on('click', function(e) {
    moveRightFormToLeft();

    $('#replace-old-tfar').fadeOut(500, function() {
       // start progress check
      $('#progress-check').fadeOut(0, function() {
        $(this).removeClass('hidden');
        $(this).fadeIn(500);
      });
    });

  });
  $('#progress-yes').on('click', function(e) {
    e.preventDefault();
    progressCheckYes();
  });
  $('#progress-no').on('click', function(e) {
    e.preventDefault();
    progressCheckNo();
  });
});
})();