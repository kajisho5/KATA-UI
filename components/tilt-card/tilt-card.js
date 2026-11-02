// KATA Tilt Card — a few degrees, a whisper of glare, then home.
document.querySelectorAll('[data-tilt]').forEach(function (wrap) {
  var card = wrap.querySelector('.k-tilt-in');
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  wrap.addEventListener('pointermove', function (e) {
    var r = wrap.getBoundingClientRect();
    var px = (e.clientX - r.left) / r.width;
    var py = (e.clientY - r.top) / r.height;
    wrap.classList.add('live');
    card.style.setProperty('--ry', ((px - .5) * 13).toFixed(2) + 'deg');
    card.style.setProperty('--rx', ((.5 - py) * 11).toFixed(2) + 'deg');
    card.style.setProperty('--gx', (px * 100).toFixed(1) + '%');
    card.style.setProperty('--gy', (py * 100).toFixed(1) + '%');
  });
  wrap.addEventListener('pointerleave', function () {
    wrap.classList.remove('live');
    card.style.setProperty('--rx', '0deg');
    card.style.setProperty('--ry', '0deg');
  });
});
