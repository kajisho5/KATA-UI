// KATA Scramble — decodes on view; click decodes again.
document.querySelectorAll('[data-scramble]').forEach(function (el) {
  var out = el.querySelector('[data-scr-out]');
  var target = el.getAttribute('data-scramble') || '';
  var GLYPHS = '!<>-_\\/[]{}=+*^?#@$%&';
  var frame = 0, timer = null;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function run() {
    if (reduced) { out.textContent = target; return; }
    frame = 0;
    clearInterval(timer);
    timer = setInterval(function () {
      frame++;
      var settled = Math.floor(frame / 2.2);
      var s = '';
      for (var i = 0; i < target.length; i++) {
        if (target[i] === ' ') { s += ' '; continue; }
        s += i < settled ? target[i] : GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
      }
      out.textContent = s;
      if (settled >= target.length) { out.textContent = target; clearInterval(timer); }
    }, 34);
  }
  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { run(); io.disconnect(); } }, { threshold: .4 });
    io.observe(el);
  } else { run(); }
  el.addEventListener('click', run);
});
