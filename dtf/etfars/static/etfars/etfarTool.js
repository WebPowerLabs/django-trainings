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
  $('#etfar_tool_clone').clone().appendTo($("#right-editor")).removeClass('hidden').attr('id', 'etfar_tool');
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
  $("#left-editor #etfar_tool").replaceWith($("#right-editor #etfar_tool"));
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
    }
    if(toggle=='hide'){
      obj.addClass('hidden');
    }
  } else {
    obj.toggleClass('hidden');
  }
}

function progressCheckNo() {
  // user selects no in progress box
  // this starts a new "tfar"
  toggleObj($('#progress-check'), 'hide');
  toggleObj($('#replace-old-tfar'), 'show');
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
    $('#start-new-tfar').addClass('hidden');
    $('#replace-old-tfar').removeClass('hidden');
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
    singleScreen();
    $('#replace-old-tfar').addClass('hidden');
    // start progress check
    toggleObj($('#progress-check'), 'show');
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