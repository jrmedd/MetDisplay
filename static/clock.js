function startClock() {
  var today = new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  h = padZero(h);
  m = padZero(m);
  s = padZero(s);
  $('#clock').html(h + ":" + m + ":" + s);
  var t = setTimeout(startClock, 500);
};

function padZero(i) {
  if (i < 10) {
    i = "0" + i
  };
  return i;
};

startClock();
