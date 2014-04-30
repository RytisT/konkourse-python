// JavaScript doc for conversations on every part of the konkourse site

(function(){
	
    $.fn.joinLeaveEvent = function() {
       $(this).toggle();
       $(this).siblings().toggle();
   };
})();

function clickComment (id, page) {
	$('div.commentReplace' + id).
		replaceWith(' \
			    <div class="commentReplace' + id + '"> \
			    <form class="commentContain style="margin-bottom:5px; width:100%;"> \
			    <table style="width:100%;"> \
			    <tr> \
			    <td><textarea style="margin-bottom:3px; margin-left:80px; width:595px; resize:none;" id="commentMessage" rows="2" placeholder="Type a response..."></textarea></td> \
			    </tr> \
			    <tr> \
			    <td> \
			    <a href="javascript:void(0)" class="btn btn-small btn-inverse btnComment" style="float:right; margin-left:5px; margin-right:10px;" onclick="comment(' + id + ', ' + page + ')"">Comment</a> \
			    <a href="javascript:void(0)" class="btn btn-small" style="float:right;" onclick="clickCommentClear(' + id + ');">Hide</a></div> \
			    <font id="tooLongCommentError' + id + '" size="3" color="red" style="float:left; margin-left:80px;margin-top:5px;display:none;">Comment length is more than 5000 characters.</font> \
			    </td> \
			    </tr> \
			    </table> \
			    </form> \
			    </div>'
			   );
}
function clickCommentProf (id, page) {
	$('div.commentReplace' + id).
		replaceWith(' \
			    <div class="commentReplace' + id + '"> \
			    <form class="commentContain style="margin-bottom:5px; width:100%;"> \
			    <table style="width:100%;"> \
			    <tr> \
			    <td><textarea style="margin-bottom:3px; width:97%; resize:none;" id="commentMessage" rows="2" placeholder="Type a response..."></textarea></td> \
			    </tr> \
			    <tr> \
			    <td> \
			    <a href="javascript:void(0)" class="btn btn-small btn-inverse btnComment" style="float:right; margin-left:5px;" onclick="comment(' + id + ', ' + page + ')"">Comment</a> \
			    <a href="javascript:void(0)" class="btn btn-small" style="float:right;" onclick="clickCommentClear(' + id + ');">Hide</a></div> \
			    <font id="tooLongCommentError' + id + '" size="3" color="red" style="float:left; margin-top:5px;display:none;">Comment length is more than 5000 characters.</font> \
			    </td> \
			    </tr> \
			    </table> \
			    </form> \
			    </div>'
			   );
}
function clickCommentFeed (id, page) {
	$('div.commentReplace' + id).
		replaceWith(' \
			    <div class="commentReplace' + id + '"> \
			    <form class="commentContain style="margin-bottom:5px; width:100%;"> \
					<table style="width:370px; margin-left:80px; margin-top:5px;"> \
						<tr> \
							<td><textarea style="margin-bottom:3px; width:97%; resize:none;" id="commentMessage" rows="2" placeholder="Type a response..."></textarea></td> \
							</tr> \
							<tr> \
							<td> \
							<a href="javascript:void(0)" class="btn btn-small btn-inverse btnComment" style="float:right; margin-left:5px;" onclick="comment(' + id + ', ' + page + ')"">Comment</a> \
							<a href="javascript:void(0)" class="btn btn-small" style="float:right;" onclick="clickCommentClear(' + id + ');">Hide</a></div> \
							<font id="tooLongCommentError' + id + '" size="2" color="red" style="float:left; margin-top:5px;display:none;">Comment length > 5000 chars.</font> \
							</td> \
						</tr> \
					</table> \
			    </form> \
			    </div>'
				);
}
function clickCommentClear (id) {
	$('div.commentReplace' + id ).
		replaceWith(' \
			    <div class="commentReplace'+ id +'"> \
			    </div>'
			   );

}

/*function clickCommentClear2 () {
  $('div.commentReplace2').
  replaceWith(' \
  <div class="commentReplace2"> \
  </div>'
  );

  }

  function clickCommentClear3 (id) {
  $('div.commentReplace' + id ).
  replaceWith(' \
  <div class="commentReplace'+ id +'"> \
  </div>'
  );

  }*/

function share(id, type) {
	$('#tooLongPostError').css('display','none');
	var message = $('#postMessage').val();
	$('#postMessage').val("");
	var postData = { 'message': message, 'id': id, 'type':type };
	var result = $.post( "/post/", postData, function ( json ) {
		if(json['success'] == false){
			if(json['error'] == 'invalid length'){
				$('#tooLongPostError').css('display','inline');
			}
		} else {
			$('#wall').load(' #wall', function(){$(this).children().unwrap()})
		}
	} );
	return false;
}

function endorse(id) {
	var postData = {'id': id};
	$.post( "/endorse/", postData, function ( json ) {
	} );
	return false;
}


function comment(id, page) {
	var link = this.location.pathname;
	var message = $('#commentMessage').val();
	$('#commentMessage').val("");
	var postData = { 'message': message, 'id': id };
	$.post( "/comment/", postData, function ( json ) {
		if(json['success'] == false){
			if(json['error'] == 'invalid length'){
				$('#tooLongCommentError' + id).css('display','inline');
			}
		} else {
			$('#post' + id).load(link + '?page=' + page + ' #post' + id)
		}
	} );
	return false;
}

function deletePost(id) {
	var postData = { 'id': id };
	$.post( "/deletePost/", postData, function ( json ) {
		$('#post' + id).fadeOut("slow");
	} );
	return false;
}

function deleteComment(id) {
	var postData = { 'id': id };
	$.post( "/deleteComment/", postData, function ( json ) {
		$('#c' + id).fadeOut("slow");
	} );
	return false;
}

function deleteEvent(id) {
	var postData = { 'id': id };
	$.post( "/course/deleteEvent/", postData, function ( json ) {
		$('#event' + id).fadeOut("slow");
	} );
	return false;
}

function joinEvent(id) {
	var postData = {'id': id };
	$.post( "/course/joinEvent/", postData, function ( json ) {
		$('#goingCount' + id).load(' #goingCount' + id, function(){$(this).children().unwrap()})
		$('#goingModal' + id).load(' #goingModal' + id, function(){$(this).children().unwrap()})
	} );
	return false;
}

function addCourse() {
	var course_id = $('#course_id').val();
	var course_number = $('#course_number').val();
	var postData = {'course_id': course_id, 'course_number': course_number };
	$.post( "/course/addCourse/", postData, function ( json ) {
		if(json['success'] == true){
			$('#courses').load(' #courses', function(){$(this).children().unwrap()});
			$('#profileButton').load(' #profileButton', function(){$(this).children().unwrap()});
			$('#course_id').val("");
			$('#course_number').val("");
		} else {
			$('#tooManyCoursesError').css('display','inline');
		}
	} );
	return false;
}

function leaveEvent(id) {
	var postData = {'id': id };
	$.post( "/course/leaveEvent/", postData, function ( json ) {
		$('#goingCount' + id).load(' #goingCount' + id, function(){$(this).children().unwrap()})
		$('#goingModal' + id).load(' #goingModal' + id, function(){$(this).children().unwrap()})
	} );
	return false;
}


function renameDocument(id) {
	var newName = $('#renameInput').val();
	var postData = { 'id': id, 'newName': newName };
	$.post( "/renameDocument/", postData, function ( json ) {
		$('#all-files').load(' #all-files', function(){$(this).children().unwrap()})
		$('#doc' + id).load(' #doc' + id, function(){$(this).children().unwrap()})
		$('#rename' + id).load(' #rename' + id, function(){$(this).children().unwrap()})
		$('#delete' + id).load(' #delete' + id, function(){$(this).children().unwrap()})
		$('#share' + id).load(' #share' + id, function(){$(this).children().unwrap()})
		$('#docslist').load(' #docslist', function(){$(this).children().unwrap()})
	} );
	return false;
}

function deleteDocument(id) {
	var postData = { 'id': id };
	$.post( "/deleteDocument/", postData, function ( json ) {
		$('#docslist').load(' #docslist', function(){$(this).children().unwrap()})
	} );
	return false;
}

function accept( id ) {
  var postData = {'id': id};
  $.post( "/accept/", postData, function ( json ) {	  
      $('#req' + id).fadeOut("slow");
  } );
}
function hide( id ) {
  var postData = {'id': id};
  $.post( "/hide/", postData, function ( json ) {
      $('#req' + id).fadeOut("slow");
  } );
}
function autoCompleteType(){
	var query = $('#id_q').val();
	$.ajax({
		url: "/search/autocomplete/",
		data: {
			"q": query,
		},
		success: function(data) {
			autoCompleteResult(data);
		} 
	});
}

function autoCompleteResult(data) {
	var results = data.results;
	$( "#id_q" ).autocomplete({
		source: results,
		focus: function(event, ui) {
        	$(".searchResult").removeClass("ui-state-focus");
        	$("#ui-id-" + ui.item.id)
            	.addClass("ui-state-focus");
    		},
    	select: function( event, ui ) {
   			if ( event.originalEvent.originalEvent.type === "keydown" ) {
   				window.location.href = "/" + ui.item.username
    		}
		    $("#id_q").val(ui.item.value);
		        $("#searchform").submit();
    	},
	}).data("uiAutocomplete" )._renderItem = function( ul, item ) {
		$item = $( "<li class='searchResult' id='ui-id-" + item.id + "'></li>" ).data( "item.autocomplete", item ).append( "<strong><a>" + "<img src='" + item.img + "' style='width:50px;' class='img-rounded' />" + " " + item.label+ "</a></strong>" );
		return $item.appendTo( ul );
	};
}

$( document ).ready( function () {
	var box = document.getElementById('id_q'); 
	box.setAttribute("onkeyup", "autoCompleteType()");
	return false;
} );
