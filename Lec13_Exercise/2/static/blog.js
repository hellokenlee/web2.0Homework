$(document).ready(function(){
	$("#getCommentBtn").click(function(){
		$.getJSON('/comment?jsoncallback=?', function(data) {
			$.each(data, function(i, comment){
				$("#commentsList").append("<div class='comment'><span class='name'>"+comment["name"]+"</span><span class='time'>"+comment["time"]+"</span><p>"+comment["content"]+"</p></div>")
			})
		})
	})
});