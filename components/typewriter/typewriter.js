// KATA Typewriter — types, rests, deletes, moves on.
document.querySelectorAll('[data-type]').forEach(function (el) {
  var out = el.querySelector('[data-type-out]');
  var phrases = [];
  try { phrases = JSON.parse(el.getAttribute('data-phrases') || '[]'); } catch (e) { phrases = []; }
  if (!phrases.length) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { out.textContent = phrases[0]; return; }
  var pi = 0, ci = 0, deleting = false;
  function tick() {
    var full = phrases[pi];
    if (deleting) {
      ci--;
      out.textContent = full.slice(0, ci);
      if (ci === 0) { deleting = false; pi = (pi + 1) % phrases.length; setTimeout(tick, 420); return; }
      setTimeout(tick, 34);
    } else {
      ci++;
      out.textContent = full.slice(0, ci);
      if (ci === full.length) { deleting = true; setTimeout(tick, 1850); return; }
      setTimeout(tick, 68 + Math.random() * 60);
    }
  }
  tick();
});
