//JS to hide the more button and show on mouse over of the "course dash"
$(document).ready(function(){
	$("#toolBar").mouseover(function() { $("#more").css('visibility','visible'); });
	$("#toolBar").mouseout(function() { $("#more").css('visibility','hidden'); });
});