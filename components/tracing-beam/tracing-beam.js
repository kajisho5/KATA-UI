// KATA Tracing Beam — fill height is the scroll fraction, kept honest.
document.querySelectorAll('[data-beam]').forEach(function (root) {
  var body = root.querySelector('.k-beam-body');
  var rail = root.querySelector('.k-beam-rail');
  var fill = root.querySelector('.k-beam-fill');
  var dot = root.querySelector('.k-beam-dot');
  function update() {
    var max = body.scrollHeight - body.clientHeight;
    var f = max > 0 ? body.scrollTop / max : 0;
    var h = (rail.clientHeight - 8) * f;
    fill.style.height = h + 'px';
    dot.style.top = (4 + h) + 'px';
  }
  body.addEventListener('scroll', update, { passive: true });
  update();
});
