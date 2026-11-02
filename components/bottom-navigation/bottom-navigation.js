// KATA Bottom Navigation — in the catalog preview, taps move the marker.
// In production these are links; the current page carries .on.
document.querySelectorAll('[data-bnav]').forEach(function (bar) {
  bar.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      bar.querySelectorAll('a').forEach(function (x) { x.classList.remove('on'); });
      a.classList.add('on');
    });
  });
});
