// KATA Horizontal Reel — the scroll fraction, pointed sideways.
document.querySelectorAll('[data-reel]').forEach(function (root) {
  var strip = root.querySelector('.k-reel-strip');
  var view = root.querySelector('.k-reel-view');
  function update() {
    var max = root.scrollHeight - root.clientHeight;
    var p = max > 0 ? root.scrollTop / max : 0;
    var travel = Math.max(0, strip.scrollWidth - view.clientWidth + 18);
    strip.style.transform = 'translateX(' + (-p * travel).toFixed(1) + 'px)';
  }
  root.addEventListener('scroll', update, { passive: true });
  update();
});
