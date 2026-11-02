// KATA Menubar — click opens; while open, crossing the bar switches menus.
document.querySelectorAll('[data-mbar]').forEach(function (bar) {
  var items = Array.prototype.slice.call(bar.querySelectorAll('.k-mbar-item'));
  var anyOpen = false;
  function set(it, open) {
    it.classList.toggle('open', open);
    it.querySelector('.k-mbar-btn').setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  function closeAll() { items.forEach(function (it) { set(it, false); }); anyOpen = false; }
  items.forEach(function (it) {
    var btn = it.querySelector('.k-mbar-btn');
    btn.addEventListener('click', function () {
      var was = it.classList.contains('open');
      closeAll();
      if (!was) { set(it, true); anyOpen = true; }
    });
    btn.addEventListener('pointerenter', function () { if (anyOpen) { closeAll(); set(it, true); anyOpen = true; } });
    it.querySelectorAll('.k-mbar-mi').forEach(function (mi) { mi.addEventListener('click', closeAll); });
  });
  document.addEventListener('click', function (e) { if (!bar.contains(e.target)) closeAll(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeAll(); });
});
