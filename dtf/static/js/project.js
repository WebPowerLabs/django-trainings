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

function showNotification(html, time){
    var notifyBalloon = '<div class="notify-balloon">' + html + '</div>';
    $('body').append(notifyBalloon);
    setTimeout(function(){
        $('.notify-balloon').fadeOut();
    }, time);
}

$(document).ready(function(){
    $('#shareModal').on('hidden.bs.modal', function(event){
        $('.modal-share-form').html('');
    });
    // AJAX request to DTFCommentShareView
    $('body').on('click', '.btn-share-form', function(event){
        var url = $(this).attr('data-url');
        $.ajax({
            url: url,
            type: 'GET',
            success: function (data) {
                $('.modal-share-form').html(data);
            }
        });        
    });
    // AJAX submit to DTFCommentShareView
    $('body').on('submit', '.share-form', function(event){
        event.preventDefault();
        var postData = $(this).serializeArray();
        var selectedGroup = $(this).find(':selected').text();
        var notifyMessage = '<b>Post sent</b>.<br> This post has been shared \
                             to the community <br /><b>"' + selectedGroup + '"</b>.';
        var url = $('.btn-share-form').attr('data-url');
        $.ajax({
            url: url,
            data: postData,
            type: 'POST',
            statusCode: {
                200: function(data){
                    $('.modal-share-form').html(data);
                },
                201: function(){
                    $('#shareModal').modal('hide');
                    showNotification(notifyMessage, 2000);
                }
            }
        });
    });
    // AJAX request to CommentPreview
    $('body').on('click', 'a.tab-preview', function(event){
        var url = $(this).attr('data-url');
        var commentId = $(this).attr('data-id');
        var data = $('#tab-write-' + commentId + ' textarea').val(); 
        var tabPreview = $('#tab-preview-' + commentId);
        tabPreview.html('Loading preview...');
        $.ajax({
            url: url,
            type: 'POST',
            data: {data: data},
            success: function (data) {
                tabPreview.html(data);
            }
        });        
    });
    // AJAX request to FavouriteAddView.
    $('body').on('click', '.ajax_action', function(event){
        event.preventDefault();
        var $this = $(this);
        var target = $this.attr('data-target');
        target = target != undefined ? $(target) : $this;
        var url = $this.attr('data-url');
        console.log(target);
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
    
    // AJAX file uploader
    var uploader = $('.fileuploader');
    var acceptFileTypes = /(mp4|avi|mov|mpeg)$/i;
    var in_progress = 0;
    
    // Remove uploaded file
    $('body').on('click', '.fileinput-button-remove', function(event){
        event.preventDefault();
        $("#id_video_pk").val('');
        $("#id_video_path").val('');
        $(this).addClass('hidden');
        $('.fileinput-button').removeClass('hidden');
    });
    
    // Upload file
    uploader.each(function(){
        var upl = $(this);
        var addBtn = $('.fileinput-button');
        var removeBtn = $('.fileinput-button-remove');
        var submitBtn = $('#submit-id-save_changes');
        upl.fileupload({
            url: upl.attr('data-url'),
            dataType : 'json',
            add : function(e, data) {
                var file = data.files[0];
                var uploadErrors = [];
                if (file['name'].length && !acceptFileTypes.test(file['name'])) {
                    uploadErrors.push('Accepts only avi, mp4, mov, mkv files.');
                }
                if (uploadErrors.length > 0) {
                    alert(uploadErrors.join("\n"));
                } else {
                    in_progress += 1;
                    data.submit();
                    addBtn.attr('disabled', 'disabled');
                    submitBtn.attr('disabled', 'disabled');
                }
            },
            done : function(e, data) {
                $("#id_video_path").val(data.result.path);
                submitBtn.removeAttr('disabled');
                addBtn.addClass('hidden').removeAttr('disabled');
                removeBtn.removeClass('hidden');
                removeBtn.find('.fileinput-title').text("Remove " + "'" + data.result.base_name + "'");
            },
            progress: function(e, data){
                var file = data.files[0];
                var progress = parseInt(data.loaded / data.total * 100, 10);
                var progressBar = $('.progress');
                if(progress == 100){
                    progressBar.removeClass('active');
                    in_progress = in_progress - 1;
                    setTimeout(function(){
                        progressBar.addClass('hidden');
                    }, 1000);
                    if (in_progress == 0){
                    }
                }else{
                    progressBar.removeClass('hidden');
                }
                progressBar.find('.progress-bar').css('width', progress + '%');
            }
        });
    });
});











