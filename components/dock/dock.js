// KATA Dock — scale by distance from the cursor; rest when it leaves.
document.querySelectorAll('[data-dock]').forEach(function (dock) {
  var tiles = Array.prototype.slice.call(dock.querySelectorAll('.k-dock-i'));
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  dock.addEventListener('pointermove', function (e) {
    tiles.forEach(function (t) {
      var r = t.getBoundingClientRect();
      var d = Math.abs(e.clientX - (r.left + r.width / 2));
      var s = 1 + 0.55 * Math.max(0, 1 - d / 120);
      t.style.transform = 'scale(' + s.toFixed(3) + ')';
    });
  });
  dock.addEventListener('pointerleave', function () {
    tiles.forEach(function (t) { t.style.transform = ''; });
  });
});
