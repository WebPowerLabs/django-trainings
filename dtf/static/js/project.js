// CSRF for AJAX request.
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
// end CSRF for AJAX request.
$(document).ready(function(){
    // AJAX request to FavouriteAddView.
    $('body').on('click', '.ajax_action', function(event){
        event.preventDefault();
        var $this = $(this);
        var target = $this.attr('data-target');
        target = target != undefined ? $(target) : $this;
        var url = $this.attr('data-url');
        $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            success: function (data) {
                if(data.is_active == true){
                    target.addClass('is_active');
                }else{
                    target.removeClass('is_active');
                }
            }
        });
    });

    
    
    // Renders element with class 'video-js' to HTML5 video player.
    $('.video-js').each(function(){
        videojs(this, {}, function(){
        });
    });
    // Adds drag&drop reordering functionality to element with class 'sortable'.
    $('.sortable').each(function() {
        var $this = $(this);
        var url = $this.attr('data-url');
        $this.sortable({
            items: '.sortable_item',
            start: function(e, ui){
                ui.placeholder.height(ui.item.height());
            },
            stop: function(event, ui){
                var data = [];
                $this.find('.sortable_item').each(function(index, item){
                    data.push($(item).attr('data-pk'));
                });
                $.ajax({
                    url: url,
                    data: JSON.stringify({'new_order': data}),
                    type: 'POST',
                    contentType: 'application/json',
                });
            }
        });
        $this.disableSelection();
    });
});


