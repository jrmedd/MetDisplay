var timeout;
function autoTimeout() {
  clearTimeout(timeout);
  timeout = setTimeout(function(){ console.log('Refreshing'); refreshBoards(); }, 50000);
};
$("#timetable").on('webkitAnimationEnd oanimationend msAnimationEnd animationend', function() { //after any text is finished animating
  refreshBoards();
});
function refreshBoards() {
  $.get(window.origin+'/timetable/'+window.location.pathname.split('/').slice(-1), function(data) { //grab the latest timetable
     $("#timetable").html($.parseHTML(data)); //stick the data into a table
     autoTimeout();
   });
};
autoTimeout();

setTimeout(function(){
    location.reload();
}, 1800000);