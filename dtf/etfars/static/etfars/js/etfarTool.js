(function () {
function splitScreen() {
  // show right editor, make left editor half width
  $("#right-editor").addClass('col-md-6').removeClass('hidden');
  $("#left-editor").addClass('col-md-6 inactive');
}
function singleScreen() {
  // hide right editor, make left editor full width
  $("#right-editor").removeClass('col-md-6').addClass('hidden');
  $("#left-editor").removeClass('col-md-6 inactive');
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
  // move event input to page title
  $('#event-title').removeClass('hidden').text(eventInput.val());
  // hide event field and move to clone.
  eventInput.parents('.form-group').addClass('hidden').appendTo($("#etfar_tool_clone"));
}
function saveTfar(baseForm, newForm) {
  newForm.find('#hint_id_thought').text("Old Thought: " + baseForm.find('#id_thought').val());
  newForm.find('#hint_id_feeling').text("Old Feeling: " + baseForm.find('#id_feeling').val());
  newForm.find('#hint_id_action').text("Old Action: " + baseForm.find('#id_action').val());
  newForm.find('#hint_id_result').text("Old Result: " + baseForm.find('#id_result').val());
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
  saveTfar($("#left-editor #etfar_tool"), $("#right-editor #etfar_tool"));
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
    saveTfar($("#left-editor #etfar_tool"), $("#right-editor #etfar_tool"));
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