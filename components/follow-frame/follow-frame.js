(() => {
  'use strict';
  const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('[data-follow]').forEach(zone => {
    if (zone.dataset.kataReady) return;
    const frame = zone.querySelector('[data-frame]');
    const tag = zone.querySelector('[data-frame-tag]');
    if (!frame || !tag) return;
    zone.dataset.kataReady = 'true';
    let tx = 0, ty = 0, x = 0, y = 0, moved = false, raf = 0;

    function center() { tx = zone.clientWidth / 2; ty = zone.clientHeight / 2; }
    function place() {
      frame.style.left = x + 'px'; frame.style.top = y + 'px';
      tag.style.left = x + 'px'; tag.style.top = y + 'px';
    }
    function jump() { x = tx; y = ty; place(); }
    // The loop runs only while this frame is travelling, and stops once it arrives.
    function step() {
      x += (tx - x) * 0.16; y += (ty - y) * 0.16;
      if (Math.abs(tx - x) < 0.5 && Math.abs(ty - y) < 0.5) { x = tx; y = ty; raf = 0; }
      else raf = requestAnimationFrame(step);
      place();
    }
    function follow() {
      const scale = parseFloat(getComputedStyle(zone).getPropertyValue('--k-mscale'));
      if (scale === 0) { cancelAnimationFrame(raf); raf = 0; jump(); return; }
      if (!raf) raf = requestAnimationFrame(step);
    }
    center(); jump();

    zone.addEventListener('pointermove', event => {
      // Under reduced motion the frame stays parked in the center.
      if (reduced()) return;
      const box = zone.getBoundingClientRect();
      moved = true;
      tx = Math.max(64, Math.min(box.width - 64, event.clientX - box.left));
      ty = Math.max(48, Math.min(box.height - 48, event.clientY - box.top));
      follow();
    });
    zone.addEventListener('pointerleave', () => { moved = false; center(); if (reduced()) jump(); else follow(); });
    // One observer per zone keeps the parked frame centered when the zone resizes.
    if ('ResizeObserver' in window) new ResizeObserver(() => { if (!moved) { cancelAnimationFrame(raf); raf = 0; center(); jump(); } }).observe(zone);
  });
})();
