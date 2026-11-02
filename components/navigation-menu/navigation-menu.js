// KATA Navigation Menu — one panel at a time; Escape and outside clicks close.
document.querySelectorAll('[data-navm]').forEach(function (root) {
  var items = Array.prototype.slice.call(root.querySelectorAll('.k-navm-item'));
  function closeAll(except) {
    items.forEach(function (it) {
      if (it === except) return;
      it.classList.remove('open');
      var b = it.querySelector('.k-navm-btn'); if (b) b.setAttribute('aria-expanded', 'false');
    });
  }
  items.forEach(function (it) {
    var btn = it.querySelector('.k-navm-btn');
    if (!btn || !it.querySelector('.k-navm-panel')) return;
    btn.addEventListener('click', function () {
      var open = it.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) closeAll(it);
    });
    it.addEventListener('pointerenter', function () {
      if (window.matchMedia('(hover: hover)').matches) { closeAll(it); it.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
    });
    it.addEventListener('pointerleave', function () {
      if (window.matchMedia('(hover: hover)').matches) { it.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
    });
  });
  document.addEventListener('click', function (e) { if (!root.contains(e.target)) closeAll(null); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeAll(null); });
});
