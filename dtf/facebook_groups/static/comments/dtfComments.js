
function getCommentId() {
  var commentId = $.QueryString["c"];
  console.log(commentId);
  return commentId;
}

function goToComment(commentId) {
  if(commentId) {
  var $comment = $('#c' + commentId.toString());
  console.log($comment);
  $comment.goTo();
  }
}


$(document).ready(function(){
  var commentId = getCommentId();
  goToComment(commentId);
});