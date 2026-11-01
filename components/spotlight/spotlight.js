// KATA Spotlight — the light follows the pointer.
document.querySelectorAll('[data-spot]').forEach(function (el) {
  el.addEventListener('pointermove', function (e) {
    var r = el.getBoundingClientRect();
    el.style.setProperty('--mx', ((e.clientX - r.left) / r.width) * 100 + '%');
    el.style.setProperty('--my', ((e.clientY - r.top) / r.height) * 100 + '%');
  });
});
