// JavaScript Document - Modal / Search Results 

//Modal for people search results

function resetForm() {
	document.getElementById('selectRel').reset();
	document.getElementById('newLabel').style.visibility='hidden';
}
function modalHideInput(value) {
document.getElementById('newLabel').style.visibility='hidden';
}
function toggle(value){
if(value=='show')
 document.getElementById('newLabel').style.visibility='visible';
else
 document.getElementById('newLabel').style.visibility='hidden';
}