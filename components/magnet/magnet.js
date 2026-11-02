// KATA Magnet — leans toward the cursor at a third of the distance.
document.querySelectorAll('[data-magnet]').forEach(function (zone) {
  var inner = zone.querySelector('.k-mag-in');
  if (!inner || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  zone.addEventListener('pointermove', function (e) {
    var r = zone.getBoundingClientRect();
    var dx = e.clientX - (r.left + r.width / 2);
    var dy = e.clientY - (r.top + r.height / 2);
    zone.classList.add('live');
    inner.style.transform = 'translate(' + (dx * .32).toFixed(1) + 'px,' + (dy * .32).toFixed(1) + 'px)';
  });
  function home() {
    zone.classList.remove('live');
    inner.style.transform = '';
  }
  zone.addEventListener('pointerleave', home);
  zone.addEventListener('pointerup', home);
  zone.addEventListener('pointercancel', home);
});
