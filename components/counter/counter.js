// KATA Counter — count up once, when visible.
document.querySelectorAll('[data-count-to]').forEach(function (el) {
  var to = parseFloat(el.dataset.countTo);
  var decimals = parseInt(el.dataset.decimals || '0', 10);
  var dur = parseInt(el.dataset.duration || '1400', 10);
  function fmt(v) {
    return v.toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
  }
  function finish() { el.textContent = fmt(to); }
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    finish();
    return;
  }
  el.textContent = fmt(0);
  var io = new IntersectionObserver(function (entries) {
    if (!entries[0].isIntersecting) return;
    io.disconnect();
    var t0 = null;
    function tick(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / dur);
      var eased = 1 - Math.pow(1 - p, 4);
      el.textContent = fmt(to * eased);
      if (p < 1) requestAnimationFrame(tick); else finish();
    }
    requestAnimationFrame(tick);
  }, { threshold: 0.4 });
  io.observe(el);
});
