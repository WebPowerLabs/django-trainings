function createCommentList(data, commentTemplate, $post) {

	for (var i = 0; i < data.data.length; i++) {
		comment = data.data[i];
		console.log(comment);
		var $comment = $(commentTemplate).clone();
		$comment.attr("id", "comment-" + comment.id);
		var commentFromImg = "https://graph.facebook.com/" + comment.from.id + "/picture?width=64&height=64";
		$comment.find(".fb-profile-img").attr("src", commentFromImg);
		$comment.find(".fb-from-user").text(comment.from.name);
		$comment.find(".fb-message").text(comment.message);
		if(comment.picture && comment.link) {
			$comment.find(".fb-link").attr("href", comment.link);
			$comment.find(".fb-picture").attr("src", comment.picture);
		} else {
			$comment.remove(".fb-link");
			$comment.remove(".fb-picture");
		};
		$post.find(".fb-comments").append($comment);
	};

};

function createPostList(data, postTemplate, commentTemplate, feedList) {

	for (var i = 0; i < data.data.length; i++) {
		post = data.data[i];
		console.log(post);
		var $post = $(postTemplate).clone();
		$post.attr("id", "post-" + post.id);
		var postFromImg = "https://graph.facebook.com/" + post.from.id + "/picture?width=64&height=64";
		$post.find(".fb-profile-img").attr("src", postFromImg);
		$post.find(".fb-from-user").text(post.from.name);
		$post.find(".fb-message").text(post.message);
		if(post.picture && post.link) {
			$post.find(".fb-link").attr("href", post.link);
			$post.find(".fb-picture").attr("src", post.picture);
		} else {
			$post.remove(".fb-link");
			$post.remove(".fb-picture");
		};
		if(post.comments) {
			createCommentList(post.comments, "#comment-template", $post)
		};
		$(feedList).append($post);
	};

};

function getNext(nextUrl, postTemplate, feedList, nextBtn) {
	$.getJSON(nextUrl, function(data) {
		console.log(data);
		createPostList(data, "#post-template", "#comment-template", "#facebook-feed-list");
		$(nextBtn).data("next", data.paging.next);
	});
};

$('#get-next').click(function(e) {
	e.preventDefault();
	var nextUrl = $(this).data('next');
	getNext(nextUrl, "#post-template", "#facebook-feed-list", this);
});